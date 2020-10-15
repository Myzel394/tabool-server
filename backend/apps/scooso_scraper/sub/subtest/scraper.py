import json
import os
import random
import string
from datetime import date, datetime
from pathlib import Path

import lorem

from apps.lesson.mixins.tests.course import CourseTestMixin
from apps.lesson.mixins.tests.lesson import LessonUploadTestMixin
from apps.school_data.models import TeacherScoosoData
from ...actions import import_teachers
from ...mixins.tests.dummy_data import DummyUser
from ...scrapers.material import MaterialRequest, MaterialTypeOptions
from ...scrapers.parsers import PureTimetableParser
from ...scrapers.timetable import TimetableRequest


class ParserTest(DummyUser):
    def setUp(self) -> None:
        # Load data
        self.load_dummy_user()
        
        with Path(__file__).parent.joinpath("jsons/2809_0210.json").open() as file:
            data = file.read()
        
        self.data = json.loads(data)
    
    def test_parser_offline(self):
        parser = PureTimetableParser(self.data)
        self.assertTrue(parser.is_valid)
        data = parser.data
        
        self.assertEqual(len(data["lessons"]), 21)
        self.assertEqual(len(data["modifications"]), 7)
        self.assertEqual(len(data["events"]), 3)
        self.assertEqual(len(data["materials_data"]), 5)


class SomeTests(LessonUploadTestMixin):
    def setUp(self) -> None:
        self.load_lesson_upload()
        
        with TimetableRequest(self.username, self.password) as scraper:
            data = scraper.get_timetable(
                start_date=datetime.strptime(os.getenv("DATA_START_DATE"), os.getenv("DATE_FORMAT")).date(),
                end_date=datetime.strptime(os.getenv("DATA_END_DATE"), os.getenv("DATE_FORMAT")).date()
            )
        
        self.data = data
    
    def test_upload_material(self):
        filename = str("".join(random.choices(string.ascii_letters + string.digits, k=10))) + ".txt"
        content = lorem.text()
        material_type = MaterialTypeOptions.HOMEWORK
        
        with MaterialRequest(self.username, self.password) as scraper:
            scraper.upload_material(self.time_id, self.target_date, filename, content, material_type)
        
        # Check if file exists
        materials = scraper.get_materials(self.time_id, self.target_date, material_type)
        names = [
            material['filename']
            for material in materials['materials']
        ]
        exists = any([
            filename == name
            for name in names
        ])
        print(filename, names)
        self.assertTrue(exists)
    
    def test_delete_uploaded(self):
        filename = str("".join(random.choices(string.ascii_letters + string.digits, k=10))) + ".txt"
        content = lorem.text()
        material_type = MaterialTypeOptions.HOMEWORK
        
        with MaterialRequest(self.username, self.password) as scraper:
            previous_count = len(scraper.get_materials(self.time_id, self.target_date, material_type)['materials'])
            scraper.upload_material(self.time_id, self.target_date, filename, content, material_type)
            materials = scraper.get_materials(self.time_id, self.target_date, material_type)
            material_id = materials['materials'][0]['scooso_id']
            scraper.delete_material(material_id)
            materials = scraper.get_materials(self.time_id, self.target_date, material_type)
        
        self.assertEqual(previous_count - 1, len(materials['materials']))


class ForeignSerializerTest(CourseTestMixin):
    def setUp(self) -> None:
        self.load_dummy_user()
        
        import_teachers()
        self.scraper = TimetableRequest(self.username, self.password)
        self.scraper.login()
        self.timetable = self.scraper.get_timetable(start_date=date(2020, 10, 5), end_date=date(2020, 10, 10))
    
    def test_timetable(self):
        # Creation
        random_lesson = random.choice(self.timetable['lessons'])
        lesson = TimetableRequest.import_lesson_from_scraper(random_lesson)
        
        # Validation
        lesson_data = lesson.lesson_data
        course = lesson_data.course
        subject = course.subject
        room = lesson_data.room
        
        course_data = random_lesson['course']
        subject_data = random_lesson['subject']
        lesson_data_data = random_lesson['lesson']
        room_data = random_lesson['room']
        
        self.assertEqual(subject.short_name, subject_data['code'])
        self.assertEqual(course.course_number, course_data['course_number'])
        self.assertEqual(room.place, room_data['code'])
        self.assertEqual(lesson_data.start_time, lesson_data_data['start_time'])
        self.assertEqual(lesson_data.end_time, lesson_data_data['end_time'])
        self.assertEqual(lesson_data.weekday, lesson_data_data['weekday'])
        self.assertEqual(lesson.date, lesson_data_data['date'])
    
    def test_simple(self):
        """Just checks that there are no errors thrown while importing objects"""
        # Event
        random_event = random.choice(self.timetable['events'])
        event = TimetableRequest.import_event_from_scraper(random_event)
        # Modification
        random_modification = random.choice(self.timetable['modifications'])
        modification = TimetableRequest.import_modification_from_scraper(
            random_modification,
            course=self.Create_course()
        )
    
    def test_materials(self):
        random_material_data = random.choice(self.timetable['materials_data'])
        scraper = MaterialRequest(self.username, self.password)
        materials = scraper.get_teacher_homework(
            time_id=random_material_data['material']['time_id'],
            targeted_date=random_material_data['material']['target_date'],
        )
        random_material = random.choice(materials['materials'])
        material_data_time_id = random_material_data['material']['time_id']
        
        lesson = [
            lesson
            for lesson in self.timetable['lessons']
            if lesson['lesson']['time_id'] == material_data_time_id
        ][0]
        
        imported_teacher = self.scraper.import_teacher(lesson['teacher'])
        
        teachers = TeacherScoosoData.objects.all()
        teacher = teachers.get(scooso_id=lesson['teacher']['scooso_id'])
        
        print(teacher)
    
    def test_create_material(self):
        materials_subject_ids = [
            material['subject']['scooso_id']
            for material in self.timetable['materials_data']
        ]
        lessons_with_materials = [
            lesson
            for lesson in self.timetable['lessons']
            if lesson['subject']['scooso_id'] in materials_subject_ids
        ]
        
        chosen_material = random.choice(self.timetable['materials_data'])
        chosen_lesson = [
            lesson
            for lesson in lessons_with_materials
            if lesson['subject']['scooso_id'] == chosen_material['subject']['scooso_id']
        ][0]
        lesson = self.scraper.import_lesson_from_scraper(chosen_lesson)
        
        materials = self.scraper.import_materials_from_lesson(lesson)
        print("{count} materials imported".format(count=len(materials)))
        
        # Check
        random_material = random.choice(materials)
        path = Path(random_material.file.path)
        print(path)
        self.assertTrue(path.exists())
        
        random_material.delete()
        self.assertFalse(path.exists())
    
    def test_multiple_import(self):
        import_teachers()
        
        start_count = TeacherScoosoData.objects.count()
        
        random_lesson = random.choice(self.timetable['lessons'])
        teacher = self.scraper.import_teacher(random_lesson['teacher'])
        
        self.assertTrue(hasattr(teacher, "teacherscoosodata"))
        self.assertEqual(start_count + 1, TeacherScoosoData.objects.count())
        
        teacher = self.scraper.import_teacher(random_lesson['teacher'])
        
        self.assertTrue(hasattr(teacher, "teacherscoosodata"))
        self.assertEqual(start_count + 1, TeacherScoosoData.objects.count())
