# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "pyarrow",
#     "altair",
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


@app.cell
def _():
    import altair as alt
    import polars as pl

    return alt, pl


@app.cell
def _():
    from datetime import date

    return (date,)


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
    **One date for every question.** `AS_OF` is the "today" every question counts back from: "last 90 days" is the 90 days ending on `AS_OF`, and "past due" means `due_date` before `AS_OF`. It's the same date `make_data.py` built the data around, so the two line up.
    """)
    return


@app.cell
def _(date):
    AS_OF = date(2026, 11, 8)
    return (AS_OF,)


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

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Ten Questions

    Eight from the scenario's list, and two of my own, in words first and the query right under each.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 1. How much of each project's budget has it spent so far?

    Each project's total expenses against its budget, as a percent, largest share first.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.project_id,
            p.name,
            p.budget,
            coalesce(sum(e.amount), 0) AS total_spent,
            round(coalesce(sum(e.amount), 0) / p.budget * 100, 1) AS pct_of_budget_spent
        FROM project p
        LEFT JOIN expense e ON e.project_id = p.project_id
        GROUP BY p.project_id, p.name, p.budget
        ORDER BY pct_of_budget_spent DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** the most over-committed project has spent about 480% of its budget, and three other active projects have already passed 100%; the four projects that haven't spent anything yet are all still "planned," so no real work — and no spending — has started on them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2. Which tasks are overdue and still not done?

    Tasks past their due date and not completed, with the project's name and the name of the person assigned. *(uses task, project and person — three tables)* A task with nobody assigned yet can't have "the name of the person assigned," so I only count tasks that already have an assignee; the check in Section 1 below shows how many were left out that way, and why.
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT
            t.task_id,
            pr.name AS project_name,
            per.first_name || ' ' || per.last_name AS assigned_to,
            t.due_date
        FROM task t
        JOIN project pr ON pr.project_id = t.project_id
        JOIN person per ON per.person_id = t.assignee_id
        WHERE t.due_date < DATE '{AS_OF}' AND t.completed_date IS NULL
        ORDER BY t.due_date
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** 108 assigned tasks are past due and still not done as of 2026-11-08; that's the list a manager would use to start following up person by person.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 3. Who's carrying too much work right now?

    Each person's hours a week across all their active projects, and who is over 40 — using `person_workload`, the view `build.py` creates for this exact question.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            *,
            total_hours_per_week > 40 AS over_40
        FROM person_workload
        ORDER BY total_hours_per_week DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** only two people are over 40 hours a week across their active projects — Abigail Brown (88) and Ethan Moore (65) — both because they're double-booked onto more than one active project at once, not because any single assignment is too big.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 4. Which expense categories cost more than typical, lately?

    Expenses by category over the last 90 days, keeping only the categories whose total is above the average of the four category totals.
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        WITH category_totals AS (
            SELECT category, sum(amount) AS total
            FROM expense
            WHERE expense_date BETWEEN DATE '{AS_OF}' - INTERVAL 90 DAY AND DATE '{AS_OF}'
            GROUP BY category
        )
        SELECT category, total
        FROM category_totals
        WHERE total > (SELECT avg(total) FROM category_totals)
        ORDER BY total DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** of the four expense categories, only "software" and "data labeling" spent above the four-category average in the last 90 days; "GPU cloud" and "travel" came in below it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 5. Which projects haven't spent anything yet?

    The projects with no expenses at all.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT p.project_id, p.name, p.status
        FROM project p
        WHERE NOT EXISTS (SELECT 1 FROM expense e WHERE e.project_id = p.project_id)
        ORDER BY p.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** four projects have no expenses at all, and all four are still in "planned" status — see Section 2 below for how this answer came from fixing a Part A bug.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 6. How busy and how expensive is each project?

    One row per project with its number of tasks and its total expenses. Each of those two numbers comes from its own subquery against `task` or `expense` directly, instead of one join to both — joining a project straight to both `task` and `expense` at once would multiply rows together and overcount, so each count is "checked against counting it on its own."
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.project_id,
            p.name,
            (SELECT count(*) FROM task t WHERE t.project_id = p.project_id) AS num_tasks,
            (SELECT coalesce(sum(amount), 0) FROM expense e WHERE e.project_id = p.project_id) AS total_expenses
        FROM project p
        ORDER BY p.project_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** task counts per project range from the high 30s to the mid 50s, with no obvious link between how many tasks a project has and how much it has spent — a busy project isn't necessarily an expensive one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 7. Which tasks are assigned to someone who isn't even on that project? *(checks a rule)*

    Every task checked against the rule that its assignee works on its project — `assignment` has no row for that person and that project — and a list of any that break it. *(uses task, project, assignment and person)*
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            t.task_id,
            pr.name AS project_name,
            per.first_name || ' ' || per.last_name AS assignee_name
        FROM task t
        LEFT JOIN assignment a ON a.project_id = t.project_id AND a.person_id = t.assignee_id
        JOIN project pr ON pr.project_id = t.project_id
        JOIN person per ON per.person_id = t.assignee_id
        WHERE t.assignee_id IS NOT NULL AND a.person_id IS NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** exactly two tasks break this rule — task 119 (Acme Retail Data Pipeline, assigned to Mason Jones) and task 29 (Internal Tool 14, assigned to Sophia Perez) — the two rows `make_data.py` plants on purpose, and the query finds both by name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 8. For each manager, how big is their team and how booked up is it?

    For each manager, how many people report to them directly, and the hours a week those people have committed across all of their projects (not just active ones). *(uses person twice — once as the manager, once as the report — and assignment)*
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            m.person_id,
            m.first_name || ' ' || m.last_name AS manager_name,
            count(DISTINCT e.person_id) AS direct_reports,
            coalesce(sum(a.hours_per_week), 0) AS reports_total_hours
        FROM person m
        JOIN person e ON e.manager_id = m.person_id
        LEFT JOIN assignment a ON a.person_id = e.person_id
        GROUP BY m.person_id, m.first_name, m.last_name
        ORDER BY direct_reports DESC, reports_total_hours DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** 14 people manage somebody directly, most of them with 1-2 direct reports, and the hours those reports have committed across every project (active or not) range from 0 up to 222 — a wide enough spread that team size alone doesn't say how booked up a manager's team is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 9. Which clients bring in the most contracted work? *(my own question)*

    Total budget across all of a client's projects, largest first — a different question from #1, which looks at spending against budget; this one only looks at how much business each client represents, with no mention of expenses.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT client_name, sum(budget) AS total_budget, count(*) AS num_projects
        FROM project
        WHERE client_name IS NOT NULL AND client_name != ''
        GROUP BY client_name
        ORDER BY total_budget DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** Summit Realty is BabsonAI Labs' biggest client by contracted budget, at just over $700,000 across three projects — more than double the next closest client.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 10. Do some kinds of projects take longer to finish their tasks? *(my own question)*

    The average number of days between a task being created and being completed, by project category — a different question from #6 and #8, which count tasks and hours; this one measures how long finished work actually takes.
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            p.category,
            round(avg(t.completed_date - t.created_date), 1) AS avg_days_to_complete
        FROM task t
        JOIN project p ON p.project_id = t.project_id
        WHERE t.completed_date IS NOT NULL
        GROUP BY p.category
        ORDER BY avg_days_to_complete DESC
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Answer:** completed LLM app tasks take the longest on average, about 11.2 days, compared to about 9.1 days for data pipeline tasks — a two-day gap, not a dramatic one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. How I Know These Numbers Are Right

    Two checks below, each run as real code against the live database, each comparing a number two different ways. If either query were wrong, the two sides would stop agreeing and the `assert` would raise an error instead of quietly printing a markdown sentence.
    """)
    return


