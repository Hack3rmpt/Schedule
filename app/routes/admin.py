from flask import render_template, redirect, url_for, flash
from flask import Blueprint

admin = Blueprint('admin', __name__)

@admin.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin.route('/create_user')
def create_user():
    return render_template('admin/create_user.html')

@admin.route('/logs')
def logs():
    return render_template('admin/logs.html')