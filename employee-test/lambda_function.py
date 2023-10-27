import json
from os import environ as env

import employeescrud


def lambda_handler(event, _):
    print(event)
    method = event.get("httpMethod")

    try:
        query = event.get("queryStringParameters") or {}
        body = event.get("body") or ""

        if not method in {"POST", "GET", "PUT", "DELETE"}:
            code, result = 405, {"message": f"HTTP {method} not allowed here", "succes":"false"}
        else:
            code , result = employeescrud.crete_database_employeetable()
            if code == 200:
                if method == "POST":
                    code, result = employeescrud.create(body)
                if method == "GET":
                    code, result = employeescrud.read(query)
                if method == "PUT":
                    code, result = employeescrud.update(body)
                if method == "DELETE":
                    code, result = employeescrud.delete(body)
            else:
                return code, result

    except Exception as e:
        import traceback

        traceback.print_exc()
        code = 500
        result = {"message": ["internal server error"], "succes":"false"}

    headers = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}

    response = {"statusCode": code, "isBase64Encoded": False, "headers": headers}
    
    if result:
        print(result)
        response.update(body=json.dumps(result))
        print(response)

    return response
