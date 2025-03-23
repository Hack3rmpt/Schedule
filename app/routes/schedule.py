from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from .decorators import admin_required
from app.forms import (
    DirectionForm, AddSpecializationForm, EditSpecializationForm, AddGroupForm, EditGroupForm, AddRoomForm,
    EditRoomForm, AddTeacherForm, EditTeacherForm, AddExamForm, EditExamForm
)
from app.models.models import (
    Direction, Specialization, StudentGroup,
    Subject, Room, Exam, Teacher
)

schedule = Blueprint('schedule', __name__, url_prefix='/schedule')


def handle_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{getattr(form, field).label.text}: {error}", 'danger')


# ========================
# Направления (Directions)
# ========================
@schedule.route('/directions')
@login_required
def list_directions():
    directions = Direction.query.order_by(Direction.code).all()
    form = DirectionForm() if current_user.role == 'admin' else None
    return render_template('schedule/direction.html', directions=directions, add_form=form)

@schedule.route('/directions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_direction():
    form = DirectionForm()
    if form.validate_on_submit():
        try:
            direction = Direction(
                code=form.code.data.strip(),
                name=form.name.data.strip()
            )
            db.session.add(direction)
            db.session.commit()
            flash('Направление создано', 'success')
            return redirect(url_for('schedule.list_directions'))
        except IntegrityError:
            db.session.rollback()
            flash('Направление с таким кодом уже существует', 'danger')
    return render_template('schedule/direction.html', form=form, title='Новое направление')

@schedule.route('/directions/<int:direction_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    form = DirectionForm(obj=direction)
    form.current_id = direction_id

    if form.validate_on_submit():
        try:
            form.populate_obj(direction)
            db.session.commit()
            flash('Изменения сохранены', 'success')
            return redirect(url_for('schedule.list_directions'))
        except IntegrityError:
            db.session.rollback()
            flash('Направление с таким кодом уже существует', 'danger')
    add_form = DirectionForm()
    return render_template('schedule/direction.html', form=form, add_form=add_form, title='Редактирование направления')

@schedule.route('/directions/<int:direction_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_direction(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    db.session.delete(direction)
    db.session.commit()
    flash('Направление удалено', 'success')
    return redirect(url_for('schedule.list_directions'))


# ========================
# Специальности (Specializations)
# ========================
@schedule.route('/directions/<int:direction_id>/specializations')
@login_required
def list_specializations(direction_id):
    direction = Direction.query.get_or_404(direction_id)
    add_form = AddSpecializationForm()
    add_form.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]
    return render_template('schedule/specializations.html', direction=direction, add_form=add_form)


@schedule.route('/specializations/create', methods=['POST'])
@login_required
def create_specialization():
    form = AddSpecializationForm()
    form.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]

    if form.validate_on_submit():
        try:
            specialization = Specialization(
                name=form.name.data.strip(),
                direction_id=form.direction_id.data
            )
            db.session.add(specialization)
            db.session.commit()
            flash('Специальность создана', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Специальность с таким именем уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_specializations', direction_id=form.direction_id.data))


@schedule.route('/specializations/<int:specialization_id>/edit', methods=['POST'])
@login_required
def edit_specialization(specialization_id):
    specialization = Specialization.query.get_or_404(specialization_id)
    form = EditSpecializationForm(obj=specialization)
    form.direction_id.choices = [(d.id, d.name) for d in Direction.query.all()]

    if form.validate_on_submit():
        try:
            form.populate_obj(specialization)
            db.session.commit()
            flash('Изменения сохранены', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Специальность с таким именем уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_specializations', direction_id=specialization.direction_id))


@schedule.route('/specializations/<int:specialization_id>/delete', methods=['POST'])
@login_required
def delete_specialization(specialization_id):
    specialization = Specialization.query.get_or_404(specialization_id)
    direction_id = specialization.direction_id
    db.session.delete(specialization)
    db.session.commit()
    flash('Специальность удалена', 'success')
    return redirect(url_for('schedule.list_specializations', direction_id=direction_id))



# ========================
# Группы (groups)
# ========================

@schedule.route('/specializations/<int:specialization_id>/groups')
@login_required
def list_groups(specialization_id):
    specialization = Specialization.query.get_or_404(specialization_id)
    add_form = AddGroupForm()
    add_form.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.all()]
    return render_template('schedule/groups.html', specialization=specialization, add_form=add_form)


@schedule.route('/groups/create', methods=['POST'])
@login_required
def create_group():
    form = AddGroupForm()
    form.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.all()]

    if form.validate_on_submit():
        try:
            group = StudentGroup(
                name=form.name.data.strip(),
                specialization_id=form.specialization_id.data
            )
            db.session.add(group)
            db.session.commit()
            flash('Группа создана', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Группа с таким названием уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_groups', specialization_id=form.specialization_id.data))

@schedule.route('/groups/<int:group_id>/edit', methods=['POST'])
@login_required
def edit_group(group_id):
    group = StudentGroup.query.get_or_404(group_id)
    form = EditGroupForm(obj=group)
    form.specialization_id.choices = [(s.id, s.name) for s in Specialization.query.all()]

    if form.validate_on_submit():
        try:
            form.populate_obj(group)
            db.session.commit()
            flash('Изменения сохранены', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Группа с таким названием уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_groups', specialization_id=group.specialization_id))

@schedule.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    group = StudentGroup.query.get_or_404(group_id)
    specialization_id = group.specialization_id
    db.session.delete(group)
    db.session.commit()
    flash('Группа удалена', 'success')
    return redirect(url_for('schedule.list_groups', specialization_id=specialization_id))







