from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

import hash_password
from data_base import Database
from models import UserLogin

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('signIn.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = Database().check_user_exists(email=email)
    print(user, email)

    if user is None:
        print("Неверный логин или пароль")
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    elif user['email'] == email:
        print("Успешно")
        # login_user = UserLogin().create(user)
        # login_user(login_user, remember=remember)
        return render_template('profile.html', email=email)


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@auth.route('/signup')
def signup():
    return render_template('signUp.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    user = Database().check_user_exists(email=email)
    if user is None:
        new_password = hash_password.hash_password(password)
        Database().add_new_user(username=username, email=email, password=new_password)
        return redirect(url_for('auth.login'))
    else :
        print("Такой аккаунт уже существует")
        return redirect(url_for('auth.signup'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
