"""Main module.

Inicializace aplikace. Připojení k Logfire.
"""

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from .models import StagResponse
from .settings import settings

load_dotenv()
app = FastAPI()

logfire.configure(
    token=settings.logfire.token.get_secret_value(),
    project_name=settings.logfire.project_name,
)
logfire.instrument_fastapi(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def read_root(
    request: Request, stagUserTicket: str | None = None, stagUserInfo: str | None = None
) -> HTMLResponse:
    """Root.

    Returns
    -------
        HTMLResponse: index page

    """
    try:
        stag_info = StagResponse(ticket=stagUserTicket, userinfo=stagUserInfo)

        if stag_info:
            return templates.TemplateResponse(
                "home.html",
                {
                    "request": request,
                    "ticket": stag_info.ticket,
                    "userinfo": stag_info.userinfo.get("email"),
                },
            )
    except Exception as e:
        logger.error(e)

    login_url = f"{settings.stag.login}?originalURL={request.url}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "login_url": login_url,
        },
    )
