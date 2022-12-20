import re
from datetime import datetime, date

from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Patient, HospitalStaff,SystemConfig
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
auth = Blueprint('auth', __name__)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^\d{11}$')

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        if check_session()["Logged_In"] == True:
            return redirect(url_for('views.home'))

        if request.method == 'POST':

            email = request.form.get('email')
            password = request.form.get('password')
            patient = Patient.query.filter_by(E_Mail=email).first()
            staff = HospitalStaff.query.filter_by(EMail=email).first()
            system_admin = SystemConfig.query.filter_by(Admin_E_Mail = email).first()

            if system_admin:
                if check_password_hash(system_admin.Admin_Password, password):
                    session.permanent = True
                    print("admin")
                    session['Admin_E-Mail'] = system_admin.Admin_E_Mail
                    print("Admin login successfull.")
                    return redirect(url_for('views.admin'))

            if staff:
                if check_password_hash(staff.Password, password):

                    session.permanent = True
                    print("staff")
                    session['Staff_ID'] = staff.Staff_ID
                    session['Staff_Role'] = staff.Role
                    print("Hospital staff login successfull. ")
                    return redirect(url_for('views.staff'))

                else:
                    flash('Error logging in', category="error")

            elif patient:
                if check_password_hash(patient.Password, password):
                    flash('logged in successfully: '+ patient.E_Mail, category="success")
                    session.permanent = True
                    print("patient")
                    session['Patient_ID'] = patient.Patient_ID
                    return redirect(url_for('views.home'))
                else:
                    print("fail")
                    flash('Error logging in', category="error")


            elif not EMAIL_REGEX.match('email'):
                flash('Invalid Email address!', category='error')

            else:
                flash('Here', category="error")
                # text = argument to send towards the template
    except:
        flash('Login Error', category="error")

    else:
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
    session.pop("Admin_E-Mail", None)

    return redirect(url_for('auth.login'))

def dateDiff(date1, date2, resultType, ):
    diff = date1 - date2
    if resultType == "years":
        return diff.days//365
    elif resultType == "days":
        return diff.days

@auth.route('/sign_up', methods= ['GET', 'POST'])
def sign_up():
    try:
        if check_session()["Logged_In"] == True:
            return redirect(url_for('views.home'))

        if request.method == 'POST':
            email = request.form.get('email')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            phone = request.form.get('phone')
            birthDate = request.form.get('birthdate')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            patient = Patient.query.filter_by(E_Mail=email).first()
            result = dateDiff(date.today(), datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date(),"years")
            if patient:
                flash('Email already exists.', category='error')
            elif not EMAIL_REGEX.match(email):
                flash('Invalid Email address!', category='error')
            elif not PHONE_REGEX.match(phone):
                flash('Phone should be 11 digits', category='error')
            elif result < 18:
                flash('You need to be at least 18 years old to register', category='error')
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


    except:
        flash('sign up error', category='error')

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
    elif session.get("Admin_E-Mail"):
        return {"Logged_In": True, "Role": "Admin"}
    else:
        return {"Logged_In": False, "Role": None}