@app.cell
def _(AS_OF, ask, mo):
    _total_overdue = ask(f"""
        SELECT count(*) AS n FROM task
        WHERE due_date < DATE '{AS_OF}' AND completed_date IS NULL
    """).item()
    _parts = ask(f"""
        SELECT
            sum(CASE WHEN assignee_id IS NOT NULL THEN 1 ELSE 0 END) AS with_assignee,
            sum(CASE WHEN assignee_id IS NULL THEN 1 ELSE 0 END) AS without_assignee
        FROM task
        WHERE due_date < DATE '{AS_OF}' AND completed_date IS NULL
    """)
    _with_assignee = _parts["with_assignee"].item()
    _without_assignee = _parts["without_assignee"].item()

    assert _total_overdue == _with_assignee + _without_assignee, "the parts no longer add up to the total"

    mo.md(f"""
    **Check 1 — a total against the sum of its parts.** All overdue, incomplete tasks: **{_total_overdue}**. Split by whether they have an assignee: **{_with_assignee}** with one, **{_without_assignee}** without, which add back up to **{_with_assignee + _without_assignee}**. They agree, which is why question 2's answer of 108 is only the assigned ones, not all {_total_overdue}.
    """)
    return


@app.cell
def _(ask, mo):
    _view_total = ask("SELECT sum(total_hours_per_week) AS total FROM person_workload").item()
    _manual_total = ask("""
        SELECT sum(a.hours_per_week) AS total
        FROM assignment a
        JOIN project p ON p.project_id = a.project_id
        WHERE p.status = 'active'
    """).item()

    assert _view_total == _manual_total, "the view no longer matches a hand-written join"

    mo.md(f"""
    **Check 2 — the view against a hand-written join.** `person_workload` sums to **{_view_total}** hours a week. Re-doing the same sum by hand, joining `assignment` to `project` and filtering to `status = 'active'` myself, also gives **{_manual_total}**. They agree, so question 3 can trust the view.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working With the Agent

    One piece of AI output I didn't accept as-is: my agent's first version of `make_data.py` gave every project expense rows no matter its status, including projects still marked "planned." That made question 5 ("which projects haven't spent anything yet?") always come back empty — zero rows, every time — which isn't a real answer, it's a sign the data doesn't match the scenario: a project that hasn't started yet shouldn't have spending against it.

    I caught this while writing question 5 in this notebook, not while building Part A, which is exactly the case the assignment warns about. I had the agent fix `make_expenses()` in `make_data.py` so it only picks from projects that aren't "planned," regenerated the CSVs, and rebuilt the database. I know it worked because question 5 now returns four real rows instead of zero, and I checked that nothing else moved: the same two tasks (29 and 119) still break the assignment rule, and the row counts in `build.py` are unchanged, because the fix only touches how expenses are picked, not people, projects, assignments or tasks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Reading It Back

    **Question:** The tasks past their due date and not completed, with the project's name and the name of the person assigned. (uses `task`, `project` and `person` — three tables)

    **My prediction, written before running anything, and committed as `db: Prediction` before any question above was answered:** "I expect around a fourth of all tasks to show up here, mostly on older projects that started earlier in the year."
    """)
    return


