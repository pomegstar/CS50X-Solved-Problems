import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as t_shares FROM 'transaction' WHERE user_id = ? GROUP BY symbol HAVING t_shares > 0", session["user_id"])

    cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    t_value = cash[0]["cash"]
    for stock in stocks:
        quote = lookup(stock["symbol"])
        stock["price"] = quote["price"]
        stock["value"] = quote["price"] * stock["t_shares"]
        t_value += stock["value"]

    return render_template("index.html", stocks=stocks, cash=cash, t_value=t_value)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        shares = request.form.get("shares")
        quoted = lookup(symbol)
        if not symbol:
            return apology("Missing Symbol")
        elif not quoted:
            return apology("Invalid Symbol")
        elif not shares:
            return apology("Missing Shares")
        elif not shares.isdigit() or int(shares) < 1:
            return apology("Shares must be a postive number")

        t_price = quoted["price"] * int(shares)

        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        r_cash = cash[0]["cash"] - t_price
        if r_cash < 0:
            return apology("You haven't enough cash")
        db.execute("UPDATE users SET cash = ? WHERE id = ?", r_cash, session["user_id"])
        db.execute("INSERT INTO 'transaction' (user_id, symbol, shares, price)  VALUES(?,?,?,?)",
                   session["user_id"], symbol, shares, quoted["price"])

        flash("Bought!")
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    trans = db.execute(
        "SELECT * FROM 'transaction' WHERE user_id = ? ORDER BY timestamp DESC", session["user_id"])

    return render_template("history.html", trans=trans)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quoted = lookup(symbol)
        if not quoted:
            return apology("Invalid Symbol")

        return render_template("quoted.html", quoted=quoted)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")

        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password does not match")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return apology("Username already exists")

        db.execute("INSERT INTO users (username, hash)  VALUES(?,?)",
                   request.form.get("username"), generate_password_hash(request.form.get("password")))

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) as t_shares FROM 'transaction' WHERE user_id = ? GROUP BY symbol HAVING t_shares > 0", session["user_id"])
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        if not symbol:
            return apology("Missing Symbol")
        elif not shares:
            return apology("Missing Shares")
        elif not shares.isdigit() or int(shares) < 1:
            return apology("Shares must be a postive number")
        shares = int(shares)
        symbol = symbol.upper()

        for stock in stocks:
            if stock["symbol"] == symbol:
                if stock["t_shares"] < shares:
                    return apology("Not enough shares")
                else:
                    quoted = lookup(symbol)
                    if not quoted:
                        return apology("Symbol doesn't exist")

                    t_price = quoted["price"] * shares
                    cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
                    r_cash = cash[0]["cash"] + t_price
                    db.execute("UPDATE users SET cash = ? WHERE id = ?", r_cash, session["user_id"])
                    db.execute("INSERT INTO 'transaction' (user_id, symbol, shares, price)  VALUES(?,?,?,?)",
                               session["user_id"], symbol, -shares, quoted["price"])
                    flash("Sold!")
                    return redirect("/")
        return apology("Symbol not owened")

    else:
        return render_template("sell.html", stocks=stocks)


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        rows = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"]
        )
        if not request.form.get("oldp"):
            return apology("must provide old password")
        elif not request.form.get("newp"):
            return apology("Password misssing")
        elif not request.form.get("confirmation"):
            return apology("must confirm password")

        elif not check_password_hash(
            rows[0]["hash"], request.form.get("oldp")
        ):
            return apology("invalid password", 403)
        elif request.form.get("newp") != request.form.get("confirmation"):
            return apology("Password does not match")

        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(request.form.get("newp")), session["user_id"])

        flash("Password changed!")
        return redirect("/")

    else:
        return render_template("change.html")
