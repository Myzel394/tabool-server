import random
from datetime import datetime
from pathlib import Path

import lorem
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.django.utils.tests import *
from apps.utils.files import get_file_dates, set_file_dates
from constants import upload_sizes
from constants.api import API_VERSION
from ...mixins.tests import MaterialTestMixin


class MaterialTest(MaterialTestMixin, ClientTestMixin, UtilsTestMixin):
    def test_size(self):
        ok_data = self.Random_data(random.randint(
            int(upload_sizes.MIN_UPLOAD_SIZE * 1.1),
            int(upload_sizes.MAX_UPLOAD_SIZE * .9)
        ))
        print("Testing ok data")
        self.Create_material(
            file=SimpleUploadedFile(
                self.Random_filename(),
                ok_data.encode(),
            )
        )
        
        with self.assertRaises(ValidationError):
            print("Testing too small data")
            material = self.Create_material(
                file=SimpleUploadedFile(
                    self.Random_filename(),
                    "".encode()
                )
            )
            material
        
        with self.assertRaises(ValidationError):
            too_big_data = self.Random_data(int(upload_sizes.MAX_UPLOAD_SIZE * 1.1))
            
            print("Testing too big data")
            self.Create_material(
                file=SimpleUploadedFile(
                    self.Random_filename(),
                    too_big_data.encode()
                )
            )
    
    def test_utils(self):
        path = Path.cwd().joinpath("test.txt")
        path.write_text(lorem.text() * 5)
        new_date = datetime(2001, 1, 1, 1, 1, 1)
        
        try:
            set_file_dates(path, modified_at=new_date, accessed_at=new_date)
            
            dates = get_file_dates(path)
            self.assertEqual(dates['modified_at'], new_date)
            self.assertEqual(dates['accessed_at'], new_date)
        finally:
            path.unlink()
    
    def test_private(self):
        material = self.Create_material()
        
        with self.Login_user_as_context() as user:
            course = material.lesson.lesson_data.course
            course.participants.add(user)
            course.save()
            
            # TODO: Private-storage check!
            url = material.file.url
            
            response = self.client.get(url)
            self.assertStatusOk(response.status_code)
        
        with self.Login_user_as_context() as user:
            response = self.client.get(url)
            self.assertStatusNotOk(response.status_code)


class APITest(ClientTestMixin, MaterialTestMixin):
    def test_material(self):
        with self.Login_user_as_context() as user:
            material = self.Create_material()
            
            response = self.client.get(
                f"/api/{API_VERSION}/data/material/{material.id}/"
            )
            self.assertStatusOk(response.status_code)