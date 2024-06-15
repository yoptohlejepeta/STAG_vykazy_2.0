import datetime
from io import StringIO

import holidays
import pandas as pd
import requests

holidays = holidays.CZ(years=2024)


def get_name(shortcut, department, cookie):
    url = "https://ws.ujep.cz/ws/services/rest2/predmety/getPredmetInfo"
    vars = {
        "zkratka": shortcut,
        "outputFormat": "CSV",
        "katedra": department,
        "outputFormatEncoding": "utf-8",
    }

    predmet = requests.get(
        url,
        cookies={"WSCOOKIE": cookie},
        params=vars,
    )

    data = predmet.text
    df = pd.read_csv(StringIO(data), sep=";")

    return df["nazev"][0]


def get_df(url, vars, cookie, type=True):
    rozvrh = requests.get(
        url,
        cookies={"WSCOOKIE": cookie},
        params=vars,
    )

    data = rozvrh.text
    df = pd.read_csv(StringIO(data), sep=";")

    if df.empty:
        return df

    df.datum = pd.to_datetime(
        df.datum,
        format="%d.%m.%Y",
    )
    df.sort_values(by=["datum", "hodinaSkutOd"], ascending=True, inplace=True)

    if type:
        df = df.loc[(df.denZkr == "So") | (df.denZkr == "Ne") & (~df.datum.isin(holidays))]
    df = df.loc[df["obsazeni"] > 0]

    df.reset_index(inplace=True)

    df["typAkceZkr"] = df["typAkceZkr"].replace(
        {"Zápočet": "Zp", "Zkouška": "Zk", "Záp. před zk.": "Zpz"},
    )

    df["hodinaSkutOd"] = pd.to_datetime(df["hodinaSkutOd"], format="%H:%M")
    df["hodinaSkutDo"] = pd.to_datetime(df["hodinaSkutDo"], format="%H:%M")
    df["hodinaOdDo"] = (
        df["hodinaSkutOd"]
        .dt.strftime("%H:%M")
        .str.cat(df["hodinaSkutDo"].dt.strftime("%H:%M"), sep="–")
    )
    try:
        df["kodPredmetu"] = df["katedra"].str.cat(df["predmet"].astype("str"), sep="/")
    except:
        # Někde není vyplněna katedra. (např. idno: 2317, červen 2023)
        df["kodPredmetu"] = df["predmet"]

    df["pocetVyucHodin"] = (
        df["pocetVyucHodin"]
        .fillna(
            (df["hodinaSkutDo"] - df["hodinaSkutOd"]).apply(lambda x: x.total_seconds()) / 3600,
        )
        .round(1)
    )

    # U zápočtů a zkoušek je místo názvu přemětu pouze kód.
    for index, row in df.iterrows():
        if row["kodPredmetu"] == row["nazev"]:
            df.at[index, "nazev"] = get_name(row["predmet"], row["katedra"], cookie)

    df["akce"] = df["kodPredmetu"].str.cat(
        df["nazev"].str.cat(df["typAkceZkr"].apply(lambda x: f"({x})"), sep="  "),
        sep="  ",
    )

    try:
        for i in range(len(df)):
            row = df.iloc[i]
            next_row = df.iloc[i + 1]
            while (row["datum"] == next_row["datum"]) and (
                row["hodinaOdDo"] == next_row["hodinaOdDo"]
            ):
                df.iloc[i, df.columns.get_loc("akce")] = " + ".join(
                    [row["akce"], next_row["akce"]],
                )
                df.drop(labels=i + 1, inplace=True)
                df.reset_index(inplace=True, drop=True)
                next_row = df.iloc[i + 1]
                row = df.iloc[i]
    except IndexError:
        pass

    return df


def get_month_days(year: int, month_name: str):
    month_names_czech = {
        "Leden": 1,
        "Únor": 2,
        "Březen": 3,
        "Duben": 4,
        "Květen": 5,
        "Červen": 6,
        "Červenec": 7,
        "Srpen": 8,
        "Září": 9,
        "Říjen": 10,
        "Listopad": 11,
        "Prosinec": 12,
    }

    month = month_names_czech.get(month_name)

    first_day = datetime.date(year, month, 1)
    next_month = first_day.replace(day=28) + datetime.timedelta(days=4)
    last_day = next_month - datetime.timedelta(days=next_month.day)

    return first_day.strftime("%d/%m/%Y").replace("/", "."), last_day.strftime(
        "%d/%m/%Y",
    ).replace("/", ".")
