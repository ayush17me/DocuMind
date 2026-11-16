import unittest
from unittest.mock import Mock
from core import REFUSAL, run

class AnswerTests(unittest.TestCase):
    def check_answer(self, verdict, expected):
        index, model = Mock(), Mock()
        index.similarity_search.return_value = [Mock(page_content="It opens at noon.", metadata={"id": "D1-p1.0"})]
        model.invoke.side_effect = [Mock(content=text, usage_metadata={"input_tokens": 10, "output_tokens": 2})
                                    for text in ("Noon [D1-p1.0]", verdict)]
        answer, trace = run(index, model, "When does it open?", verify=verdict is not None)
        self.assertEqual(answer, expected)
        self.assertEqual(trace["sources"], ["D1-p1.0"])
        self.assertEqual(len(trace["calls"]), 1 + int(verdict is not None))

    def test_direct(self):
        self.check_answer(None, "Noon [D1-p1.0]")

    def test_supported(self):
        self.check_answer("PASS", "Noon [D1-p1.0]")

    def test_unsupported(self):
        self.check_answer("FAIL", REFUSAL)
