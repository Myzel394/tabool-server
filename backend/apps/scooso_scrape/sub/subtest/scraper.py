import json
import os
from pathlib import Path
from pprint import pp

from django.test import TestCase
from dotenv import load_dotenv

from ...scrapers.parsers import PureTimetableParser


class ParserTest(TestCase):
    def setUp(self) -> None:
        load_dotenv()
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        
        with Path(__file__).parent.joinpath("jsons/2809_0210.json").open() as file:
            data = file.read()
        
        self.data = json.loads(data)
    
    def test_parser(self):
        parser = PureTimetableParser(self.data)
        self.assertTrue(parser.is_valid)
        data = parser.data
        
        self.assertEqual(len(data["lessons"]), 21)
        self.assertEqual(len(data["modifications"]), 1)
        self.assertEqual(len(data["events"]), 3)
        self.assertEqual(len(data["free_periods"]), 6)
        self.assertEqual(len(data["materials_data"]), 6)
        
        pp(parser.data)
