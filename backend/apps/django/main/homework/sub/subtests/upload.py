# TODO: Add for non GitHub-Workflow environments!
"""
class UploadTest(ClientTestMixin, LessonUploadTestMixin, UtilsTestMixin):
    def setUp(self) -> None:
        self.load_lesson_upload()
    
    def _test_direct_scooso_upload(self):
        filename = self.Random_filename()
        
        response = self.client.post(
            f"/api/data/submission/scooso/",
            {
                "lesson": self.lesson.id,
                "file": SimpleUploadedFile(
                    filename,
                    self.Random_data(1024 * 5).encode()
                )
            }
        )
        self.assertStatusOk(response.status_code)
        
        # Check
        with MaterialRequest(username=self.username, password=self.password) as scraper:
            materials = scraper.get_materials(
                time_id=self.time_id,
                targeted_date=self.target_date,
                material_type=MaterialTypeOptions.HOMEWORK
            )
        
        available_filenames = [
            material['filename']
            for material in materials['materials']
        ]
        self.assertIn(filename, available_filenames)
"""
