##routes for website
from flask import Blueprint, render_template, request,flash
from .models import Patient
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("profile.html", patient=False)