@app.cell
def _(AS_OF, ask):
    ask(f"""
        SELECT count(*) AS joined_row_count
        FROM task t
        JOIN project pr ON pr.project_id = t.project_id
        JOIN person per ON per.person_id = t.assignee_id
        WHERE t.due_date < DATE '{AS_OF}' AND t.completed_date IS NULL
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Did it match?** Not quite. I predicted around a fourth of all 700 tasks (about 175). The joins alone, before any grouping, produce 108 rows — about 15%, not 25%. I was too high because I didn't account for two things working against each other: about 15% of all tasks never get an assignee in the first place, so they drop out of this inner join entirely (Section 1's Check 1 shows the full overdue count, with and without an assignee); and of the tasks that are already past due, only about 40% stay incomplete — most get finished. Both of those cut into "a fourth" before the join even runs.

    **What one row means.** One row, say task 119 for the Acme Retail Data Pipeline assigned to Mason Jones, means: that task's due date has already passed, nobody has marked it done, and Mason Jones is the person a manager would ask about it first.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Going Further

    I put question 1's answer on a chart: each project's percent of budget spent, as a bar, sorted the same way the table is. It's below, with both axes titled.
    """)
    return


@app.cell
def _(ask):
    # a few projects share the same name (same client, same category), so the
    # chart's labels add the project_id to tell those bars apart
    budget_share = ask("""
        SELECT
            p.name || ' (#' || p.project_id || ')' AS project_label,
            round(coalesce(sum(e.amount), 0) / p.budget * 100, 1) AS pct_of_budget_spent
        FROM project p
        LEFT JOIN expense e ON e.project_id = p.project_id
        GROUP BY p.project_id, p.name, p.budget
        ORDER BY pct_of_budget_spent DESC
    """)
    return (budget_share,)


@app.cell
def _(alt, budget_share, mo):
    budget_chart = mo.ui.altair_chart(
        budget_share.plot.bar(
            x=alt.X("pct_of_budget_spent", title="Percent of budget spent"),
            y=alt.Y("project_label", sort="-x", title="Project"),
        ).properties(title="Budget spent so far, by project")
    )
    budget_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Time Spent

    _Fill in your own number of hours here — about how long the whole project took you outside class. It isn't graded._
    """)
    return


if __name__ == "__main__":
    app.run()
