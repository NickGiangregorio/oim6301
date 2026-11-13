# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "pyarrow",
# ]
# ///
"""Part B: asking database.duckdb questions.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb

    return (duckdb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part B: Questions

    This notebook only reads `database.duckdb`, the one `build.py` builds. Run `build.py` first if the file doesn't exist yet.
    """)
    return


@app.cell
def _(mo):
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every cell asks through `ask`.** It opens the file only to read, runs one query, hands back the result as a table, and closes the file again.
    """)
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    **Question:** _fill in the question here (it has to use 3 or more tables)._

    **My prediction, written before running anything:** _fill in your own guess here, in your own words._


    Question : Overdue, incomplete tasks, with project and assignee name. (3 tables: task, project, person)

    Prediction: "I expect  around a fourth of all tasks to show up here, mostly on older projects that started earlier in the year."
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
