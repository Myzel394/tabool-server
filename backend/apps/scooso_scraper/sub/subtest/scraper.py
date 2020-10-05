import json
import random
import uuid
from datetime import date, datetime
from pathlib import Path
from pprint import pp

import lorem

from apps.lesson.models import TeacherScoosoData
from ...actions import import_teachers
from ...mixins.tests.dummy_data import DummyUser
from ...scrapers import HomeworkRequest, MaterialRequest, MaterialTypeOptions, TimetableRequest
from ...scrapers.parsers import PureTimetableParser


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


class SomeTests(DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
        
        scraper = TimetableRequest(self.username, self.password)
        scraper.login()
        data = scraper.get_timetable()
        
        self.data = data
    
    def test_material(self):
        material_id = 73893
        download_path = Path(f"./tmp/scooso_scraper/materials/random_file.txt")
        scraper = MaterialRequest(self.username, self.password)
        
        scraper.download_material(material_id, download_path)
    
    def test_get_material(self):
        random_material_data = random.choice(self.data['materials_data'])
        scraper = MaterialRequest(self.username, self.password)
        materials = scraper.get_materials(
            random_material_data['material']['time_id'],
            random_material_data['material']['target_date']
        )
        random_material = random.choice(materials['materials'])
        
        download_path = Path(f"./tmp/scooso_scraper/materials/{random_material['filename']}")
        
        path = scraper.download_material(random_material['id'], download_path)
        
        self.assertTrue(path.exists())
    
    def test_upload_material(self):
        time_id = 29743
        target_date = date(2020, 10, 1)
        filename = str(uuid.uuid4()) + ".txt"
        content = lorem.text()
        material_type = MaterialTypeOptions.HOMEWORK
        
        scraper = MaterialRequest(self.username, self.password)
        scraper.login()
        
        scraper.upload_material(time_id, target_date, filename, content, material_type)
        
        # Check if file exists
        materials = scraper.get_materials(time_id, target_date, material_type)
        names = [
            material['filename']
            for material in materials['materials']
        ]
        exists = any([
            filename == name
            for name in names
        ])
        self.assertTrue(exists)
    
    def test_homework(self):
        time_id = 29501
        targeted_date = datetime(2020, 9, 25, 9, 50)
        scraper = HomeworkRequest(self.username, self.password)
        scraper.login()
        
        homework = scraper.get_homework(time_id, targeted_date)
        
        pp(homework)


class ForeignSerializerTest(DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
        
        import_teachers()
        self.scraper = TimetableRequest(self.username, self.password)
        self.scraper.login()
        self.timetable = self.scraper.get_timetable()
    
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
        event = TimetableRequest.import_modification_from_scraper(random_modification)
    
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
