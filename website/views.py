##routes for website
import sqlalchemy
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, jsonify
from . import db
import json
from .models import Patient, Appointment, Specification, HospitalStaff, AvailabilitySchedule,SystemConfig,TimeSlot, Room
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
        return render_template("profile.html", patient=user, role="patient")
    elif check_session()["Logged_In"] != False and check_session()["Role"] == "1":
        doctorID = session["Staff_ID"]
        doctor = HospitalStaff.query.filter_by(Staff_ID = doctorID).first()
        return render_template("staff_profile.html", staff=doctor, role = "staff")
    elif check_session()["Logged_In"] != False and check_session()["Role"] == "Admin":
        email = session["Admin_E-Mail"]
        system_admin = SystemConfig.query.filter_by(Admin_E_Mail=email).first()
        return render_template("admin.html", role="admin", admin=system_admin)
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
        return render_template("staff_profile.html", role="staff", staff=doctor, patient= None)
    else:
        return redirect(url_for('views.home'))



#delete schedule
@views.route('/delete-schedule', methods = ['POST'])
def delete_schedule():
    if request.method == "POST" and check_session()["Logged_In"] != False and check_session()["Role"] != "Patient":
        # delete schedule
        schedule_id = json.loads(request.data)
        schedule_id = schedule_id['Schedule_ID']

        schedule = AvailabilitySchedule.query.filter_by(Schedule_ID = schedule_id).first()
        if schedule:
            print(schedule.Schedule_ID)
            schedule.Status = 0
            db.session.commit()
    return redirect(url_for('views.schedule'))


#availability_schedule page
@views.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if check_session()["Logged_In"] != False and check_session()["Role"] != "Patient" and request.method != "POST":
        doctorID = session["Staff_ID"]
        doctor = HospitalStaff.query.filter_by(Staff_ID = doctorID).first()

        #only list the availables not blocked by an appointment so no conflict.
        schedules   = ""
        sql = text("""
        SELECT
                        	a.Schedule_ID ,
                        a.Schedule_Date,
                        c.Start_Time,
                        c.End_Time,
                        a.Slot_ID,
                        a.Staff_ID,
                        
                        b.Room,
                        b.Building
                    from Availability_Schedule a
                    JOIN
                        Rooms b ON a.Room_ID  = b.Room_ID  
                    JOIN 
                        Time_Slots c ON a.Slot_ID = c.Slot_ID 
            WHERE Status != 0 AND  Schedule_ID NOT IN (SELECT Schedule_ID from V_Appointments WHERE Status = 1 ) AND Staff_ID = """
                    + str(doctorID))
        schedules = db.engine.execute(sql)

        sql = text("select * from V_Appointments WHERE Staff_ID = " + str(doctorID))
        appointments = db.engine.execute(sql)
        return render_template("schedule.html", staff=doctor, role="staff", appointments=appointments, schedules=schedules)
    else:
        return redirect(url_for('views.home'))


#create availability slot
@views.route('/insert_availability', methods=['POST'])
def insert_availability():
    if check_session()["Logged_In"] != False and check_session()["Role"] != "Patient":
       if request.method == 'POST':
           #data validation required
        date = request.form.get('date')
        date = (datetime.strptime(date,"%d/%m/%Y"))
        time_slot = request.form.get('Time_Slots')
        room_id = request.form.get('room')
        staff = session.get("Staff_ID")
        ## insert it into database
        new_availability = AvailabilitySchedule(Schedule_Date=date, Slot_ID = time_slot, Staff_ID = staff,Room_ID = room_id, Status = 1)
        db.session.add(new_availability)
        db.session.commit()
        flash('Schedule is set!', category='success')
        return redirect(url_for('views.schedule'))
    else:
        return redirect(url_for('views.home'))





#admin

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    if check_session()["Logged_In"] != False and check_session()["Role"] == "Admin":

        return render_template("admin.html", role="admin", admin=True)
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


        specifications = Specification.query.all()

        return render_template("appointments.html", role = "patient", patient=user, appointments=appointments, specifications = specifications)

    elif check_session()["Logged_In"] != False and check_session()["Role"] == "Patient" and request.method == 'POST':
        schedule_id = request.form.get('date')

        patient_id = session["Patient_ID"]
        type = "Visit"

        new_appointment = Appointment(Schedule_ID = schedule_id, Patient_ID = patient_id, Type= type, Status = 1)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment is set!', category='success')
        return  redirect(url_for('views.appointments'))

    elif check_session()["Logged_In"] != False and check_session()["Role"] != "Patient" and request.method != 'POST':
        #("staff or admin user visiting appointments view")
        staff = session['Staff_ID']
        sql = text("select * from V_Appointments ")
        appointments = db.engine.execute(sql)
        patients = Patient.query.all()
        specifications = Specification.query.all()
        staff = HospitalStaff.query.filter_by(Staff_ID = staff).first()

        return render_template("staff_appointments.html", role="staff", patient= patients, appointments=appointments, specifications = specifications)
    elif check_session()["Logged_In"] != False and check_session()["Role"] != "Patient" and request.method == 'POST':
        patient_id = request.form.get('patient')
        schedule_id = request.form.get('date')
        type = "Visit"

        new_appointment = Appointment(Schedule_ID=schedule_id, Patient_ID=patient_id, Type=type, Status=1)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment is set!', category='success')
        return redirect(url_for('views.appointments'))
    else:
        return redirect(url_for('auth.login'))


