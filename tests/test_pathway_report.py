import unittest

from run_pathway_comparison import build_report, markdown_report


class PathwayReportTests(unittest.TestCase):
    def test_report_contains_all_pathways(self):
        report = build_report()
        self.assertEqual(
            [row["pathway"] for row in report["pathways"]],
            ["alternative", "acquire", "abstain", "negotiate", "request"],
        )

    def test_markdown_report_is_human_readable(self):
        text = markdown_report(build_report())
        self.assertIn("# Deterministic Pathway Comparison", text)
        self.assertIn("| alternative |", text)
        self.assertIn("not WAH efficacy evidence", text)


if __name__ == "__main__":
    unittest.main()
