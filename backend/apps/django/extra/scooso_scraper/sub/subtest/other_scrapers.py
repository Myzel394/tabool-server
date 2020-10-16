from pprint import pp

from django.test import TestCase

from apps.django.extra.scooso_scraper.other_scrapers.scrape_teachers import scrape_teachers


class TeacherScrapeTest(TestCase):
    def test_scraper(self):
        data = scrape_teachers()
        
        self.assertGreater(len(data), 0)
        pp(data)
