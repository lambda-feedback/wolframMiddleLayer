import os
from typing import Any

import requests
from lf_toolkit.preview import Result, Params, Preview

def preview_function(response: Any, params: Params) -> Result:
    """
    Function used to preview a student response.
    ---
    The handler function passes three arguments to preview_function():

    - `response` which are the answers provided by the student.
    - `params` which are any extra parameters that may be useful,
        e.g., error tolerances.

    The output of this function is what is returned as the API response
    and therefore must be JSON-encodable. It must also conform to the
    response schema.

    Any standard python library may be used, as well as any package
    available on pip (provided it is added to requirements.txt).

    The way you wish to structure you code (all in this function, or
    split into many) is entirely up to you.
    """
    try:
        url = os.getenv("PREVIEW_API")

        data_payload = {
            "response": response
        }

        wolfram_response = requests.post(url, data=data_payload)
        response_json = wolfram_response.json()

        print(response_json)

        if "Success" in response_json:
            if not response_json["Success"]:
                result = Result(preview=Preview(feedback=response_json["error"]))
                return result

        if "error" in response_json:
            if response_json["error"] is not None:
                result = Result(preview=Preview(feedback=response_json["error"]))
                return result


        result = Result(preview=Preview(latex=response_json["latex"],sympy=response_json["sympy"]))

        return result
    except Exception as e:
        return Result(preview=Preview(feedback=str(e)))
