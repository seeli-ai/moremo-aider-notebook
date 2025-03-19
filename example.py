import marimo

__generated_with = "0.11.22"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd

    alt.renderers.enable('mimetype')
    return alt, mo, pd


@app.cell
def _(alt, pd):
    def create_chart():  
        # Sample data
        df = pd.DataFrame({'x': range(10), 'y': [v**2 for v in range(10)]})

        # Create chart
        chart = alt.Chart(df).mark_line().encode(
            x='x',
            y='y'
        )
        return chart

    create_chart()
    return (create_chart,)


@app.cell
def _():
    from sqlalchemy import create_engine
    import os
    DATABASE_URL = "sqlite:///db/test.db"
    engine = create_engine(DATABASE_URL)
    return DATABASE_URL, create_engine, engine, os


@app.cell
def _(engine, mo, trade):
    dftrades = mo.sql(
        f"""
        SELECT * FROM trade
        """,
        engine=engine
    )
    return (dftrades,)


@app.cell
def _(alt, dftrades):
    def create_chart1(df):  

        # Create chart
        chart = alt.Chart(df).mark_bar().encode(
            alt.X('gap_in_atr:Q', bin=True),
            alt.Y('median(profit_original)')
           # color='trade_type:N',
           # tooltip=['symbol', 'trade_date', 'trade_type']
        ).interactive()
        return chart

    create_chart1(dftrades)
    return (create_chart1,)


if __name__ == "__main__":
    app.run()
