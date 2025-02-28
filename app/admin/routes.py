from flask import Blueprint, render_template

bp = Blueprint('admin', __name__)

@bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')