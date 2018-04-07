from flask import Flask, request, redirect
import os
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/')
def index():
    return jinja_env.get_template('index.html').render()

@app.route('/', methods=['POST'])
def form_entry():
    pattern = re.compile('.{3,20}')

    username_err = ""
    password_err = ""
    confirm_password_err = ""
    email_err = ""

    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    email = request.form['email']

    if not pattern.match(username):
        username_err = "Username must contain 3-20 characters."
    elif ' ' in username:
        username_err = "Username cannot contain any spaces."

    if not pattern.match(password):
        password_err = "Password must contain 3-20 characters."
    elif ' ' in password:
        password_err = "Password cannot contain any spaces."

    if not pattern.match(confirm_password):
        confirm_password_err = "Password must contain 3-20 characters."
    elif ' ' in confirm_password:
        confirm_password_err = "Password cannot contain any spaces."
    elif password != confirm_password:
        confirm_password_err = "Passwords do not match."

    if email:
        if not pattern.match(confirm_password):
            email_err = "Email must contain 3-20 characters."
        elif ' ' in confirm_password:
            email_err = "Email cannot contain any spaces."
        elif not ('@' in email and '.' in email):
            email_err = "Email must contain a single @ and a single ."
            
    if not (username_err and password_err and confirm_password_err and email_err):
        return jinja_env.get_template('welcome_page.html').render(name=username)
    else:
        return jinja_env.get_template('index.html').render(
            username=username,
            email=email,
            username_err=username_err, 
            password_err=password_err, 
            confirm_password_err=confirm_password_err,
            email_err=email_err
        )

app.run()