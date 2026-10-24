import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import requests

    return mo, requests


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


@app.cell
def _():
    place = "Belmont"
    state = "Massachusetts"
    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 30
    max_wind_mph = 15
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    The steps below turn a town name into coordinates, get its seven-day
    forecast, and collect it into one record per day.
    """)
    return


@app.cell
def _(place, requests, state):
    def find_place(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"
        reply = requests.get(url, params={"name": place, "count": 100, "language": "en", "format": "json"}).json()
        matches = reply["results"]
        for match in matches:
            if match["admin1"] == state:
                return {"name": match["name"], "lat": match["latitude"], "lon": match["longitude"]}
        return None


    def get_forecast(lat, lon):
        url = "https://api.open-meteo.com/v1/forecast"
        reply = requests.get(url, params={
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
        }).json()
        daily = reply["daily"]
        days = []
        for date, high, low, rain, wind in zip(
            daily["time"],
            daily["temperature_2m_max"],
            daily["temperature_2m_min"],
            daily["precipitation_probability_max"],
            daily["wind_speed_10m_max"],
        ):
            days.append({"date": date, "high": high, "low": low, "rain_chance": rain, "wind": wind})
        return days


    town = find_place(place, state)
    forecast = get_forecast(town["lat"], town["lon"])
    town
    return find_place, forecast, get_forecast, town


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    A table with one row per day: the date, the high, the low, the chance of
    rain, the strongest wind, and whether the day passes every rule.
    A value equal to a limit passes
    """)
    return


@app.cell
def _():
    # duplicate removed; see the cell above for the best-day calculation
    return


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    table = []
    for day in forecast:
        broken_rules = 0
        if day["high"] < lowest_high_f or day["high"] > highest_high_f:
            broken_rules = broken_rules + 1
        if day["rain_chance"] > max_rain_chance:
            broken_rules = broken_rules + 1
        if day["wind"] > max_wind_mph:
            broken_rules = broken_rules + 1
        passes = broken_rules == 0
        _row = {
            "date": day["date"],
            "high": day["high"],
            "low": day["low"],
            "rain_chance": day["rain_chance"],
            "wind": day["wind"],
            "passes": passes,
            "broken_rules": broken_rules,
        }
        table.append(_row)

    table
    return (table,)


@app.cell
def _(table, town):
    passing_days = []
    for _row in table:
        if _row["passes"]:
            passing_days.append(_row)

    if len(passing_days) > 0:
        best = passing_days[0]
        for _row in passing_days:
            if _row["rain_chance"] < best["rain_chance"]:
                best = _row
            elif _row["rain_chance"] == best["rain_chance"] and _row["wind"] < best["wind"]:
                best = _row
        reason = f"it passes every rule and has the lowest chance of rain ({best['rain_chance']}%)"
    else:
        best = table[0]
        for _row in table:
            if _row["broken_rules"] < best["broken_rules"]:
                best = _row
        reason = f"no day passes every rule, but this one breaks the fewest rules ({best['broken_rules']})"

    f"The best day for the event in {town['name']} is {best['date']}, because {reason}."
    return (passing_days,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    One check, run as code, that shows two numbers agreeing.
    """)
    return


@app.cell
def _(passing_days, table):
    rows_found = len(table)

    zero_broken_rules = 0
    for _row in table:
        if _row["broken_rules"] == 0:
            zero_broken_rules = zero_broken_rules + 1

    f"Rows in table: {rows_found} (should be 7). Days marked passes: {len(passing_days)}, days with 0 broken rules: {zero_broken_rules} (should match)."
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

    I compared towns: I ran the same forecast and rule check for Lexington,
    Massachusetts, next to Belmont, using the same `find_place` and
    `get_forecast` functions (two cells below this one).

    Both towns picked **2026-10-24** as the best day, with 0% chance of rain
    in each, since they are close together and share similar weather. Belmont
    had 6 of 7 days pass every rule; Lexington had 5 of 7, failing on
    2026-10-27 and 2026-10-28 because the high was below 55°F on those days,
    where Belmont only failed once, and for the same reason.
    """)
    return


@app.cell
def _(
    find_place,
    get_forecast,
    highest_high_f,
    lowest_high_f,
    max_rain_chance,
    max_wind_mph,
):
    second_place = "Lexington"
    second_state = "Massachusetts"

    second_town = find_place(second_place, second_state)
    second_forecast = get_forecast(second_town["lat"], second_town["lon"])

    second_table = []
    for _day in second_forecast:
        _broken_rules = 0
        if _day["high"] < lowest_high_f or _day["high"] > highest_high_f:
            _broken_rules = _broken_rules + 1
        if _day["rain_chance"] > max_rain_chance:
            _broken_rules = _broken_rules + 1
        if _day["wind"] > max_wind_mph:
            _broken_rules = _broken_rules + 1
        _passes = _broken_rules == 0
        _row = {
            "date": _day["date"],
            "high": _day["high"],
            "low": _day["low"],
            "rain_chance": _day["rain_chance"],
            "wind": _day["wind"],
            "passes": _passes,
            "broken_rules": _broken_rules,
        }
        second_table.append(_row)

    second_table
    return second_table, second_town


@app.cell
def _(second_table, second_town):
    second_passing_days = []
    for _row in second_table:
        if _row["passes"]:
            second_passing_days.append(_row)

    if len(second_passing_days) > 0:
        second_best = second_passing_days[0]
        for _row in second_passing_days:
            if _row["rain_chance"] < second_best["rain_chance"]:
                second_best = _row
            elif _row["rain_chance"] == second_best["rain_chance"] and _row["wind"] < second_best["wind"]:
                second_best = _row
        second_reason = f"it passes every rule and has the lowest chance of rain ({second_best['rain_chance']}%)"
    else:
        second_best = second_table[0]
        for _row in second_table:
            if _row["broken_rules"] < second_best["broken_rules"]:
                second_best = _row
        second_reason = f"no day passes every rule, but this one breaks the fewest rules ({second_best['broken_rules']})"

    f"The best day for the event in {second_town['name']} is {second_best['date']}, because {second_reason}."
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
