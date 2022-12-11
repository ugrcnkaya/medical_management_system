##routes for website
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Patient
from . import db
import json
from .models import Patient
from .models import Room,RoomBooking
from .auth import check_session
from sqlalchemy import select,text

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if check_session():
        patientID = session["Patient_ID"]
        user = Patient.query.filter_by(Patient_ID=patientID).first()
        return render_template("profile.html", patient=user)
    else:
        return redirect(url_for('auth.login'))


@views.route('/rooms', methods=['GET', 'POST'])
def showrooms():
    if request.method == 'POST':
        if request.form.get('room_type') == "1":
            rt = 1
        else:
            rt = 0
        new_room = Room(Room = request.form.get('room_name'),
                        Building = request.form.get('building'),
                        Type = request.form.get('room_type'))
        
        db.session.add(new_room)
        db.session.commit()
        rooms = db.session.query(Room).all()
        return render_template('rooms.html',rooms=rooms)


    rooms = db.session.query(Room).all()
    return render_template('rooms.html',rooms=rooms)

@views.route('/deleteroom/<int:id>', methods=['POST'])
def deleteroom(id):
    room_to_delete = db.session.query(Room).get(id)
    db.session.delete(room_to_delete)
    db.session.commit()
    return redirect('/rooms')


@views.route('/roombooking', methods=['GET', 'POST'])
def bookrooms():
    if request.method == 'POST':
        query_for_patient = text("SELECT Patient_ID FROM Patients WHERE Name='"+request.form.get('patientname')+"' and E_Mail='"+request.form.get('patientemail')+"'")
        patient_id = db.session.execute(query_for_patient).fetchone()
        # query_for_room = text("SELECT Room_ID FROM Rooms WHERE Room='"+request.form.get('room_name')+"'")
        # room_id = db.session.execute(query_for_patient).fetchone()
        
        new_admission = RoomBooking(
            Patient_ID = patient_id[0],
            Room_ID = request.form.get('room'),
            Start_Date = request.form.get('arrive'),
            End_Date = request.form.get('depart'),
            Status = 1
            )
        
        db.session.add(new_admission)
        db.session.commit()
        return redirect('/roombooking')
    statement = text("SELECT Room_ID, Room from Rooms where Type = \'Admission Room\' and Room_ID NOT IN (SELECT Room_ID from Room_Bookings)")
    availablerooms = db.session.execute(statement)
    return render_template("roombooking.html",availablerooms=availablerooms)


@views.route('/roomadmissions', methods=['GET', 'POST'])
def showadmissions():
    stmt = text("SELECT Room_Bookings.Booking_ID,Room_Bookings.Patient_ID,Room_Bookings.Room_ID,Room_Bookings.Start_Date,Room_Bookings.End_Date,Room_Bookings.Status,Rooms.Room,Patients.Name FROM Room_Bookings,Rooms,Patients WHERE Room_Bookings.Room_ID = Rooms.Room_ID and Room_Bookings.Patient_ID = Patients.Patient_ID")
    admissions = db.session.execute(stmt)
    return render_template('roomadmissions.html',admissions=admissions)

@views.route('/canceladmission/<int:id>', methods=['POST'])
def canceladmission(id):
    stmt = text("UPDATE Room_Bookings SET Status=0 WHERE Booking_ID='"+str(id)+"'")
    db.session.execute(stmt)
    db.session.commit()
    return redirect('/roomadmissions')
