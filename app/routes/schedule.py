from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.extensions import db
from app.models.models import Exam, Subject, StudentGroup, Teacher, Room
from datetime import datetime

schedule = Blueprint('schedule', __name__, url_prefix='/schedule')

# 1. Просмотр всех экзаменов
@schedule.route('/')
@login_required
def view_schedule():
    exams = Exam.query.all()
    return render_template('admin/schedule.html', exams=exams)

# 2. Добавление экзамена
@schedule.route('/add', methods=['GET', 'POST'])
@login_required
def add_exam():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        group_id = request.form.get('group_id')
        teacher_id = request.form.get('teacher_id')
        room_id = request.form.get('room_id')
        date = request.form.get('date')
        time = request.form.get('time')

        new_exam = Exam(
            subject_id=subject_id,
            group_id=group_id,
            teacher_id=teacher_id,
            room_id=room_id,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            time=datetime.strptime(time, '%H:%M').time()
        )
        db.session.add(new_exam)
        db.session.commit()
        flash('Экзамен успешно добавлен!', 'success')
        return redirect(url_for('schedule.view_schedule'))

    subjects = Subject.query.all()
    groups = StudentGroup.query.all()
    teachers = Teacher.query.all()
    rooms = Room.query.all()
    return render_template('admin/add_exam.html', subjects=subjects, groups=groups, teachers=teachers, rooms=rooms)

# 3. Удаление экзамена
@schedule.route('/delete/<int:exam_id>', methods=['POST'])
@login_required
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    db.session.delete(exam)
    db.session.commit()
    flash('Экзамен удален!', 'danger')
    return redirect(url_for('schedule.view_schedule'))