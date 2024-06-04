import logfire
import os
import plotly.express as px
import pandas as pd
import random
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
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
        title="PostgreSQL Data",
        xaxis_title="Height",
        yaxis_title="Weight",
        font=dict(
            family="Roboto",
            size=18,
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        # hide grid
        xaxis_showgrid=False,
        yaxis_showgrid=False,
    )

    return templates.TemplateResponse("index.html", {"request": request, "plot": fig.to_html(full_html=False, config={"displayModeBar": False}
)})


@app.get("/plot")
def get_plot(db: str, type:str, request: Request):
    if type == "scatter":
        test_df = pd.DataFrame({
            "x": random.sample(range(1, 200), 100),
            "y": random.sample(range(1, 200), 100),
        })
        fig = px.scatter(test_df, x="x", y="y", color_discrete_sequence=["#DB924B"], template="none")
        fig.update_layout(
            title=db,
            xaxis_title="Height",
            yaxis_title="Weight",
            font=dict(
                family="Roboto",
                size=18,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            # hide grid
            xaxis_showgrid=False,
            yaxis_showgrid=False,
        )
    elif type == "bar":
        test_df = pd.DataFrame({
            "x": random.sample(range(1, 200), 100),
            "y": random.sample(range(1, 200), 100),
        })
        fig = px.bar(test_df, x="x", y="y", color_discrete_sequence=["#DB924B"], template="none")
        fig.update_layout(
            title=db,
            xaxis_title="Height",
            yaxis_title="Weight",
            font=dict(
                family="Roboto",
                size=18,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            # hide grid
            xaxis_showgrid=False,
            yaxis_showgrid=False,
        )
    elif type == "line":
        test_df = pd.DataFrame({
            "x": [i for i in range(100)],
            "y": random.sample(range(1, 200), 100),
        })
        fig = px.line(test_df, x="x", y="y", color_discrete_sequence=["#DB924B"], template="none")
        fig.update_layout(
            title=db,
            xaxis_title="Height",
            yaxis_title="Weight",
            font=dict(
                family="Roboto",
                size=18,
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            # hide grid
            xaxis_showgrid=False,
            yaxis_showgrid=False,
        )
    else:
        return HTMLResponse("""
<div role="alert" class="alert alert-warning">
  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
  <span>Warning: Invalid type!</span>
</div>
                            """)
    return templates.TemplateResponse("components/plot.html", {"request": request, "plot": fig.to_html(full_html=False, config={"displayModeBar": False})})