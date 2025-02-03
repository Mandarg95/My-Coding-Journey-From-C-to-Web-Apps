import os
import re

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

    # Get the user's ID from the session
    user_id = session.get("user_id")

    # Retrieve the stocks the user has bought and the number of shares for each from the database
    buys = db.execute("SELECT symbol, shares FROM buysinfo WHERE user_id = ?", user_id)

    # Initialize the total portfolio value
    index_cash = 0

    # Loop through each stock the user owns
    for buy in buys:
        symbol = buy["symbol"]  # Get the stock symbol
        shares = buy["shares"]  # Get the number of shares owned

        # Get the current stock price and other info
        stock_info = lookup(symbol)

        # Calculate the total value of the shares owned for this stock
        total = shares * stock_info["price"]

        # Add the value of this stock to the total portfolio value
        index_cash += total

        # Update the database with the current stock price and total value
        db.execute("UPDATE buysinfo SET price = ?, total = ? WHERE user_id = ? AND symbol = ?",
                   usd(stock_info["price"]), usd(total), user_id, symbol)

    # Retrieve the user's current cash balance from the database
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)

    # Add the cash balance to the total portfolio value
    index_cash += cash[0]["cash"]

    # Retrieve the updated stock information for rendering in the template
    update_buys = db.execute("SELECT * FROM buysinfo WHERE user_id = ?", user_id)

    # Render the portfolio page with the updated stock and cash information
    return render_template("index.html", index=update_buys, total=usd(index_cash), cash=usd(cash[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Pulling information from the form
        symbol = request.form.get("symbol")  # Get the stock symbol from the form
        shares_unit = request.form.get("shares", "0")  # Get the number of shares from the form, default to "0"

        # Looking up the stock in API
        dic = lookup(symbol)  # Use lookup function to get stock details (e.g., price)
        user_id = session.get("user_id")  # Get the user ID from the session
        buys = db.execute("SELECT * FROM buysinfo WHERE user_id = ?", user_id)  # Get current user's buy information
        cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)  # Get current user's available cash

        try:
            # Validate input and stock information
            if not symbol or dic is None:
                return apology("Invalid Symbol", 400)  # Return an error if symbol is invalid or not found
            elif shares_unit == '' or int(shares_unit) < 1:
                return apology("missing shares", 400)  # Return an error if no shares are specified or invalid

            cash = float(cash[0]["cash"])  # Convert cash to a float value
            current_total = float(dic["price"] * float(shares_unit))  # Calculate total price of the shares

            # Check if user has enough cash to buy the shares
            if current_total > cash:
                return apology("can't afford", 400)  # Return an error if user cannot afford the shares

            # Record the transaction in the history table
            db.execute("INSERT INTO History (user_id,symbol,shares,price) VALUES (?,?,?,?)",
                       user_id, symbol, shares_unit, usd(dic["price"]))

            # Check if the user already owns the stock
            if len(buys) != 0 and buys[0]["symbol"] == dic["symbol"]:
                # If they do, update the shares and total price
                share_total = float(buys[0]["shares"]) + float(shares_unit)
                total = float(share_total * dic["price"])
                db.execute("UPDATE buysinfo SET shares = shares + ?, total = ? WHERE symbol = ?",
                           shares_unit, usd(total), buys[0]["symbol"])
                # Deduct the cost from user's cash balance
                db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                           float(current_total), user_id)
                return redirect("/")  # Redirect to the homepage after successful purchase

            else:
                # If the user doesn't own the stock, insert a new record
                db.execute("INSERT INTO buysinfo (user_id,symbol,shares,price,total) VALUES (?,?,?,?,?)",
                           user_id, dic["symbol"], shares_unit, usd(dic["price"]), usd(current_total))
                # Update the user's cash balance
                db.execute("UPDATE users SET cash = ? WHERE id = ?",
                           float(cash - current_total), user_id)
                return redirect("/")  # Redirect to the homepage after successful purchase
        except (ValueError):
            return apology("invalid shares", 400)  # Return an error if shares input is invalid

    return render_template("buy.html")  # Render the buy page if request method is GET


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session.get("user_id")
    data = db.execute("SELECT * FROM History WHERE user_id = ?", user_id)
    return render_template("history.html", info=data)


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
        quote = request.form.get("symbol")
        dic = lookup(quote)

        if dic is not None:
            return render_template("quoted.html", symbol=dic["symbol"], price=usd(dic["price"]))
        else:
            return apology("Invalid Symbol", 400)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provied username", 400)
        elif not request.form.get("password") or not request.form.get("confirmation"):
            return apology("must provied password", 400)

        try:
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            if password == confirmation:
                password = generate_password_hash(password)
                db.execute("INSERT INTO users (username,hash) VALUES (?,?)", username, password)
                row = db.execute("SELECT id FROM users WHERE username=?", username)
                session["user_id"] = row[0]["id"]
                return redirect("/")

            else:
                return apology("password don't match", 400)

        except ValueError:
            return apology("username taken", 400)

    return render_template("registration.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    user_id = session.get("user_id")
    buys = db.execute("SELECT * FROM buysinfo WHERE user_id = ?", user_id)
    if request.method == "POST":
        shares_unit = request.form.get("shares")
        share_symbol = request.form.get("symbol")
        buys_shares = db.execute(
            "SELECT * FROM buysinfo WHERE user_id = ? AND symbol = ?", user_id, share_symbol)
        if not shares_unit or int(shares_unit) < 1 or int(buys_shares[0]["shares"]) < int(shares_unit):
            return apology("invalid shares", 400)

        symbols = []
        for data in buys:
            symbols.append(data["symbol"])

        if not share_symbol in symbols:
            return apology("invaid stock", 400)

        stock_info = lookup(share_symbol)
        stock_sql = db.execute(
            "SELECT * FROM buysinfo WHERE symbol = ? AND user_id = ?", share_symbol, user_id)
        if stock_sql[0]["shares"] != 0:
            total = float(shares_unit) * float(stock_info["price"])
            stock_total = float(re.sub("[$,,]", "", stock_sql[0]["total"]))
            db.execute("UPDATE buysinfo SET shares = shares - ?, total =  ? WHERE symbol = ? AND user_id = ?",
                       shares_unit, usd(stock_total - total), share_symbol, user_id)
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", total, user_id)
            up_stock_sql = db.execute(
                "SELECT shares FROM buysinfo WHERE symbol = ? AND user_id = ?", share_symbol, user_id)
            if up_stock_sql[0]["shares"] == 0:
                db.execute("DELETE FROM buysinfo WHERE user_id = ? AND symbol = ?",
                           user_id, share_symbol)
            db.execute("INSERT INTO History (user_id,symbol,shares,price) VALUES (?,?,-?,?)",
                       user_id, share_symbol, shares_unit, usd(stock_info["price"]))
            return redirect("/")
        else:
            return apology("stock not found", 400)

    return render_template("sell.html", symbol=buys)
