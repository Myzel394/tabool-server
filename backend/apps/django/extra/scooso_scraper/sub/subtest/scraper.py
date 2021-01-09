import json
import os
import random
import string
from datetime import datetime
from pathlib import Path

import lorem

from apps.django.main.homework.models import Homework
from apps.django.main.lesson.mixins.tests import *
from apps.django.main.lesson.models import Lesson, LessonData
from apps.django.main.school_data.models import Subject, TeacherScoosoData
from apps.django.utils.tests import *
from ...actions import import_teachers
from ...mixins.tests import *
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


class SomeTests(LessonUploadTestMixin, UtilsTestMixin):
    def setUp(self) -> None:
        self.load_lesson_upload()
        self.scraper = TimetableRequest(self.username, self.password)
        self.scraper.login()
        
        data = self.scraper.get_timetable(
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
        filename = self.Random_filename()
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
    
    def test_download_material(self):
        material_time_ids = [
            material['material']['time_id']
            for material in self.data['materials_data']
        ]
        
        lessons_with_materials = [
            lesson
            for lesson in self.data['lessons']
            if lesson['lesson']['time_id'] in material_time_ids
        ]
        lesson_data = lessons_with_materials[0]
        lesson = self.scraper.import_lesson_from_scraper(lesson_data)
        
        self.scraper.import_materials_from_lesson(lesson)
    
    def test_timetable(self):
        with TimetableRequest(self.username, self.password) as scraper:
            data = scraper.get_timetable(datetime(2020, 11, 9), datetime(2020, 11, 13))
            
            lessons = scraper.import_timetable_from_scraper(data)
            
            print(data['homeworks'])
            print(Homework.objects.all().count())
            
            self.assertEqual(len(data['homeworks']), Homework.objects.all().count())


class ForeignSerializerTest(LessonTestMixin):
    def setUp(self) -> None:
        self.load_dummy_user()
        
        import_teachers()
        self.scraper = TimetableRequest(self.username, self.password)
        self.scraper.login()
        self.start_date = datetime.strptime(os.getenv("DATA_START_DATE"), os.getenv("DATE_FORMAT"))
        self.end_date = datetime.strptime(os.getenv("DATA_END_DATE"), os.getenv("DATE_FORMAT"))
        self.timetable = self.scraper.get_timetable(start_date=self.start_date, end_date=self.end_date)
    
    def test_timetable(self):
        # Creation
        random_lesson = random.choice(self.timetable['lessons'])
        lesson = TimetableRequest(self.username, self.password).import_lesson_from_scraper(random_lesson)
        
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
        self.assertEqual(lesson.date, lesson_data_data['date'])
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
            lesson=self.Create_lesson()
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
        
        teachers_scooso_data = TeacherScoosoData.objects.all()
        teacher_scooso_data = teachers_scooso_data.get(scooso_id=lesson['teacher']['scooso_id'])
        
        print(teacher_scooso_data)
    
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
    
    def test_no_duplicates_for_subjects(self):
        subject = self.scraper.get_timetable(
            start_date=self.start_date,
            end_date=self.end_date)['lessons'][0]['subject']
        self.scraper.import_subject(subject)
        count = Subject.objects.all().count()
        
        subject = self.scraper.get_timetable(
            start_date=self.start_date,
            end_date=self.end_date)['lessons'][0]['subject']
        self.scraper.import_subject(subject)
        new_count = Subject.objects.all().count()
        
        self.assertEqual(count, new_count)
    
    def test_no_duplicates(self):
        print("First fetch. Fixed date")
        timetable = self.scraper.get_timetable(start_date=self.start_date, end_date=self.end_date)
        self.scraper.import_timetable_from_scraper(timetable)
        count = LessonData.objects.all().count()
        print("Amount:", count)
        
        print("Second fetch. Fixed date")
        timetable = self.scraper.get_timetable(start_date=self.start_date, end_date=self.end_date)
        self.scraper.import_timetable_from_scraper(timetable)
        new_count = LessonData.objects.all().count()
        print("Amount:", new_count)
        
        self.assertEqual(count, new_count)
        
        print("Third fetch. Current date")
        timetable = self.scraper.get_timetable()
        self.scraper.import_timetable_from_scraper(timetable)
        today_count = LessonData.objects.all().count()
        print("Amount:", today_count)
        
        print("Fourth fetch. Current date")
        timetable = self.scraper.get_timetable()
        self.scraper.import_timetable_from_scraper(timetable)
        new_today_count = LessonData.objects.all().count()
        print("Amount:", new_today_count)
        
        self.assertEqual(today_count, new_today_count)
    
    def test_random(self):
        timetable = self.scraper.get_timetable()
        self.scraper.import_timetable_from_scraper(timetable)
        with_conference = Lesson.objects.all().filter(video_conference_link__isnull=False)


class DummyTest(DummyUser):
    def setUp(self) -> None:
        # Load data
        self.load_dummy_user()
        
        with Path(__file__).parent.joinpath("jsons/0211_0611.json").open() as file:
            data = file.read()
        
        self.data = json.loads(data)
    
    def test_parser_offline(self):
        parser = PureTimetableParser(self.data)
        self.assertTrue(parser.is_valid)
        data = parser.data
        
        print(data)
