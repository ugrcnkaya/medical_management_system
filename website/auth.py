from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Patient
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        patient = Patient.query.filter_by(E_Mail=email).first()

        if patient:
            if check_password_hash(patient.Password, password):
                flash('logged in successfully: '+ patient.E_Mail, category="success")
                login_user(patient, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Error logging in', category="error")

            # text = argument to send towards the template
    return render_template("login.html", patient= current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods= ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        patient = Patient.query.filter_by(E_Mail=email).first()
        if patient:
            flash('Email already exists.', category='error')

        if len(email)  < 4:
            flash('E-Mail must be greater than 3 characters.', category='error')

        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')

        elif password1 != password2:
            flash('Passwords don\'t match', category='error')

        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')

        else:
            new_patient = Patient(E_Mail=email, Name=firstName, Password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_patient)
            db.session.commit()
            flash('User is created.', category='success')
            login_user(new_patient, remember=True)
            return redirect(url_for('views.home')) ##blueprint


    return render_template("sign_up.html", patient=current_user)


