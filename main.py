import logfire
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

logfire.configure(token=os.getenv("LOGFIRE_TOKEN"), project_name=os.getenv("LOGFIRE_PROJECT_NAME"))
logfire.instrument_fastapi(app)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})