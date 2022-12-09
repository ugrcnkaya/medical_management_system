##routes for website
import sqlalchemy
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from . import db
import json
from .models import Patient, Appointment, Specification, HospitalStaff, AvailabilitySchedule,SystemConfig
from .auth import check_session
from sqlalchemy import text
from sqlalchemy.sql import func
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Patient":
        patientID = session["Patient_ID"]
        user = Patient.query.filter_by(Patient_ID=patientID).first()
        return render_template("profile.html", patient=user)
    elif check_session()["Logged_In"] != False and check_session()["Role"] == "1":
        doctorID = session["Staff_ID"]
        doctor = HospitalStaff.query.filter_by(Staff_ID = doctorID).first()
        return render_template("staff_profile.html", staff=doctor, patient= None)
    elif check_session()["Logged_In"] != False and check_session()["Role"] == "Admin":
        email = session["Admin_E-Mail"]
        system_admin = SystemConfig.query.filter_by(Admin_E_Mail=email).first()
        return render_template("admin.html", staff=None, patient=None, admin=system_admin)
    else:
        return redirect(url_for('auth.login'))

##staff route
@views.route('/staff', methods=['GET', 'POST'])
def staff():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Patient":
        #patientID = session["Patient_ID"]
       # user = Patient.query.filter_by(Patient_ID=patientID).first()
        return redirect(url_for('views.home'))
    elif check_session()["Logged_In"] != False and check_session()["Role"] == "1":
        doctorID = session["Staff_ID"]
        doctor = HospitalStaff.query.filter_by(Staff_ID = doctorID).first()
        return render_template("staff_profile.html", staff=doctor, patient= None)
    else:
        return redirect(url_for('views.home'))


#admin

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Admin":

        return render_template("admin.html", staff=None, patient=None, admin=True)
    else:
        return redirect(url_for('auth.login'))






##appointment views-controls

@views.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Patient" and request.method != 'POST':
        patientID = session["Patient_ID"]
        user = Patient.query.filter_by(Patient_ID=patientID).first()

        ## pass appointments from Appointments View
        sql = text("select * from V_Appointments WHERE Patient_ID = " + str(patientID))
        appointments = db.engine.execute(sql)

        ## create appointment part : required objects -> pass
        specifications = Specification.query.all()

        return render_template("appointments.html", patient=user, appointments=appointments, specifications = specifications)

    elif request.method == 'POST':
        schedule_id = request.form.get('date')

        patient_id = session["Patient_ID"]
        type = "Visit"

        new_appointment = Appointment(Schedule_ID = schedule_id, Patient_ID = patient_id, Type= type, Status = 1)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment is set!', category='success')
        return  redirect(url_for('views.appointments'))



    else:
        return redirect(url_for('auth.login'))


@views.route('/cancel-appointment', methods = ['POST'])
def cancel_appointment():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Patient":
        appointment = json.loads(request.data)
        appointmentID = appointment['Appointment_ID']

        #get the appointment info first
        appointment = Appointment.query.filter_by(Appointment_ID=appointmentID).first()
        # check if this appointment is actually current patient's, (they can change javascript post id)
        if(appointment.Patient_ID == session["Patient_ID"]):
            #yes
            appointment.Status = 0
            sql = text("UPDATE Appointments SET Status = 0 WHERE Appointment_ID = "+ str(appointment.Appointment_ID))
            db.engine.execute(sql)

            print("true")
        else:
            #he or she trying to hack us :)
            print("false")


    else:
        return redirect(url_for('auth.login'))


@views.route('/list_appointments', methods = ['GET'])
def list_appointments():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Patient":
        if request.args.get("Specification_ID") != None:
            spec_id = request.args.get("Specification_ID")
            staffs = HospitalStaff.query.filter_by(Specification_ID = spec_id).all()
            all_staff = [{'id': staf_members.Staff_ID, 'name': staf_members.Name + " " + staf_members.Surname} for staf_members in staffs]
            return jsonify(all_staff)

        if request.args.get("Doctor_ID") != None:
            doctor_id = request.args.get("Doctor_ID")
            sql = text("SELECT 	Schedule_ID,CONCAT(CONCAT(DATE_FORMAT(Schedule_Date, '%d/%m/%Y'), ' ', DATE_FORMAT(Start_Time, '%H:%i')), ' - ', DATE_FORMAT(End_Time, '%H:%i')) as Slot FROM V_Available_Slots Where Doctor_ID = " + str(doctor_id))
            available_slots = db.engine.execute(sql)
            all_slots = [{'id' :str(slot.Schedule_ID), 'date':slot.Slot} for slot in available_slots]
            return jsonify(all_slots)
    else:
        return redirect(url_for('auth.login'))





