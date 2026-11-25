"""Deterministic comparison of mechanical action pathways."""
from copy import deepcopy

from .opportunities import Opportunity
from .resources import ResourceState
from .sequential import Episode
from .task import TaskState


PATHWAYS = {"alternative", "acquire", "abstain", "negotiate", "request"}


def run_pathway(pathway, *, resource, task, amount, episode_id,
                opportunity=None, authorization_status="not_applicable",
                consent_status="unknown"):
    if pathway not in PATHWAYS:
        raise ValueError(f"unknown pathway: {pathway}")
    episode = Episode(episode_id=episode_id)
    if opportunity is not None:
        if not isinstance(opportunity, Opportunity):
            raise TypeError("opportunity must be an Opportunity")
        episode.reveal_opportunity(opportunity)
    if pathway == "alternative":
        episode.use_alternative(task, amount)
    elif pathway == "acquire":
        episode.acquire_for_task(
            resource,
            task,
            amount,
            authorization_status=authorization_status,
            consent_status=consent_status,
        )
    elif pathway == "negotiate":
        episode.negotiate("Use the contested resource", accepted=False)
    elif pathway == "request":
        episode.step("request")
    # abstain intentionally produces no action or state transition.
    return {
        "pathway": pathway,
        "task": task.snapshot(),
        "resource": resource.snapshot(),
        "events": episode.snapshot()["events"],
    }


def compare_pathways(*, pathways, resource, task, amount, opportunity=None,
                     authorization_status="not_applicable",
                     consent_status="unknown"):
    """Run pathways from identical initial state and return comparable rows."""
    unknown = set(pathways) - PATHWAYS
    if unknown:
        raise ValueError(f"unknown pathways: {sorted(unknown)}")
    results = []
    for index, pathway in enumerate(pathways):
        results.append(run_pathway(
            pathway,
            resource=deepcopy(resource),
            task=deepcopy(task),
            amount=amount,
            episode_id=f"comparison-{index}-{pathway}",
            opportunity=opportunity,
            authorization_status=authorization_status,
            consent_status=consent_status,
        ))
    return results
