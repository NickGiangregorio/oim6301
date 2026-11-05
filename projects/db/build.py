# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "pyarrow",
# ]
# ///
"""Builds the BabsonAI Labs database.
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
    # Building the Database

    This notebook builds `database.duckdb` from the CSV files in `data/`, which `make_data.py` writes. Run `make_data.py` first if `data/` is empty.
    """)
    return


@app.cell
def _(mo):
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables

    Six `CREATE TABLE` statements, one per entity in the ERD, with every primary key and foreign key declared, and `NOT NULL` / `CHECK` where the scenario's rules call for them.

    - `person.manager_id` references `person` itself, so a manager is just another row of the same table.
    - `position_history` and `assignment` have no single-column id; their primary key is the two columns together, since one pairing (person + date, or person + project) names exactly one row.
    - The rule "a task is assigned only to somebody who works on its project" is **not** a `CHECK` here, because a `CHECK` can only look at one table's own columns, not compare `task` against `assignment`. Section 2 below says which two rows break this rule on purpose, and Part B question 7 finds them with a query instead.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data

    `make_data.py` writes the CSV files in `data/`, following the scenario's rules, with one exception on purpose: two `task` rows are assigned to a real person who does not work on that task's project, breaking the rule behind Part B question 7. `make_data.py` prints which two task ids those are when it runs.
    """)
    return


@app.cell
def _(database, duckdb, mo):
    # Rebuild the database fresh each time this cell runs.
    database.unlink(missing_ok=True)
    _data_dir = mo.notebook_dir() / "data"

    def _csv(file_name):
        # as_posix() avoids Windows backslashes breaking the SQL string below
        return (_data_dir / file_name).as_posix()

    with duckdb.connect(database) as _con:
        _con.execute("""
            CREATE TABLE person (
                person_id  INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name  VARCHAR NOT NULL,
                start_date DATE NOT NULL,
                manager_id INTEGER REFERENCES person(person_id)
            )
        """)
        _con.execute("""
            CREATE TABLE position_history (
                person_id      INTEGER NOT NULL REFERENCES person(person_id),
                effective_date DATE NOT NULL,
                title          VARCHAR NOT NULL,
                work_email     VARCHAR NOT NULL,
                PRIMARY KEY (person_id, effective_date)
            )
        """)
        _con.execute("""
            CREATE TABLE project (
                project_id  INTEGER PRIMARY KEY,
                name        VARCHAR NOT NULL,
                client_name VARCHAR,
                category    VARCHAR NOT NULL CHECK (category IN ('LLM app', 'data pipeline', 'internal tool')),
                budget      DECIMAL(12, 2) NOT NULL CHECK (budget > 0),
                start_date  DATE NOT NULL,
                status      VARCHAR NOT NULL CHECK (status IN ('planned', 'active', 'paused', 'done'))
            )
        """)
        _con.execute("""
            CREATE TABLE assignment (
                person_id      INTEGER NOT NULL REFERENCES person(person_id),
                project_id     INTEGER NOT NULL REFERENCES project(project_id),
                role           VARCHAR NOT NULL,
                hours_per_week INTEGER NOT NULL CHECK (hours_per_week BETWEEN 1 AND 40),
                joined_date    DATE NOT NULL,
                PRIMARY KEY (person_id, project_id)
            )
        """)
        _con.execute("""
            CREATE TABLE task (
                task_id        INTEGER PRIMARY KEY,
                project_id     INTEGER NOT NULL REFERENCES project(project_id),
                assignee_id    INTEGER REFERENCES person(person_id),
                description    VARCHAR NOT NULL,
                created_date   DATE NOT NULL,
                due_date       DATE NOT NULL,
                completed_date DATE,
                CHECK (completed_date IS NULL OR completed_date >= created_date)
            )
        """)
        _con.execute("""
            CREATE TABLE expense (
                expense_id   INTEGER PRIMARY KEY,
                project_id   INTEGER NOT NULL REFERENCES project(project_id),
                expense_date DATE NOT NULL,
                amount       DECIMAL(12, 2) NOT NULL CHECK (amount > 0),
                category     VARCHAR NOT NULL CHECK (category IN ('GPU cloud', 'data labeling', 'software', 'travel')),
                note         VARCHAR
            )
        """)

        # person.manager_id points back at person itself, so DuckDB has to
        # check each row against the ones already loaded. Loading everyone in
        # one statement fails in whatever order the rows come; one INSERT per
        # person, in person_id order, works because make_data.py always gives
        # a person a manager_id smaller than their own person_id.
        _person_rows = _con.sql(f"SELECT * FROM read_csv('{_csv('person.csv')}')").fetchall()
        for _row in _person_rows:
            _con.execute("INSERT INTO person VALUES (?, ?, ?, ?, ?)", _row)

        _con.execute(f"INSERT INTO position_history BY NAME SELECT * FROM read_csv('{_csv('position_history.csv')}')")
        _con.execute(f"INSERT INTO project BY NAME SELECT * FROM read_csv('{_csv('project.csv')}')")
        _con.execute(f"INSERT INTO assignment BY NAME SELECT * FROM read_csv('{_csv('assignment.csv')}')")
        _con.execute(f"INSERT INTO task BY NAME SELECT * FROM read_csv('{_csv('task.csv')}')")
        _con.execute(f"INSERT INTO expense BY NAME SELECT * FROM read_csv('{_csv('expense.csv')}')")

    database.name
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Every other cell asks through `ask`.** It opens the file only to read, runs one query, hands back the result as a table, and closes the file again.
    """)
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _(ask):
    ask("""
        SELECT
            (SELECT count(*) FROM person) AS people,
            (SELECT count(*) FROM project) AS projects,
            (SELECT count(*) FROM assignment) AS assignments,
            (SELECT count(*) FROM task) AS tasks,
            (SELECT count(*) FROM expense) AS expenses
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM person LIMIT 10")
    return


if __name__ == "__main__":
    app.run()
