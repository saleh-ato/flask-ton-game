from flask import Flask, render_template, request, make_response, session, url_for, send_from_directory, jsonify, redirect, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from app import app,db
from models import *

@app.route("/")
def home():
    # print(current_user.id)
    if current_user.is_authenticated:
        balance = Balance.query.filter_by(user_id=current_user.id).first()
    else:
        balance = None  # Default to None for anonymous users

    # Ensure balance_coins is a valid value
    if balance is None:
        balance_coins = 0  # Default value
    else:
        balance_coins = balance.coins  # Access attribute if object exists

    return render_template('main.html', total="25k", balance=balance_coins, user=current_user)


@app.route("/mine")
def mine():
    return render_template('soon.html')

@app.route("/tasks")
def tasks():
    return render_template('soon.html')

# @app.route('/add_number', methods=['POST'])
# def add_number():
#     data = request.json
#     token = data.get('csrf_token')
#     number = data.get('number')

#     # Verify CSRF token
#     if token != session.get('csrf_token'):
#         return jsonify({'error': 'Invalid CSRF token'}), 403

#     # Handle the number (e.g., add to database, update UI, etc.)
#     # For demonstration, just return the received number
#     return jsonify({'status': 'success', 'number_received': number})

# @app.route('/get_csrf_token', methods=['GET'])
# def get_csrf_token():
#     return jsonify({'csrf_token': session['csrf_token']})

@app.route("/verify_wallet", methods=["POST"])
def verify_wallet():
    data = request.json
    wallet_address = data.get("wallet_address")

    # Check if wallet exists in your database
    user = User.query.filter_by(wallet_address=wallet_address).first()
    if user:
        return jsonify({"status": "success", "username": user.username})
    return jsonify({"status": "error", "message": "Wallet not registered"}), 401

@app.route("/wallet", methods=['GET','POST'])
def wallet():
    if current_user.is_authenticated:
        balance=Balance.query.filter_by(user_id=current_user.id).first().coins
        return render_template("wallet.html", auth=True, user=current_user or False, balance=balance)
    if request.method == "POST":
        wallet_address = request.form.get("wallet_address")
        password = request.form.get("password")
        user = User.query.filter_by(wallet_address=wallet_address).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Logged in successfully!", category="success")
            return redirect(url_for("wallet"))
        else:
            flash("Invalid wallet address or password!", category="error")
    return render_template("wallet.html", auth=False)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        wallet_address = request.form.get("wallet_address")
        password = request.form.get("password")

        # Check if wallet address is valid
        if not is_valid_ton_address(wallet_address):
            flash("Invalid wallet address format!", "error")
            return redirect(url_for("register"))

        # Check if wallet is already registered
        if User.query.filter_by(wallet_address=wallet_address).first():
            flash("Wallet already registered!", "error")
            return redirect(url_for("register"))

        # Create new user
        new_user = User(wallet_address=wallet_address)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()  # Commit to assign an ID

        # Create balance entry
        new_balance = Balance(coins=0, user_id=new_user.id)
        db.session.add(new_balance)
        db.session.commit()

        # Flash success message & login user
        flash("Registration successful! Please log in.", "success")
        login_user(new_user)

        return redirect(url_for("wallet"))  # Redirect to wallet page

    return render_template("register.html")

@app.route("/click", methods=["POST"])
def click_coin():
    data = request.json
    user_id = data.get("user_id")
    users=User.query.all()
    print(user_id)
    print(users)
    user=User.query.filter_by(id=user_id).first()
    if user is not None:
        # modified_balance=Balance.query.filter_by(user_id=current_user.id).first()
        modified_balance=Balance.query.filter_by(user_id=user.id).first()
        modified_balance.coins+=1
        print(modified_balance.coins)
        db.session.add(modified_balance)
        db.session.commit()
        print(modified_balance)
        # users[user_id] += 1  # افزایش اعتبار کاربر
        return jsonify({"balance": modified_balance.coins})
    return jsonify({"error": "User not found"}), 404