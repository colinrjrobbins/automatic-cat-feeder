from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/testLogin', methods=['POST'])
def testLogin():
    return 'success'

@auth.route('/logout')
def logout():
    return 'Logout'