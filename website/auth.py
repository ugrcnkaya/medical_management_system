from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Patient, HospitalStaff
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Patient":
        return redirect(url_for('views.home'))
    elif check_session()["Logged_In"] != False and check_session()["Role"] == "1":
        #doctor route redirect- > doctor profile
        print("here")
        return redirect(url_for('views.home'))

    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')
        patient = Patient.query.filter_by(E_Mail=email).first()
        staff = HospitalStaff.query.filter_by(EMail=email).first()
        if staff:
            if check_password_hash(staff.Password, password):

                session.permanent = True
                session['Staff_ID'] = staff.Staff_ID
                session['Staff_Role'] = staff.Role
                print("Hospital staff login successfull. ")
                return redirect(url_for('views.staff'))

            else:
                flash('Error logging in', category="error")

        elif patient:
            if check_password_hash(patient.Password, password):
                flash('logged in successfully: '+ patient.E_Mail, category="success")
                print("success")
                session.permanent = True
                session['Patient_ID'] = patient.Patient_ID
                return redirect(url_for('views.home'))
            else:
                print("fail")
                flash('Error logging in', category="error")

            # text = argument to send towards the template
    return render_template("login.html")


def user_role(email, password):
    staff = HospitalStaff.query.filter_by(E_Mail=email).first()
    if staff:
        if check_password_hash(staff.Password, password):
            print("Hospital staff login successfull. ")


@auth.route('/logout')
def logout():
    session.pop("Patient_ID", None)
    session.pop("Staff_ID", None)
    session.pop("Role", None)
    return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods= ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        phone = request.form.get('phone')
        birthDate = request.form.get('birthdate')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        patient = Patient.query.filter_by(E_Mail=email).first()
        if patient:
            flash('Email already exists.', category='error')
        elif len(email)  < 4:
            flash('E-Mail must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_patient = Patient(E_Mail=email,
                                  Name=firstName,
                                  Surname=lastName,
                                  Birthdate=birthDate,
                                  Password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_patient)
            db.session.commit()
            session['Patient_ID'] = new_patient.Patient_ID
            flash('User is created.', category='success')
            return redirect(url_for('views.home')) ##blueprint


    return render_template("sign_up.html")


def check_session():
    if session.get("Patient_ID"):
        return {
            "Logged_In" : True,
            "Role" : "Patient"
        }
    elif session.get("Staff_ID") and session.get("Staff_Role"):
        if  session.get("Staff_Role") == 1:
            return {"Logged_In": True, "Role": "1"}
        else:
            return {"Logged_In": True, "Role": str(session.get("Staff_Role"))}
    else:
        return {"Logged_In": False, "Role": None}

