import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests

    return (mo,)


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *(Write 2–3 sentences, in words someone outside this course would understand:
    who would use this, and what decision does it help them make?)*

    This tool is going to be very usefull to plan events because you will be able to see the predicted weather for the upcoming week. This will help with picking the day to host the event. In this scenario a club is planning an event and wants to see which day will have the nicest weather.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *(Open the API's address in your browser and read what comes back.
    Then write, in five lines or more, the steps you would take, in plain words.

    Step 1: I will set the coordinates to the town of choice, for the example I will use Belmont,Ma as its where I am from. I will also set the variables to tell me the temp , rain and wind speed for each day.

    Step 2: I will then search for Belmont using the search feature and I will load the chart that reads me all the weather variables for the upcoming week.

    Step 3: I will then read the data from the table with my agent keeping the rules in mind to find the day with the best temprature.

    step 4: I will then reccomend the best day in Belmont to the club so they can have their event.

    step 5: I will then compare near by towns to find the best locoation within a close distance for them to hold their event.

    Then answer:*

    - *Which functions will your tool need? For each, what goes in and what comes out?*  One function I will need is find_place. what goes in is the town name I am using and what comes out is a dictionary with the town name, latititude and longtitude. Another function I will need is get_forecast. What goes into this function is two coordinates and what comes out is the town that I have searched and the daily wether with the variables I have searched for. The last function I will need is show_table. what goes in is the list of the weeks forecast and what comes out is a table with the results.
    - *Which addresses will they request?* The adress they will request is https://geocoding-api.open-meteo.com/v1/search?name=belmont&count=100&language=en&format=json
    - *How will you know you have every record?*  I will know I have every recored when it shows the forecast and weather variables for 7 days.
    - *Which check will you use in section 6, and which two numbers should agree?* The number rows in section 7 should match the amount of days I am getting information for wich will be 7. The number of days that are marked pass should be the same as the days that have broken 0 rules.

    *Commit with the message `mp2: plan before AI` after writing this.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every input the tool needs, in one cell.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    The steps below turn a town name into coordinates, get its seven-day
    forecast, and collect it into one record per day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    A table with one row per day: the date, the high, the low, the chance of
    rain, the strongest wind, and whether the day passes every rule.
    A value equal to a limit passes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    One check, run as code, that shows two numbers agreeing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *(Pick one piece of AI output you did not accept as-is. What did it give
    you, what did you change, and how did you know? Point to the commit or
    the cell. If the agent got it right the first time: what did you do to
    verify that? Pointing to your check in section 7 is enough.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back

    *(Pick two functions in your notebook that your agent wrote or helped write.
    For each, write in your own words what goes in, what comes out, and one line
    you had to ask about. Then choose one change to what the tool does, such as
    another county, another week or another rule. Changing one value in your
    Inputs cell is enough. Write what you expect to change in the answer.
    Commit with the message `mp2: prediction`, make the change, run it, and
    write what happened and whether it matched.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further

    *(What did you try past the main task? What did you find, and where is it
    in this notebook? Pick one: comparing towns, a second forecast service,
    scoring days out of 10, or letting the organizer change the rules without
    editing code.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    *(About how many hours this project took you outside class, as one number.
    It is not graded.)*
    """)
    return


if __name__ == "__main__":
    app.run()
