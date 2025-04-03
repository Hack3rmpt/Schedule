from dis import show_code
from shlex import shlex
import logging
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from .decorators import admin_required
from app.forms import (
    DirectionForm, AddSpecializationForm, EditSpecializationForm, AddGroupForm, EditGroupForm, AddRoomForm,
    EditRoomForm, AddTeacherForm, EditTeacherForm, AddExamForm, EditExamForm, EditSubjectForm, AddSubjectForm,
    AddCourseForm, EditCourseForm, GenerateScheduleForm
)
from app.models.models import (
    Direction, Specialization, StudentGroup,
    Subject, Room, Exam, Teacher, Course, ScheduleSettings
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

@schedule.route('/courses/<int:course_id>/groups')
@login_required
def list_groups(course_id):
    course = Course.query.get_or_404(course_id)
    specialization = course.specialization
    add_form = AddGroupForm()
    add_form.course_id.choices = [(c.id, f"{c.number} курс") for c in Course.query.filter_by(specialization_id=course.specialization_id).all()]
    return render_template('schedule/groups.html', course=course, specialization=specialization, add_form=add_form)


@schedule.route('/groups/create', methods=['POST'])
@login_required
def create_group():
    form = AddGroupForm()
    form.course_id.choices = [(c.id, f"{c.number} курс") for c in Course.query.filter_by(specialization_id=Course.query.get(form.course_id.data).specialization_id).all()]

    if form.validate_on_submit():
        try:
            group = StudentGroup(
                name=form.name.data.strip(),
                course_id=form.course_id.data
            )
            db.session.add(group)
            db.session.commit()
            flash('Группа создана', 'success')
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Ошибка при создании группы: {e}")
            flash('Группа с таким названием уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_groups', course_id=form.course_id.data))



@schedule.route('/groups/<int:group_id>/edit', methods=['POST'])
@login_required
def edit_group(group_id):
    group = StudentGroup.query.get_or_404(group_id)
    form = EditGroupForm(obj=group)
    form.group_id.data = group.id
    form.course_id.choices = [(c.id, f"{c.number} курс") for c in Course.query.filter_by(specialization_id=group.course.specialization_id).all()]

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
    return redirect(url_for('schedule.list_groups', course_id=group.course_id))


@schedule.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    group = StudentGroup.query.get_or_404(group_id)
    course_id = group.course_id
    db.session.delete(group)
    db.session.commit()
    flash('Группа удалена', 'success')
    return redirect(url_for('schedule.list_groups', course_id=course_id))

# ========================
# Предметы (subjects)
# ========================

@schedule.route('/courses/<int:course_id>/subjects')
@login_required
def list_subjects(course_id):
    course = Course.query.get_or_404(course_id)
    add_form = AddSubjectForm()
    add_form.course_id.choices = [(c.id, f"Курс {c.number}") for c in Course.query.all()]
    add_form.teachers.choices = [(t.id, t.full_name) for t in Teacher.query.all()]
    return render_template('schedule/subjects.html', course=course, add_form=add_form)


