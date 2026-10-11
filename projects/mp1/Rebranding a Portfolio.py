# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell
def _():
    print ("A finacial advisor or investor would use this tool when one of their client's portfolios is no longer balanced.\n For example, if Apple stock was intially 20 percent of the portfolio but the price sky rockets it is now more then 20%. \nThis would require a rebalancing which would entail selling Apple shares until it is back closer to 20 percent of the portfolio.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell
def _():
    print ("Step 1: Add all of the stock together along with the 5,000 cash to get the portfolio value\n" 
              "Step 2: I will calculate how much should be invested into each stock based on its targeted percentage\n" 
              "Step 3: I will divide the targeted price by each stocks actual price to see how many shares I should buy per stock\n" 
              "Step 4: I will then see the difference in shares that I have versus what I should\n"
              "Step 5: I will update the cash after each trade then calculate what percent each stock makes up of the portfolio\n"
              "Step 6: I will then confirm that I am not negative in cash")
    return


@app.cell
def _():
    print (" My loop is going to carry the cash from one stock to the next, which will be updated after every trade\n. Buying shares will lower my cash balance and selling shares will raise my cash balance. After the last trade, \nthe running balance will be the leftover cash ")
    return


@app.cell
def _():
    print (" I will check the portfolios total value before I rebalance it. After rebalancing it I will check the values of the stock\n and the remaining cash, which should equal the starting value for the portfolio.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    cash = 5000.00
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}
    return cash, holdings, target_weights


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(cash, holdings):
    total_value = cash
    for h in holdings:
        ticker = h[0]
        shares = h[1]
        price = h[2]
        value = shares * price
        total_value = total_value + value

    print(f"Total portfolio value: ${total_value:.2f}")
    return (total_value,)


@app.cell
def _(holdings, target_weights, total_value):
    for _h in holdings:
        _ticker = _h[0]
        _weight = target_weights[_ticker]
        _target = total_value * _weight
        print(f"{_ticker}: target investment = ${_target:.2f}")
    return


@app.cell
def _(cash, holdings, target_weights, total_value):
    running_cash = cash
    trades = []
    for _h in holdings:
        _ticker = _h[0]
        _shares = _h[1]
        _price = _h[2]
        _weight = target_weights[_ticker]
        _target_dollars = total_value * _weight
        _target_shares = int(_target_dollars // _price)
        _diff_shares = _target_shares - _shares
        _trade_cost = _diff_shares * _price
        running_cash = running_cash - _trade_cost
        _final_value = _target_shares * _price
        trades.append((_ticker, _shares, _target_shares, _diff_shares, _final_value))
    return running_cash, trades


@app.cell
def _(running_cash):
    if running_cash < 0:
        print("Warning: cash balance is negative")
    else:
        print(f"Final cash balance: ${running_cash:.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(running_cash, total_value, trades):
    print(f"{'Ticker':<8}{'Have':>8}{'Want':>8}{'Trade':>8}{'Value':>12}{'Weight':>10}")
    for _t in trades:
        _ticker = _t[0]
        _have = _t[1]
        _want = _t[2]
        _diff = _t[3]
        _final_value = _t[4]
        _weight_after = _final_value / total_value * 100
        print(f"{_ticker:<8}{_have:>8}{_want:>8}{_diff:>+8}{_final_value:>12.2f}{_weight_after:>9.2f}%")

    _cash_weight = running_cash / total_value * 100
    print(f"{'Cash':<8}{'':>8}{'':>8}{'':>8}{running_cash:>12.2f}{_cash_weight:>9.2f}%")
    print(f"Cash remaining: ${running_cash:.2f}")
    return


@app.cell
def _(target_weights, total_value, trades):
    for _t in trades:
        _ticker = _t[0]
        _final_value = _t[4]
        _actual_weight = _final_value / total_value
        _target_weight = target_weights[_ticker]
        _diff_points = (_actual_weight - _target_weight) * 100
        print(f"{_ticker}: target {_target_weight*100:.1f}%, actual {_actual_weight*100:.2f}%, off by {_diff_points:+.2f} percent")
    return


@app.cell
def _():
    print (" Selling 79 Tesla and 60 Amazon shares and buying 39 Apple, 25 Microsoft, \n58 Google and 24 Nvidia puts every stock within 0.24 percentage points of its target percentage  ")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    print (" I know that these numbers are right because the starting total value of the portfolio matches the ending stock and cash value combined")
    return


@app.cell
def _(running_cash, total_value, trades):
    check_total = running_cash
    for _t in trades:
        check_total = check_total + _t[4]

    difference = check_total - total_value
    print(f"Starting total value: ${total_value:.2f}")
    print(f"Ending stock value + cash: ${check_total:.2f}")
    print(f"Difference: ${difference:.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell
def _():
    print(" during step 3 in cell 3 of part 4 my agent rounded total shares to the neareast whole number which completely threw off my left over cash.\n This is because the tool was either spending  more or less money then I wanted it to.\n I corrected this mistake by removing round and putting INT and adding //. ")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _():
    print (" I went further by replacing the prices that I was given with the live prices from yahoo finance. \n my agent then added a $5 fee per trade and skipped trades under $500. Which cost $30 and left $1,208.01 in cash, the largest gap \nfrom the target was 0.16 percentage points. My agent also tried rebalancing only holdings more than 5 points off the target which left $12,111.47  \n and Apple 3.79 points under its target. Third,  my agent added sliders for the targets, which refuses any set that does not add up to 100%. ")
    return


@app.cell
def _(holdings):
    import yfinance as yf

    tickers = [h[0] for h in holdings]
    live_prices = {}
    for _t in tickers:
        try:
            _hist = yf.Ticker(_t).history(period="5d")
            live_prices[_t] = round(float(_hist["Close"].iloc[-1]), 2)
        except Exception:
            live_prices[_t] = next(h[2] for h in holdings if h[0] == _t)   # fall back to listed price
            print(f"Could not fetch {_t}, using listed price")

    live_holdings = [(_t, _n, live_prices[_t]) for _t, _n, _ in holdings]
    for _h in live_holdings:
        print(f"{_h[0]}: ${_h[2]:.2f}")
    return live_holdings, tickers


@app.cell
def _():
    def rebalance(positions, start_cash, weights, fee=0.0, min_trade=0.0, drift_limit=None):
        value_now = start_cash + sum(n * p for _, n, p in positions)
        cash_left = start_cash
        rows = []
        for ticker, have, price in positions:
            drift = (have * price / value_now - weights[ticker]) * 100        # points off target now
            want = int(value_now * weights[ticker] // price)                  # round down
            diff = want - have
            skip = (diff == 0
                    or abs(diff) * price < min_trade                          # trade too small
                    or (drift_limit is not None and abs(drift) <= drift_limit))  # not drifted enough
            if skip:
                want, diff = have, 0
            else:
                cash_left -= diff * price + fee                               # trade cost plus fee
            rows.append((ticker, have, want, diff, drift, price))
        value_after = sum(r[2] * r[5] for r in rows) + cash_left              # fees reduce this
        return rows, cash_left, value_after

    def show(rows, cash_left, value_after, weights):
        print(f"{'Ticker':<8}{'Have':>6}{'Want':>6}{'Trade':>7}{'Weight':>9}{'Target':>8}{'Gap':>9}")
        for ticker, have, want, diff, drift, price in rows:
            w = want * price / value_after * 100
            gap = w - weights[ticker] * 100
            print(f"{ticker:<8}{have:>6}{want:>6}{diff:>+7}{w:>8.2f}%{weights[ticker]*100:>7.1f}%{gap:>+8.2f}")
        print(f"Cash left: ${cash_left:.2f}   Portfolio after: ${value_after:.2f}")
        if cash_left < 0:
            print("WARNING: cash is negative")

    return rebalance, show


@app.cell
def _(cash, live_holdings, rebalance, show, target_weights):
    _rows, _cash_left, _after = rebalance(live_holdings, cash, target_weights, fee=5, min_trade=500)
    show(_rows, _cash_left, _after, target_weights)
    _worst = max(abs(r[2] * r[5] / _after * 100 - target_weights[r[0]] * 100) for r in _rows)
    print(f"Largest gap from target: {_worst:.2f} percentage points")
    return


@app.cell
def _(cash, live_holdings, rebalance, show, target_weights):
    _rows, _cash_left, _after = rebalance(live_holdings, cash, target_weights, drift_limit=5)
    show(_rows, _cash_left, _after, target_weights)
    return


@app.cell
def _(mo, target_weights, tickers):


    sliders = mo.ui.array(
        [mo.ui.slider(0, 100, step=1, value=int(target_weights[_t] * 100), label=_t)
         for _t in tickers]
    )
    sliders
    return (sliders,)


@app.cell
def _(mo, sliders, tickers):
    _pcts = sliders.value
    _total = sum(_pcts)
    mo.stop(
        _total != 100,
        mo.callout(mo.md(f"**Refused:** the targets add up to {_total}%, not 100%. Adjust the sliders."),
                   kind="danger"),
    )
    slider_weights = {_t: _p / 100 for _t, _p in zip(tickers, _pcts)}
    mo.callout(mo.md("Targets add up to 100%."), kind="success")
    return (slider_weights,)


@app.cell
def _(cash, live_holdings, rebalance, show, slider_weights):
    _rows, _cash_left, _after = rebalance(live_holdings, cash, slider_weights)
    show(_rows, _cash_left, _after, slider_weights)
    return


if __name__ == "__main__":
    app.run()
