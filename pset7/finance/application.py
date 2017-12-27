from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from helpers import *
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

#from time import gmtime, strftime
"""
TODO:
Register
1. Check for duplicate registrations                                            -done
2. Upon registration -> create table for user                                   -done
3. Take user to index                                                           -done

Index
1. Render SQL table of user                                                     -done
2. dynamically select data from user portfolio                                  -done
3. Display Latest Prices and value of stake for each stock                      -done
Quote
1.Allow user to submit Symbol                                                   -done
2.If symbol is of valid format, query data from Yahoo finance lookup(symbol)    -done
3.Render data on quoted, call USD                                               -done


Buy
1. Allow user to submit symbol and shares                                       -done
2. If symbol is valid and shares are +ve and within capability of user,         -done
    purchase shares, update table number of shares, cash etc.
3. add to history symbols shares price timestamp                                -done   PS: timestamp is a string in DB

Sell
1. List box with user shares                                                    -done
2. Number of shares and validity                                                -done
3. Update table cash, shares and delete rows if necessary                       -done
4. add to history symbols shares price timestamp                                -done
5. Dynamic list of options in selection box                                     -done

History
1.Render history table                                                          -done

Personal Touch
Add/Remove Cash                                                                 -done
Add P/L and option to add

ISSUES!!
1. Bad symbols lead to servor error in quote                                    -resolved  --symbol check logic was bad
2. Buy leads to servor error                                                    -resolved  --request method was wrongly implemented
3. Index.html is bad                                                            -resolved  --index.html of pset6 was being worked on instead of pset7. WTAF
4. Buy is not interacting with finance.db                                       -resolved  --buy.html form submission was routing to quote :(
5. Buy has sanity check issues
    Int conversion of ''                                                        -resolved  --raises valueerror exception -apologiese with "enter positive integer"

6. Sell stake total might be shifty                                             -ignore for now
7. Sell html symbol submission                                                  -resolved  --key:value were both being submitted and not just value
8. Sell no value leads to error                                                 -resolved  --None type was being passed to lookup - Bad.
9.password and confrim password mismatch error text to be changed               -NRN
10.call USD function for each currency field                                    -resolved  --looped and called
Tests:

1.Register
    Duplicate registration                                                      -Good
    No passowrd                                                                 -Good
    Passwords don't match                                                       -Good
    sql injection?                                                              -NRN

2.Log in
    Non existent userid                                                         -Good
    bad password                                                                -Good
    SQL                                                                         -NRN

3. Quote
    No entry                                                                    -Good
    Non-existent                                                                -Good
    lower-case valid symbols                                                    -Good

4. Buy
    Raises no value                                                             -Good
    Raises string non positive-integer                                          -Good

5.Sell
    Only Owned Stake symbols displayed                                          -True
    No action submit does not throw error                                       -True
    text entry                                                                  -Good
6.History                                                                       --All good no possible liabilities

7.Loadmoney
    Can't withdraw more than balance                                            -Good
    No entry submission                                                         -Good

"""

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():
    #get username of current session
    usernames =  db.execute("SELECT * FROM users WHERE id = :uid", uid=session["user_id"])
    username =usernames[0]["username"]
    portfolio = db.execute("SELECT * FROM :username",username=username)

    #update prices to latest
    #TODO
    symbols_shares = db.execute("SELECT Symbol,Shares FROM :username WHERE Symbol !='CASH' ",username=username)
    for i in symbols_shares:
        symbol=i["Symbol"]
        share=i["Shares"]
        data=lookup(symbol)
        newprice=data["price"]
        newcash=newprice*share
        db.execute("UPDATE :username SET Price = :price, TOTAL = :total WHERE Symbol = :symbol",username=username,price=newprice,total=newcash,symbol=symbol)

    #format prices as USD
    for i in range(len(portfolio)):
        portfolio[i]["Price"]=usd(portfolio[i]["Price"])
        portfolio[i]["TOTAL"]=usd(portfolio[i]["TOTAL"])
    return render_template("index.html", range=range(len(portfolio)),data=portfolio )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    if request.method=="POST":
        #get number of shares
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Enter positive integer value")
        #get symbol
        symbol = request.form.get("symbol")

        #check if symbol exists
        if symbol==None or lookup(symbol) == None:
            apology("Symbol not recognized")

        #get username of current session
        usernames =  db.execute("SELECT * FROM users WHERE id = :uid", uid=session["user_id"])
        username =usernames[0]["username"]
        row0 = db.execute("SELECT * FROM :username WHERE Symbol = 'CASH'",username=username)

        #query data from yahoo and store as fields
        data = lookup(symbol)
        price = data["price"]
        name = data["name"]
        symbol = data["symbol"]

        # Symbol Name Shares Price Total
        cash = row0[0]["Price"]

        if shares>0 and cash>shares*price:
            totalpaid = shares*price
            #insert record into portfolio
            if db.execute("SELECT Symbol FROM :username WHERE Symbol=:symbol",username=username, symbol=symbol):
                current = db.execute("SELECT Shares,TOTAL FROM :username WHERE Symbol = :symbol",username=username , symbol=symbol)
                currshares = current[0]["Shares"]
                currtotal = current[0]["TOTAL"]
                newshares = currshares+shares
                newprice = price

                newtotal = currtotal + totalpaid
                db.execute("UPDATE :username SET Shares=:shares, Price=:price, TOTAL =:total WHERE Symbol = :symbol",username=username, shares=newshares,price=newprice,total=newtotal,symbol=symbol)
            else:
                db.execute("INSERT INTO :username (Symbol,Name,Shares,Price,TOTAL) VALUES (:symbol,:name,:shares,:price,:total) ",username=username,symbol=symbol,name=name,shares=shares,price=price,total=totalpaid)

            pricecash = cash-totalpaid
            totalcash = pricecash

            #update CASH reserve in user portfolio
            db.execute("UPDATE :username SET Price = :price, TOTAL = :total WHERE Symbol = 'CASH'",username=username,price=pricecash,total=totalcash)

            tableh = username+'_history'
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #insert record into history table
            db.execute("INSERT INTO :table (Symbol,Shares,Price,TIME) VALUES(:symbol,:shares,:price,:time) ",table=tableh,symbol=symbol,shares=shares,price=price,time=time)


            #redirect to index with updated portfolio once bought
            return redirect(url_for("index"))

        else:
            return apology("too few or too many shares")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    #get username of current session
    usernames =  db.execute("SELECT * FROM users WHERE id = :uid", uid=session["user_id"])
    username =usernames[0]["username"]
    userhistory = username+'_history'
    history = db.execute("SELECT * FROM :table",table=userhistory)
    for i in range(len(history)):
        history[i]["Price"]=usd(history[i]["Price"])

    return render_template("history.html",range=range(len(history)),data=history)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    #If page is accessed through POST
    if request.method == "POST":

        #assign submitted symbol to symbol
        symbol = request.form.get("symbol")


        #check if symbol is in standard format
        if(lookup(symbol)==None):
            #throw apology if symbol not recognised
            return apology("Symbol not recognized")

        else:
            #store data as dictionary
            data=lookup(symbol)
            stock_name = data["name"]
            stock_price = data["price"]
            stock_symbol = data["symbol"]

            #render quoted and fill corresponding values
            return render_template("quoted.html",name=stock_name,price=usd(stock_price),symbol=stock_symbol)




    #if page is not accessed by POST render page
    else:
        return render_template("quote.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure user enters a Username
        if not request.form.get("username"):
            return apology("must provide username")

        #   ensure user enters a new username
        if db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            return apology("username already exists")

        # ensure password is entered
        elif not request.form.get("password"):
            return apology("must provide password")

        # ensure password is confirmed correctly
        elif not request.form.get("confirm_password") or request.form.get("confirm_password")!=request.form.get("password") :
            return apology("please confirm correct password")

        hash1 = pwd_context.hash(request.form.get("password"))

        #insert values into database
        username=request.form.get("username")
        rows = db.execute("INSERT INTO users (username,hash) VALUES(:username,:hash)",username=username,hash=hash1)

        #create table for user portfolio upon registration
        db.execute("CREATE TABLE :username (Symbol VARCHAR(5),Name VARCHAR(20),Shares INT,Price DECIMAL(15,3),TOTAL DECIMAL(15,3), PRIMARY KEY(Symbol))",username=username)

        #insert record with cash 10000
        db.execute("INSERT INTO :username (Symbol,Price,TOTAL) VALUES('CASH',10000,10000)",username = username)

        tablename=username+'_history'
        #create table for user history upon registration
        db.execute("CREATE TABLE :table (Symbol VARCHAR(5), Shares INT, Price DECIMAL(15,3),TIME VARCHAR(21), PRIMARY KEY(TIME))",table=tablename)

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")




@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    #get username of current session
    usernames =  db.execute("SELECT * FROM users WHERE id = :uid", uid=session["user_id"])
    username =usernames[0]["username"]

    #get list of symbols
    symbols = db.execute("SELECT Symbol FROM :username WHERE Symbol !='CASH'", username=username)
    if request.method =="POST":
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Enter positive integer value")
        #get symbol
        symbol = request.form.get("symbol")

        #check if symbol exists
        if symbol==None or lookup(symbol) == None:
            apology("Symbol not recognized")

        #query current cash reserve for user
        row0 = db.execute("SELECT * FROM :username WHERE Symbol = 'CASH'",username=username)
        totalcash = row0[0]["TOTAL"]


        if(request.form.get("shares"))==None:
            return apology("Don't want to sell?")


        if symbol==None or lookup(symbol) == None:
            return apology("Choose a valid symbol")
        #query current stake in company
        current = db.execute("SELECT Shares,Price,TOTAL FROM :username WHERE Symbol = :symbol",username=username , symbol=symbol)
        currshares = current[0]["Shares"]
        currtotal = current[0]["TOTAL"]
        currprice = current[0]["Price"]

        #ensure shares are not negative and within capability
        if shares>currshares:
            return apology("Selling more than you Own? Nah")
        elif shares<0:
            return apology("Might as well buy shares!")


        #query data from yahoo and store as fields
        data = lookup(symbol)
        price = data["price"]
        name = data["name"]
        symbol = data["symbol"]

        #sell shares at latest price, update cash reserve and stake in company in user table
        totalreceived = shares*price
        pricecash = totalcash+totalreceived
        sharetotal = currtotal - currprice*shares
        newshares = currshares - shares

        #update CASH reserve in user portfolio
        db.execute("UPDATE :username SET Price = :price, TOTAL = :total WHERE Symbol = 'CASH'",username=username,price=pricecash,total=pricecash)

        #update stake in company, delete if 0
        if shares==currshares:
            db.execute("DELETE FROM :username WHERE Symbol=:symbol",username=username,symbol=symbol)
        elif shares<currshares:
            db.execute("UPDATE :username SET Shares=:shares, Price=:price, TOTAL =:total WHERE Symbol = :symbol",username=username, shares=newshares,price=price,total=sharetotal,symbol=symbol)
        #username_history, get current time
        tableh = username+'_history'
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        #insert record into history table
        db.execute("INSERT INTO :table (Symbol,Shares,Price,TIME) VALUES(:symbol,:shares,:price,:time) ",table=tableh,symbol=symbol,shares=-shares,price=price,time=time)


        return redirect(url_for("index"))
    else:
        return render_template("sell.html", range= range(len(symbols)),symbols=symbols)



@app.route("/transact", methods=["GET", "POST"])
@login_required
def transact():
    """Add/remove CASH to/from portfolio"""
    if request.method =="POST":
        #get username of current session
        usernames =  db.execute("SELECT * FROM users WHERE id = :uid", uid=session["user_id"])
        username =usernames[0]["username"]

        #get cash
        total = db.execute("SELECT TOTAL FROM :username WHERE Symbol ='CASH'", username=username)
        currcash = total[0]["TOTAL"]

        amount=request.form.get("amount")
        if amount==None:
            return apology("Nothing to transact")
        try:
            amount=float(amount)
        except ValueError:
            return apology("Enter Signed floating value")

        if amount<0 and amount*(-1)>currcash:
            return apology("WITHDRAWAL EXCEEDS BALANCE!")

        newcash = currcash+amount
        db.execute("UPDATE :username SET Price = :price, TOTAL = :total WHERE Symbol = 'CASH'",username=username,price=newcash,total=newcash)

        return redirect(url_for("index"))
    else:
        return render_template("transact.html")

