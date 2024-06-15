"""Main module.

Inicializace aplikace. Připojení k Logfire.
"""

import logfire
from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .models import StagResponse
from .settings import settings
from .utils import get_df, get_month_days

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
    request: Request,
    stagUserTicket: str | None = None,
    stagUserInfo: str | None = None,
) -> HTMLResponse:
    """Root.

    Returns
    -------
        HTMLResponse: index page

    """
    if stagUserTicket and stagUserInfo:
        return RedirectResponse(
            url="/home?wscookie=" + stagUserTicket + "&wsuserinfo=" + stagUserInfo,
        )

    login_url = f"{settings.stag.login}?originalURL={request.url}"

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "login_url": login_url,
        },
    )


@app.get("/home")
def home(request: Request, wscookie: str, wsuserinfo: str) -> HTMLResponse:
    """Home.

    Returns
    -------
        HTMLResponse: home page

    """
    stag_info = StagResponse(ticket=wscookie, userinfo=wsuserinfo)

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "ticket": stag_info.ticket,
            "userinfo": stag_info.userinfo.get("email"),
        },
    )


@app.post("/table")
def table(
    request: Request,
    wscookie: str,
    idnos: str = Form(None, alias="idnos"),
) -> HTMLResponse:
    """Table.

    Returns
    -------
        HTMLResponse: table page

    """
    rozvrh_url = "https://ws.ujep.cz/ws/services/rest2/rozvrhy/getRozvrhByUcitel"
    vars = {
        "vsechnyCasyKonani": True,
        "jenRozvrhoveAkce": False,
        "vsechnyAkce": True,
        "jenBudouciAkce": False,
        "lang": "cs",
        "outputFormat": "CSV",
        "rok": 2022,
        "outputFormatEncoding": "utf-8",
    }

    vars["datumOd"], vars["datumDo"] = get_month_days(year=2024, month_name="Květen")

    for idno in list(dict.fromkeys(idnos.replace(" ", "").split(","))):
        idno = int(idno)
        vars["ucitIdno"] = idno

        ucit_df = get_df(rozvrh_url, vars, wscookie)

        ucit_df = ucit_df[["datum", "hodinaOdDo", "pocetVyucHodin", "akce"]]
        ucit_df.columns = ["Datum", "Hodina od do", "Počet hodin", "Akce"]

    return templates.TemplateResponse(
        "components/table.html", {"request": request, "idnos": idnos, "ucit_df": ucit_df}
    )
