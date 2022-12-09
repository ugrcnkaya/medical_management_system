##routes for website
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from . import db
import json
from .models import Patient, Appointment, Specification, HospitalStaff
from .auth import check_session
from sqlalchemy import text



views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if check_session():
        patientID = session["Patient_ID"]
        user = Patient.query.filter_by(Patient_ID=patientID).first()
        return render_template("profile.html", patient=user)
    else:
        return redirect(url_for('auth.login'))

@views.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if check_session():
        patientID = session["Patient_ID"]
        user = Patient.query.filter_by(Patient_ID=patientID).first()

        ## pass appointments from Appointments View
        sql = text("select * from V_Appointments WHERE Patient_ID = " + str(patientID))
        appointments = db.engine.execute(sql)

        ## create appointment part : required objects -> pass
        specifications = Specification.query.all()

        return render_template("appointments.html", patient=user, appointments=appointments, specifications = specifications)
    else:
        return redirect(url_for('auth.login'))


@views.route('/cancel-appointment', methods = ['POST'])
def cancel_appointment():
    if check_session():
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
    if check_session():
        if request.args.get("Specification_ID") != None:
            spec_id = request.args.get("Specification_ID")
            staffs = HospitalStaff.query.filter_by(Specification_ID = spec_id).all()
            all_staff = [{'id': staf_members.Staff_ID, 'name': staf_members.Name + " " + staf_members.Surname} for staf_members in staffs]
        return jsonify(all_staff)
    else:
        return redirect(url_for('auth.login'))



