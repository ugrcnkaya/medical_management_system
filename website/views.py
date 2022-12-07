##routes for website
from flask import Blueprint, render_template, request,flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Patient
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("profile.html", patient=current_user)


