##routes for website
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Patient
from . import db
import json
from .auth import check_session
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if check_session():
        patientID = session["Patient_ID"]
        return render_template("profile.html", patient=patientID)
    else:
        return redirect(url_for('auth.login'))




