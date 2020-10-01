import json
import random
from pathlib import Path

from ...mixins.tests.dummy_data import DummyUser
from ...scrapers import MaterialRequest, TimetableRequest
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
        self.assertEqual(len(data["modifications"]), 1)
        self.assertEqual(len(data["events"]), 3)
        self.assertEqual(len(data["free_periods"]), 6)
        self.assertEqual(len(data["materials_data"]), 5)


class TimetableTest(DummyUser):
    def setUp(self) -> None:
        self.load_dummy_user()
        
        scraper = TimetableRequest(self.username, self.password)
        scraper.login()
        data = scraper.get_timetable()
        
        self.data = data
    
    def test_material(self):
        random_subject = random.choice(self.data['materials_data'])
        scraper = MaterialRequest(self.username, self.password)
        materials = scraper.get_materials(random_subject['time_id'], random_subject['calendar_id'])
        random_material = random.choice(materials)
        
        download_path = Path(f"./tmp/scooso_scraper/materials/{random_material['filename']}")
        
        scraper.download_material(random_material['id'], download_path)
