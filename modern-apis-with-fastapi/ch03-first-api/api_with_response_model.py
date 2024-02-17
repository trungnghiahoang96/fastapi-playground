from typing import Any, Optional

import fastapi
import uvicorn
from fastapi import Response
from pydantic import BaseModel, Field

api = fastapi.FastAPI()


class ResponseModel(BaseModel):
    status_code: int
    message: str
    data: Optional[dict[str, Any]] = Field(default_factory=dict)


@api.get("/")
def index():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Try it: <a href='/api/calculate?x=7&y=11'>/api/calculate?x=7&y=11</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return fastapi.responses.HTMLResponse(content=body)


@api.get("/api/calculate")
def calculate(
    response: Response,
    x: int,
    y: int,
    z: Optional[int] = None,
):
    if z == 0:
        response.status_code = 400
        return ResponseModel(
            status_code=response.status_code, message="Z cannot be zero"
        )

    value = x + y

    if z is not None:
        value /= z
        response.status_code = 200

    if z == 1:
        return ResponseModel(status_code=200, message="Pydantic Default factory!")

    return ResponseModel(
        status_code=200,
        message="ok",
        data={"x": x, "y": y, "z": z, "value": value},
    )


# uvicorn was updated, and it's type definitions don't match FastAPI,
# but the server and code still work fine. So ignore PyCharm's warning:
# noinspection PyTypeChecker
uvicorn.run(api, port=8000, host="127.0.0.1")
