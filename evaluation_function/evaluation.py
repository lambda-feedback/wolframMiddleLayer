import json
from typing import Any
from lf_toolkit.evaluation import Result, Params
import os
import requests

def evaluation_function(
    response: Any,
    answer: Any,
    params: Params,
) -> Result:
    """
    Function used to evaluate a student response.
    ---
    The handler function passes three arguments to evaluation_function():

    - `response` which are the answers provided by the student.
    - `answer` which are the correct answers to compare against.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you. All that matters are the
    return types and that evaluation_function() is the main function used
    to output the evaluation response.
    """

    url = os.getenv("EVALUATE_API")

    eval_type = params["type"]
    data_payload = {
        "type": eval_type,
        "response": response,
        "answer": answer,
        "params": json.dumps(params)
    }

    response = requests.post(url, data=data_payload)
    response_json = response.json()

    if "Success" in response_json:
        if not response_json["Success"]:
            result = Result(is_correct=False)
            result.add_feedback(tag="error", feedback="Wolfram Error")
            return result

    if "error" in response_json:
        if response_json["error"] is not None:
            result = Result(is_correct=False)
            result.add_feedback(tag="error", feedback=response_json["error"])
            return result


    result = Result(is_correct=response_json["is_correct"])
    result.add_feedback(tag="feedback", feedback=response_json["feedback"])

    return result