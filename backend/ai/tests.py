from django.test import SimpleTestCase

from .exceptions import AIInvalidResponseError
from .services import _parse_analysis
from .skills import compare_skills, normalize_many


class CompareSkillsTests(SimpleTestCase):
    def test_owned_skill_is_never_missing(self):
        r = compare_skills(["Python", "PostgreSQL", "Git"], ["Django", "postgres", "Python"])
        self.assertEqual(r["matched"], ["Python", "PostgreSQL"])
        self.assertEqual(r["missing"], ["Git"])
        self.assertFalse(set(r["matched"]) & set(r["missing"]))

    def test_percentage(self):
        r = compare_skills(["Python", "Git"], ["python"])
        self.assertEqual(r["percentage"], 50.0)

    def test_empty_required_gives_zero(self):
        self.assertEqual(compare_skills([], ["Python"])["percentage"], 0)

    def test_normalize_many_removes_duplicates(self):
        self.assertEqual(
            normalize_many(["Postgres", "PostgreSQL ", "postgresql", " Python "]),
            ["PostgreSQL", "Python"],
        )


class ParseAnalysisTests(SimpleTestCase):
    def test_parses_fenced_json_and_removes_overlap(self):
        raw = (
            '```json\n{"job_title": "Dev", "required_skills": ["Python", "postgres"],'
            ' "preferred_skills": ["Docker", "python"]}\n```'
        )
        result = _parse_analysis(raw)
        self.assertEqual(result["required_skills"], ["Python", "PostgreSQL"])
        self.assertEqual(result["preferred_skills"], ["Docker"])

    def test_rejects_non_json(self):
        with self.assertRaises(AIInvalidResponseError):
            _parse_analysis("not json")

    def test_rejects_empty_required_skills(self):
        with self.assertRaises(AIInvalidResponseError):
            _parse_analysis('{"required_skills": []}')
