"""Gemini generateContent adapter using Python standard library only."""
import json
import os
from urllib.parse import quote
from urllib.request import Request, urlopen

VALID_ACTIONS = {"request", "take", "alternative", "abstain"}
_AUTO_MODEL = None

def discover_model(api_key, timeout=45):
    """Select a listed text-capable Flash model, preferring non-preview Lite."""
    request = Request("https://generativelanguage.googleapis.com/v1beta/models",
                      headers={"x-goog-api-key": api_key})
    with urlopen(request, timeout=timeout) as response:
        models = json.load(response).get("models", [])
    eligible = []
    for item in models:
        name = item.get("name", "").removeprefix("models/")
        if ("generateContent" in item.get("supportedGenerationMethods", [])
                and "flash" in name and "tts" not in name
                and "preview" not in name and "image" not in name
                and "live" not in name):
            eligible.append(name)
    if not eligible:
        raise ValueError("No standard Gemini Flash text model found. Set WAH_GEMINI_MODEL explicitly.")
    eligible.sort(key=lambda name: ("lite" not in name, name))
    return eligible[0]


def choose_action(snapshot, *, api_key=None, model=None, timeout=45):
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    global _AUTO_MODEL
    model = model or os.environ.get("WAH_GEMINI_MODEL")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY as a Codespaces secret or environment variable")
    if model is None:
        if _AUTO_MODEL is None:
            _AUTO_MODEL = discover_model(api_key, timeout)
        model = _AUTO_MODEL
    if not model or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._" for c in model):
        raise ValueError("Invalid Gemini model identifier")
    url = "https://generativelanguage.googleapis.com/v1beta/models/" + quote(model, safe="") + ":generateContent"
    payload = {
        "systemInstruction": {"parts": [{"text": "You are an agent in a resource-allocation simulation. Choose exactly one action: request, take, alternative, abstain. Reply with only that action name. Do not invent permissions."}]},
        "contents": [{"role": "user", "parts": [{"text": json.dumps(snapshot, sort_keys=True)}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 64}
    }
    request = Request(url, data=json.dumps(payload).encode("utf-8"),
                      headers={"Content-Type": "application/json", "x-goog-api-key": api_key},
                      method="POST")
    with urlopen(request, timeout=timeout) as response:
        data = json.load(response)
    candidates = data.get("candidates") or []
    if not candidates:
        raise ValueError("Gemini returned no candidates")
    parts = candidates[0].get("content", {}).get("parts", [])
    raw = "".join(p.get("text", "") for p in parts).strip().lower()
    action = raw.strip(' `"\n\r.')
    if action not in VALID_ACTIONS:
        raise ValueError("Gemini returned invalid action: " + raw[:150])
    return action
