import main
import uvicorn
import json


async def app(scope, received, send):
    message={"dados":0}
    payload = {"data": f"{message}"}
    
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = [
        (b"content-type", b"application/json; charset=utf-8"),
        (b"content-length", str(len(body)).encode("utf-8")),
    ]
    await send(
        {
            "type": "http.response.start",
            "status": 200,
    #         "headers": headers,
        }
    )
    await send(
        {
            "type": "http.response.body",
            "body": body,
            "status": 200,
            "headers": headers,
        }
    )

