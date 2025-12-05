import sys

from lf_toolkit.shared.params import Params

from evaluation_function.evaluation import evaluation_function
from evaluation_function.preview import preview_function


def dev():
    """Run the evaluation function from the command line for development purposes.

    Usage: python -m evaluation_function.dev <answer> <response>
    """
    
    answer = "x+y"
    response = "x+y"
    params = {"type": "structure"}

    # result = evaluation_function(answer, response, params)
    result = preview_function(response, {})

    print(result)

if __name__ == "__main__":
    dev()