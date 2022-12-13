# database models
from . import db  # current folder : call db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Column, DECIMAL, Date, DateTime, ForeignKey, Integer, String, TIMESTAMP, Table, Time, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from flask_login import login_user

class Disease(db.Model):
    __tablename__ = 'Diseases'

    Disease_ID = Column(Integer, primary_key=True)
    Disease_Name = Column(String(255))


class Medicine(db.Model):
    __tablename__ = 'Medicines'

    Medicine_ID = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Barcode = Column(String(120))


class Patient(db.Model):
    __tablename__ = 'Patients'

    Patient_ID = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Surname = Column(String(255))
    Birthdate = Column(DateTime)
    Photo = Column(String(255))
    Password = Column(String(255))
    E_Mail = Column(String(255), unique = True)
    Status = Column(INTEGER)


class Role(db.Model):
    __tablename__ = 'Roles'

    Role = Column(Integer, primary_key=True)
    Description = Column(String(255))


class Room(db.Model):
    __tablename__ = 'Rooms'

    Room_ID = Column(Integer, primary_key=True)
    Room = Column(VARCHAR(255))
    Building = Column(String(255))
    Type = Column(String(255))


class Specification(db.Model):
    __tablename__ = 'Specifications'

    Specification_ID = Column(Integer, primary_key=True)
    Title = Column(String(255))


class SystemConfig(db.Model):
    __tablename__ = 'System_Config'

    Hospital_Name = Column(String(255), primary_key=True)
    Hospital_Address = Column(String(255))
    Admin_E_Mail = Column('Admin_E-Mail', String(255))
    Admin_Password = Column(String(255))
    Currency = Column(String(255))


class TimeSlot(db.Model):
    __tablename__ = 'Time_Slots'

    Slot_ID = Column(Integer, primary_key=True)
    Start_Time = Column(Time)
    End_Time = Column(Time)




class HospitalStaff(db.Model):
    __tablename__ = 'Hospital_Staff'

    Staff_ID = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Surname = Column(String(255))
    Specification_ID = Column(ForeignKey('Specifications.Specification_ID'), index=True)
    Role = Column(ForeignKey('Roles.Role'), index=True)
    EMail = Column(String(255))
    Password = Column(String(255))

    Role1 = relationship('Role')
    Specification = relationship('Specification')


class Invoice(db.Model):
    __tablename__ = 'Invoices'

    Invoice_Number = Column(Integer, primary_key=True)
    Patient_ID = Column(ForeignKey('Patients.Patient_ID'), index=True)
    Due_Date = Column(DateTime)
    Status = Column(Integer)
    Creation_Date = Column(TIMESTAMP)

    Patient = relationship('Patient')




class RoomBooking(db.Model):
    __tablename__ = 'Room_Bookings'

    Booking_ID = Column(Integer, primary_key=True)
    Patient_ID = Column(ForeignKey('Patients.Patient_ID'), index=True)
    Room_ID = Column(ForeignKey('Rooms.Room_ID'), index=True)
    Start_Date = Column(DateTime)
    End_Date = Column(DateTime)
    Status = Column(Integer, comment='1 = Active, 0 = Cancelled')
    Patient = relationship('Patient')
    Room = relationship('Room')



class AvailabilitySchedule(db.Model):
    __tablename__ = 'Availability_Schedule'

    Schedule_ID = Column(INTEGER, primary_key=True,autoincrement=True)
    Schedule_Date = Column(Date)
    Slot_ID = Column(ForeignKey('Time_Slots.Slot_ID', ondelete='RESTRICT'), nullable=False, index=True)
    Staff_ID = Column(ForeignKey('Hospital_Staff.Staff_ID'), nullable=False, index=True)
    Room_ID = Column(ForeignKey('Rooms.Room_ID'), index=True)
    Status = Column(Integer)
    Room = relationship('Room')
    Time_Slot = relationship('TimeSlot')
    Hospital_Staff = relationship('HospitalStaff')


class InvoiceRecord(db.Model):
    __tablename__ = 'Invoice_Records'

    Record_ID = Column(Integer, primary_key=True)
    Invoice_Number = Column(ForeignKey('Invoices.Invoice_Number'), index=True)
    Staff_ID = Column(ForeignKey('Hospital_Staff.Staff_ID'), index=True)
    Description = Column(String(255))
    Amount = Column(DECIMAL(10, 2))

    Invoice = relationship('Invoice')
    Hospital_Staff = relationship('HospitalStaff')


class Payment(db.Model):
    __tablename__ = 'Payments'

    Payment_ID = Column(Integer, primary_key=True)
    Invoice_Number = Column(ForeignKey('Invoices.Invoice_Number'), index=True)
    Description = Column(VARCHAR(255))
    Payment_Date = Column(TIMESTAMP)
    Payment_Amount = Column(DECIMAL(10, 2))

    Invoice = relationship('Invoice')


class Prescription(db.Model):
    __tablename__ = 'Prescriptions'

    Prescription_ID = Column(Integer, primary_key=True)
    Patient_ID = Column(ForeignKey('Patients.Patient_ID'), index=True)
    Staff_ID = Column(ForeignKey('Hospital_Staff.Staff_ID'), index=True)
    Description = Column(String(255))
    Prescription_Date = Column(DateTime)

    Patient = relationship('Patient')
    Hospital_Staff = relationship('HospitalStaff')


class Appointment(db.Model):
    __tablename__ = 'Appointments'

    Appointment_ID = Column(INTEGER, primary_key=True, autoincrement=True)
    Schedule_ID = Column(ForeignKey('Availability_Schedule.Schedule_ID'), index=True)
    Status = Column(Integer)
    Patient_ID = Column(ForeignKey('Patients.Patient_ID'), index=True)
    Type = Column(String(255))

    Patient = relationship('Patient')
    Availability_Schedule = relationship('AvailabilitySchedule')


class PrescriptionContent(db.Model):
    __tablename__ = 'Prescription_Content'

    PRecord_ID = Column(Integer, primary_key=True)
    Prescription_ID = Column(ForeignKey('Prescriptions.Prescription_ID'), index=True)
    Medicine_ID = Column(ForeignKey('Medicines.Medicine_ID'), index=True)
    Box = Column(Integer)

    Medicine = relationship('Medicine')
    Prescription = relationship('Prescription')


class Diagnose(db.Model):
    __tablename__ = 'Diagnoses'

    Diagnose_ID = Column(Integer, primary_key=True)
    Patient_ID = Column(ForeignKey('Patients.Patient_ID'), index=True)
    Appointment_ID = Column(ForeignKey('Appointments.Appointment_ID'), index=True)
    Disease_ID = Column(ForeignKey('Diseases.Disease_ID'), index=True)

    Appointment = relationship('Appointment')
    Disease = relationship('Disease')
    Patient = relationship('Patient')