@schedule.route('/subjects/create', methods=['POST'])
@login_required
def create_subject():
    form = AddSubjectForm()
    form.course_id.choices = [(c.id, f"Курс {c.number}") for c in Course.query.all()]
    form.teachers.choices = [(t.id, t.full_name) for t in Teacher.query.all()]

    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data.strip(),
            course_id=form.course_id.data,
            assessment_type=form.assessment_type.data
        )
        try:
            db.session.add(subject)
            db.session.commit()

            # Добавление преподавателей
            teacher_ids = form.teachers.data
            teachers = Teacher.query.filter(Teacher.id.in_(teacher_ids)).all()
            subject.teachers.extend(teachers)

            db.session.commit()
            flash('Предмет успешно создан', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Ошибка: предмет уже существует', 'danger')
    else:
        flash('Исправьте ошибки в форме', 'danger')

    return redirect(url_for('schedule.list_subjects',
                            course_id=form.course_id.data))


@schedule.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = EditSubjectForm(obj=subject)

    # Заполняем список курсов для выбора
    form.course_id.choices = [(c.id, f"Курс {c.number}") for c in Course.query.all()]
    form.teachers.choices = [(t.id, t.full_name) for t in Teacher.query.all()]

    if form.validate_on_submit():
        try:
            # Обновляем основные поля
            subject.name = form.name.data
            subject.course_id = form.course_id.data
            subject.assessment_type = form.assessment_type.data

            # Обрабатываем поле teachers
            teacher_ids = form.teachers.data
            subject.teachers = Teacher.query.filter(Teacher.id.in_(teacher_ids)).all()

            db.session.commit()
            flash('Изменения сохранены', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Предмет с таким названием уже существует для этого курса', 'danger')
    else:
        handle_form_errors(form)

    return redirect(url_for('schedule.list_subjects', course_id=form.course_id.data))



@schedule.route('/subjects/<int:subject_id>/delete', methods=['POST'])
@login_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    course_id = subject.course_id
    db.session.delete(subject)
    db.session.commit()
    flash('Предмет удален', 'success')
    return redirect(url_for('schedule.list_subjects', course_id=course_id))

# ========================
# Курсы (courses)
# ========================

@schedule.route('/specializations/<int:specialization_id>/courses')
@login_required
def list_courses(specialization_id):
    specialization = Specialization.query.get_or_404(specialization_id)
    add_form = AddCourseForm()
    return render_template('schedule/courses.html',
                         specialization=specialization,
                         add_form=add_form)


@schedule.route('/specializations/<int:specialization_id>/courses/create', methods=['POST'])
@login_required
def create_course(specialization_id):
    form = AddCourseForm()

    if form.validate_on_submit():
        try:
            course = Course(
                number=form.number.data,
                specialization_id=specialization_id  # Берем из URL
            )
            db.session.add(course)
            db.session.commit()
            flash('Курс создан', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Курс с таким номером уже существует для этой специальности', 'danger')
    else:
        handle_form_errors(form)

    return redirect(url_for('schedule.list_courses',
                            specialization_id=specialization_id))


@schedule.route('/courses/<int:course_id>/edit', methods=['POST'])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = EditCourseForm(obj=course)
    form.course_id.data = course_id

    if form.validate_on_submit():
        try:
            form.populate_obj(course)
            db.session.commit()
            flash('Изменения сохранены', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Курс с таким номером уже существует для этой специальности', 'danger')
    else:
        handle_form_errors(form)

    return redirect(url_for('schedule.list_courses',
                            specialization_id=course.specialization_id))


@schedule.route('/courses/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    specialization_id = course.specialization_id
    db.session.delete(course)
    db.session.commit()
    flash('Курс удален', 'success')
    return redirect(url_for('schedule.list_courses', specialization_id=specialization_id))


# ========================
# Преподователи (Teachers)
# ========================

@schedule.route('/teachers', methods=['GET'])
@login_required
def list_teachers():
    teachers = Teacher.query.all()
    add_form = AddTeacherForm()
    return render_template('schedule/teachers.html', teachers=teachers, add_form=add_form)


@schedule.route('/teachers/create', methods=['GET', 'POST'])
@login_required
def create_teacher():
    form = AddTeacherForm()

    if form.validate_on_submit():
        try:
            teacher = Teacher(
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                patronymic=form.patronymic.data.strip(),
                email=form.email.data.strip()
            )
            db.session.add(teacher)
            db.session.commit()
            flash('Преподаватель успешно добавлен', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Преподаватель с такой электронной почтой уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_teachers'))

def handle_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Ошибка в поле '{getattr(form, field).label.text}': {error}", 'danger')


@schedule.route('/teachers/edit/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    form = EditTeacherForm(obj=teacher)

    if form.validate_on_submit():
        try:
            teacher.first_name = form.first_name.data.strip()
            teacher.last_name = form.last_name.data.strip()
            teacher.patronymic = form.patronymic.data.strip()
            teacher.email = form.email.data.strip()
            db.session.commit()
            flash('Данные преподавателя успешно обновлены', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Преподаватель с такой электронной почтой уже существует', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_teachers'))


@schedule.route('/teachers/delete/<int:teacher_id>', methods=['POST'])
@login_required
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    try:
        db.session.delete(teacher)
        db.session.commit()
        flash('Преподаватель успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении преподавателя: {str(e)}', 'danger')
    return redirect(url_for('schedule.list_teachers'))


# ========================
# Кабинеты (Room)
# ========================

# Роут для отображения списка аудиторий
@schedule.route('/rooms', methods=['GET', 'POST'])
def list_rooms():
    rooms = Room.query.all()
    add_form = AddRoomForm()  # Форма для добавления аудитории
    edit_form = EditRoomForm()  # Форма для редактирования аудитории

    # Обработка добавления аудитории
    if add_form.validate_on_submit():
        new_room = Room(
            number=add_form.number.data,
            capacity=add_form.capacity.data,
            type=add_form.type.data
        )
        db.session.add(new_room)
        db.session.commit()
        flash('Аудитория успешно добавлена!', 'success')
        return redirect(url_for('schedule.list_rooms'))

    return render_template('schedule/rooms.html', rooms=rooms, add_form=add_form, edit_form=edit_form)

# Роут для редактирования аудитории
@schedule.route('/edit_room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    room = Room.query.get_or_404(room_id)
    form = EditRoomForm(obj=room)  # Автоматическое заполнение из объекта
    form.room_id.data = room.id  # Явное установка room_id

    if form.validate_on_submit():
        form.populate_obj(room)  # Обновление объекта из формы
        db.session.commit()
        flash('Аудитория успешно обновлена', 'success')
        return redirect(url_for('schedule.list_rooms'))

    return render_template('rooms.html', edit_form=form)

# Роут для удаления аудитории
@schedule.route('/delete_room/<int:room_id>', methods=['POST'])
def delete_room(room_id):
    room = Room.query.get_or_404(room_id)
    db.session.delete(room)
    db.session.commit()
    flash('Аудитория успешно удалена!', 'success')
    return redirect(url_for('schedule.list_rooms'))


# ========================
# Экзамены (Exams)
# ========================

@schedule.route('/exams', methods=['GET'])
@login_required
def list_exams():
    exams = Exam.query.all()
    add_form = AddExamForm()
    edit_form = EditExamForm()  # Добавьте эту строку
    return render_template('schedule/exams.html',
                         exams=exams,
                         add_form=add_form,
                         edit_form=edit_form)  # Передаем форму редактирования


@schedule.route('/exams/create', methods=['GET', 'POST'])
@login_required
def create_exam():
    form = AddExamForm()

    if form.validate_on_submit():
        try:
            exam = Exam(
                datetime=form.datetime.data,
                duration=form.duration.data,
                subject_id=form.subject_id.data,
                group_id=form.group_id.data,
                teacher_id=form.teacher_id.data,
                room_id=form.room_id.data
            )
            db.session.add(exam)
            db.session.commit()
            flash('Экзамен успешно добавлен', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Ошибка при добавлении экзамена', 'danger')
    else:
        handle_form_errors(form)
    return redirect(url_for('schedule.list_exams'))


@schedule.route('/exams/edit/<int:exam_id>', methods=['POST'])  # Только POST
@login_required
def edit_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    form = EditExamForm(exam=exam)  # Передаем экзамен в форму

    if form.validate_on_submit():
        try:
            exam.datetime = form.datetime.data
            exam.duration = form.duration.data
            exam.subject_id = form.subject_id.data
            exam.group_id = form.group_id.data
            exam.teacher_id = form.teacher_id.data
            exam.room_id = form.room_id.data
            db.session.commit()
            flash('Экзамен успешно обновлен', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Ошибка при обновлении экзамена', 'danger')
    else:
        handle_form_errors(form)

    return redirect(url_for('schedule.list_exams'))


@schedule.route('/exams/delete/<int:exam_id>', methods=['POST'])
@login_required
def delete_exam(exam_id):
    exam = Exam.query.get_or_404(exam_id)
    try:
        db.session.delete(exam)
        db.session.commit()
        flash('Экзамен успешно удален', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении экзамена: {str(e)}', 'danger')
    return redirect(url_for('schedule.list_exams'))

from app.services.schedule_generator import ScheduleGenerator

@schedule.route('/courses/<int:course_id>/generate', methods=['GET', 'POST'])
@login_required
def generate_for_course(course_id):
    course = Course.query.get_or_404(course_id)
    form = GenerateScheduleForm()

    if form.validate_on_submit():
        try:
            generator = ScheduleGenerator(course_id)
            generated = generator.generate(
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                max_per_day=form.max_exams_per_day.data,
                min_interval=form.min_days_between_exams.data
            )

            flash(f'Сгенерировано {generated} экзаменов', 'success')
            return redirect(url_for('schedule.list_courses',
                                    specialization_id=course.specialization_id))

        except Exception as e:
            flash(f'Ошибка генерации: {str(e)}', 'danger')

    return render_template('schedule/generate.html',
                           course=course,
                           form=form)

@schedule.route('/view_schedule/<int:course_id>')
@login_required
def view_schedule(course_id):
    # Получаем данные о курсе
    course = Course.query.get_or_404(course_id)

    # Получаем сгенерированное расписание через связь с группами
    exams = Exam.query.join(StudentGroup).filter(StudentGroup.course_id == course_id).order_by(Exam.datetime).all()

    # Определяем период расписания
    start_date = exams[0].datetime if exams else None
    end_date = exams[-1].datetime if exams else None

    return render_template('schedule/view_schedule.html',
                           course=course,
                           exams=exams,
                           start_date=start_date,
                           end_date=end_date)