import logfire
import os
import plotly.express as px
import pandas as pd
import random
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
    test_df = pd.DataFrame({
        "x": random.sample(range(1, 200), 100),
        "y": random.sample(range(1, 200), 100),
    })
    
    fig = px.scatter(test_df, x="x", y="y", color_discrete_sequence=["#DB924B"], template="none")
    fig.update_layout(
        title="Test Plot",
        xaxis_title="X",
        yaxis_title="Y",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="white"
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        # hide grid
        xaxis_showgrid=False,
        yaxis_showgrid=False,
    )

    return templates.TemplateResponse("index.html", {"request": request, "plot": fig.to_html(full_html=False, config={"displayModeBar": False}
)})