@views.route('/cancel-appointment', methods = ['POST'])
def cancel_appointment():
    if check_session()["Logged_In"] != False:
        appointment = json.loads(request.data)
        appointmentID = appointment['Appointment_ID']

        #get the appointment info first
        appointment = Appointment.query.filter_by(Appointment_ID=appointmentID).first()
        # check if this appointment is actually current patient's, (they can change javascript post id)
        if check_session()["Role"] == "Patient":
            print("works here1")
            if(appointment.Patient_ID == session["Patient_ID"]):
                #yes
                appointment.Status = 0
                sql = text("UPDATE Appointments SET Status = 0 WHERE Appointment_ID = "+ str(appointment.Appointment_ID))

                db.engine.execute(sql)


        else:
            print("works here2")
            appointment.Status = 0
            sql = text("UPDATE Appointments SET Status = 0 WHERE Appointment_ID = " + str(appointment.Appointment_ID))
            print("here")
            db.engine.execute(sql)




    else:
        print("works here3")
        return redirect(url_for('auth.login'))



# JSON Call - List Appointments Available
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
    elif check_session()["Logged_In"] != False and check_session()["Role"] != "Patient":
        if request.args.get("Patient_ID") != None:
            patient_id = request.args.get("Patient_ID")

            #return active appointments of the chosen patient

            sql = text("select * from V_Appointments WHERE Status = 1 and  Patient_ID = " + str(patient_id))
            all_appointments = db.engine.execute(sql)
            all_staff = [{'id': appointment.Appointment_ID, 'staff':appointment.Staff_Name, 'date': appointment.Schedule_Date, 'start_time' : str(appointment.Start_Time), 'end_time' : str(appointment.End_Time), 'specification': appointment.Specification } for appointment in all_appointments]
            return jsonify(all_staff)

        if request.args.get("Doctor_ID") != None:
            doctor_id = request.args.get("Doctor_ID")
            sql = text(
                "SELECT 	Schedule_ID,CONCAT(CONCAT(DATE_FORMAT(Schedule_Date, '%d/%m/%Y'), ' ', DATE_FORMAT(Start_Time, '%H:%i')), ' - ', DATE_FORMAT(End_Time, '%H:%i')) as Slot FROM V_Available_Slots Where Doctor_ID = " + str(
                    doctor_id))
            available_slots = db.engine.execute(sql)
            all_slots = [{'id': str(slot.Schedule_ID), 'date': slot.Slot} for slot in available_slots]
            return jsonify(all_slots)


        if request.args.get("Specification_ID") != None:
            spec_id = request.args.get("Specification_ID")
            staffs = HospitalStaff.query.filter_by(Specification_ID = spec_id).all()
            all_staff = [{'id': staf_members.Staff_ID, 'name': staf_members.Name + " " + staf_members.Surname} for staf_members in staffs]
            return jsonify(all_staff)

    else:
        return redirect(url_for('auth.login'))


@views.route('/list_time_slots', methods = ['GET'])
def list_time_slots():
    if check_session()["Logged_In"] != False:

        time_slots = TimeSlot.query.all()

        all_slots = [{'id': str(slot.Slot_ID), 'time': str(slot.Start_Time.strftime('%H:%M')) + " - " + str(slot.End_Time.strftime('%H:%M')) } for slot in time_slots]
        return jsonify(all_slots)

    else:
        return redirect(url_for('auth.login'))


@views.route('/list_rooms', methods = ['GET'])
def list_rooms():
    if check_session()["Logged_In"] != False:
        rooms = Room.query.all()
        all_slots = [{'id': str(slot.Room_ID), 'desc': "Type: (" + slot.Type + ") (Building: " + slot.Building + ") Room: (" + slot.Room + ")"} for slot in rooms]
        return jsonify(all_slots)
    else:
        return redirect(url_for('auth.login'))



@views.route('/list_patients', methods = ['GET'])
def list_patients():
    if check_session()["Logged_In"] == True and check_session()["Role"] != "Patient":
        patients = Patient.query.all()
        all_patients = [{'id': str(patient.Patient_ID), 'desc': "" + patient.Name + " " + patient.Surname + "  -> " + str(datetime.strftime(patient.Birthdate, "%d%/%m%/%Y") ) } for patient in patients]
        return jsonify(all_patients)
    else:
        return redirect(url_for('auth.login'))







