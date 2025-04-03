from datetime import datetime, timedelta
import random
from sqlalchemy import and_
from app.models.models import Exam, Room, Teacher, Subject, Course, StudentGroup
from app.extensions import db as database, db


class ScheduleGenerator:
    def __init__(self, course_id):
        self.course = Course.query.get_or_404(course_id)
        self.groups = StudentGroup.query.filter_by(course_id=course_id).all()
        self.subjects = Subject.query.filter_by(course_id=course_id).all()

        # Конфигурация корпусов
        self.building_config = {
            'Корпус на ул. Нежинской 7': {
                'priority_time': (8, 15),
                'types': ['lecture', 'practice']
            },
            'Корпус на ул. Нахимовский проспект 21': {
                'priority_time': (13, 17),
                'types': ['lab', 'practice']
            }
        }

    def generate(self, start_date, end_date, max_per_day=3, min_interval=2):
        exams_created = 0
        try:
            current_date = start_date
            while current_date <= end_date:
                if current_date.weekday() >= 5:
                    current_date += timedelta(days=1)
                    continue

                # Выбираем корпус для дня
                selected_building = self._select_building_for_day(current_date)

                for group in self.groups:
                    subjects = self._get_group_subjects(group)
                    schedule = self._distribute_subjects(
                        subjects, current_date, current_date, max_per_day, min_interval
                    )

                    for exam_date, exam_subjects in schedule.items():
                        if len(exam_subjects) > 3:
                            raise ValueError("Максимум 3 экзамена в день")

                        time_slots = self._generate_time_slots(exam_date, len(exam_subjects))
                        used_rooms = set()

                        for i, subject in enumerate(exam_subjects):
                            teacher = self._get_available_teacher(subject, time_slots[i])
                            room = self._find_available_room(
                                subject, time_slots[i], selected_building, used_rooms
                            )

                            if teacher and room:
                                self._create_exam(group, subject, teacher, room, time_slots[i])
                                used_rooms.add(room.id)
                                exams_created += 1

                current_date += timedelta(days=1)

            database.session.commit()
            return exams_created
        except Exception as e:
            database.session.rollback()
            raise e

    def _select_building_for_day(self, date):
        # Чередование корпусов по дням
        buildings = list(self.building_config.keys())
        return buildings[date.day % len(buildings)]

    def _generate_time_slots(self, date, count):
        base_times = [
            datetime(date.year, date.month, date.day, 8, 30),  # 1-я пара
            datetime(date.year, date.month, date.day, 10, 10),  # 2-я пара
            datetime(date.year, date.month, date.day, 12, 0),  # 3-я пара
            datetime(date.year, date.month, date.day, 13, 50),  # 4-я пара
            datetime(date.year, date.month, date.day, 15, 30)  # 5-я пара
        ]
        return base_times[:count]

    def _find_available_room(self, subject, exam_time, building, used_rooms):
        end_time = exam_time + timedelta(minutes=90)
        room_type = self._determine_room_type(subject.name)

        # Ищем в выбранном корпусе
        room = Room.query.filter(
            Room.type == room_type,
            Room.building == building,
            ~Room.id.in_(used_rooms),
            ~Room.id.in_(
                database.session.query(Exam.room_id).filter(
                    and_(
                        Exam.datetime >= exam_time,
                        Exam.datetime < end_time
                    )
                )
            )
        ).order_by(db.func.random()).first()

        return room

    def _distribute_subjects(self, subjects, start, end, max_per_day, min_interval):
        if max_per_day > 3:
            raise ValueError("Максимальное количество экзаменов в день не может превышать 3")

        schedule = {}
        current_date = start
        subjects = subjects.copy()
        random.shuffle(subjects)

        while subjects and current_date <= end:
            if current_date.weekday() >= 5:
                current_date += timedelta(days=1)
                continue

            day_subjects = subjects[:max_per_day]
            subjects = subjects[max_per_day:]

            schedule[current_date] = day_subjects
            current_date += timedelta(days=min_interval)

        return schedule

    # Остальные методы остаются без изменений
    def _determine_room_type(self, subject_name):
        subject_lower = subject_name.lower()
        if any(kw in subject_lower for kw in ['программирование', 'базы данных', 'веб']):
            return 'practice'
        elif any(kw in subject_lower for kw in ['сети', 'лабораторная', 'безопасность']):
            return 'lab'
        return 'lecture'

    def _get_group_subjects(self, group):
        return Subject.query.filter_by(course_id=group.course_id).all()

    def _get_available_teacher(self, subject, exam_time):
        end_time = exam_time + timedelta(minutes=90)
        teachers = subject.teachers

        for teacher in teachers:
            conflicting = Exam.query.filter(
                and_(
                    Exam.teacher_id == teacher.id,
                    Exam.datetime >= exam_time,
                    Exam.datetime < end_time
                )
            ).count()

            if not conflicting:
                return teacher
        return None

    def _create_exam(self, group, subject, teacher, room, exam_time):
        exam = Exam(
            datetime=exam_time,
            duration=90,
            subject_id=subject.id,
            group_id=group.id,
            teacher_id=teacher.id,
            room_id=room.id
        )
        database.session.add(exam)