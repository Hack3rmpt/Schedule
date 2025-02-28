from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from flask import Blueprint

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@bp.route('/create_user')
@login_required
def create_user():
    return render_template('admin/create_user.html')

@bp.route('/logs')
@login_required
def logs():
    return render_template('admin/logs.html')