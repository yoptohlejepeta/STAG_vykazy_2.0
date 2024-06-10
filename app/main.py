"""Main module of the application."""

import os

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()

logfire.configure(
    token=os.getenv("LOGFIRE_TOKEN"),
    project_name=os.getenv("LOGFIRE_PROJECT_NAME"),
)
logfire.instrument_fastapi(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def read_root(request: Request) -> HTMLResponse:
    """Root.

    Returns
    -------
        HTMLResponse: index page

    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )
