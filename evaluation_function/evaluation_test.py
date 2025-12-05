import unittest
from unittest.mock import Mock, patch

from .evaluation import Params, evaluation_function

class TestEvaluationFunction(unittest.TestCase):
    """
    TestCase Class used to test the algorithm.
    ---
    Tests are used here to check that the algorithm written
    is working as it should.

    It's best practise to write these tests first to get a
    kind of 'specification' for how your algorithm should
    work, and you should run these tests before committing
    your code to AWS.

    Read the docs on how to use unittest here:
    https://docs.python.org/3/library/unittest.html

    Use evaluation_function() to check your algorithm works
    as it should.
    """

    @patch('requests.post')
    def test_evaluation(self, mock_post):
        mock_api_response = {
            "is_correct": True,
            "feedback": "",
            "error": None
        }

        mock_response_obj = Mock()
        mock_response_obj.status_code = 200
        mock_response_obj.json.return_value = mock_api_response

        mock_post.return_value = mock_response_obj

        # 4. Run your actual test logic
        response_input, answer, params = "x+y", "x+y", {"type": "structure"}

        result = evaluation_function(response_input, answer, params).to_dict()

        # 5. Assertions
        self.assertEqual(result.get("is_correct"), True)
        self.assertFalse(result.get("feedback", False))

        mock_post.assert_called_once()
