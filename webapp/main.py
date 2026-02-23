import os
import base64
from typing import Union, List
from os.path import dirname, abspath, join
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = Field(default=20, description="Character length of each generated token")

    model_config = {"json_schema_extra": {"examples": [{"length": 20}]}}


class PaginatedResponse(BaseModel):
    items: List[str] = Field(description="List of generated tokens")
    total: int = Field(description="Total number of items returned")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"items": ["abc123"], "total": 1, "page": 1, "page_size": 1, "total_pages": 1}
            ]
        }
    }


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate', response_model=PaginatedResponse)
def generate(
    body: Body,
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=20, ge=1, le=100, description="Number of tokens to generate (1–100)"),
):
    """
    Generate a page of pseudo-random token IDs.

    - **page**: which page of results (1-indexed; tokens are freshly generated each call)
    - **page_size**: how many tokens to return (1–100, default 20)
    - **length**: character length of each token (default 20)

    Example POST body: `{"length": 20}`
    """
    items = [
        base64.b64encode(os.urandom(64))[:body.length].decode('utf-8')
        for _ in range(page_size)
    ]
    return PaginatedResponse(
        items=items,
        total=page_size,
        page=page,
        page_size=page_size,
        total_pages=1,
    )