import marimo

__generated_with = "0.11.22"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import altair as alt
    import pandas as pd
    import polars as pl

    alt.renderers.enable('mimetype')
    return alt, mo, pd, pl


@app.cell
def _():
    from sqlalchemy import create_engine
    import os
    DATABASE_URL = "sqlite:///db/test.db"
    engine = create_engine(DATABASE_URL)
    return DATABASE_URL, create_engine, engine, os


@app.cell
def _(engine, mo, trade):
    df_trades = mo.sql(
        f"""
        SELECT * FROM trade
        """,
        engine=engine
    )
    return (df_trades,)


@app.cell
def _(alt, df_trades):
    scatter = alt.Chart(df_trades).mark_circle().transform_calculate(
       side = "datum.trade_type > 0 ? 'Long' :'Short'"
    ).encode(
       alt.X('gap_in_atr:Q', title="Gap in ATR"),
       alt.Y('profit_original:Q', title="Profit Original"),
       tooltip=['symbol', 'trade_date', 'profit_original'],
       color=alt.Color('side:N',
               scale=alt.Scale(
               domain=['Short', 'Long'],
               range=['red', 'green']
            )
       ),
   
    ).properties(
        width=700
    )

    scatter
    return (scatter,)


@app.cell
def _(alt, df_trades):

    chart = alt.Chart(df_trades).mark_bar().encode(
            x=alt.X('gap_in_atr:Q', 
                   bin=alt.Bin(maxbins=10), 
                   title="Gap in ATR (Binned)"),
            y=alt.Y('mean(profit_original):Q', 
                   title="Average Profit"),
            tooltip=[
                alt.Tooltip('gap_in_atr:Q', title="Bin Start", bin='origin'),
                alt.Tooltip('count()', title="Number of Records"),
                alt.Tooltip('mean(profit_original):Q', title="Avg Profit", format='.2f')
            ]
        ).interactive()
    chart


    return (chart,)


@app.cell
def _(df_trades, pl):

    df_gap = df_trades.sort('gap_in_atr')
    df_gap = df_gap.with_columns(pl.arange(1, df_gap.height + 1).alias("Line_Number"))
    df_gap = df_gap.with_columns((pl.col('Line_Number') / 1).floor().alias('Bin'))
                           
    df_gap
    return (df_gap,)


@app.cell
def _(alt, df_gap):
    # Create chart

    chart1 = alt.Chart(df_gap).mark_bar().encode(
        alt.X('Bin:N',  bin=alt.Bin(maxbins=80)),
        y=('mean(profit_original)'),
        tooltip=['mean(profit_original)', 'median(profit_original)', 'count()', 'min(gap_in_atr)',  'max(gap_in_atr)' ]
       # color='gap_in_atr:Q',
       # [alt.Tooltip('gap_in_atr:Q', title="Bin Start", bin='origin')]
    ).interactive().properties(title='Average Profit per Gap in ATR',width=700)


    chart1
    return (chart1,)


if __name__ == "__main__":
    app.run()
