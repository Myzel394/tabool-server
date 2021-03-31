from typing import *

from django.db.models import Model
from django.test import Client, TestCase

__all__ = [
    "ClientTestMixin", "GenericAPITestMixin", "joinkwargs",
]


class ClientTestMixin(TestCase):
    client = Client()
    
    def assertStatusOk(self, status_code: int) -> None:
        self.assertTrue(200 <= status_code <= 299, f"status_code is '{status_code}'")
    
    def assertStatusNotOk(self, status_code: int) -> None:
        self.assertTrue(status_code < 200 or status_code > 299, f"status_code is '{status_code}'")


class GenericAPITestMixin(ClientTestMixin):
    def generic_get_test(
            self,
            obj,
            api_suffix: str,
            api_name: str,
    ):
        url = f"/api/{api_suffix}{api_name}/{obj.id}/"
        response = self.client.get(url)
        self.assertStatusOk(response.status_code)
        return response
    
    def generic_list_test(
            self,
            obj,
            api_suffix: str,
            api_name: str,
    ):
        url = f"/api/{api_suffix}{api_name}/"
        response = self.client.get(url)
        self.assertStatusOk(response.status_code)
        
        ids = [
            element["id"]
            for element in response.data["results"]
        ]
        self.assertIn(obj.id, ids)
        return response
    
    def generic_post_test(
            self,
            data: dict,
            api_suffix: str,
            api_name: str,
    ):
        url = f"/api/{api_suffix}{api_name}/"
        response = self.client.post(url, data, content_type="application/json")
        self.assertStatusOk(response.status_code)
        return response
    
    def generic_patch_test(
            self,
            obj,
            data: dict,
            api_suffix: str,
            api_name: str,
    ):
        url = f"/api/{api_suffix}{api_name}/{obj.id}/"
        response = self.client.patch(url, data, content_type="application/json")
        self.assertStatusOk(response.status_code)
        return response
    
    def generic_delete_test(
            self,
            obj,
            api_suffix: str,
            api_name: str,
    ):
        url = f"/api/{api_suffix}{api_name}/{obj.id}/"
        response = self.client.delete(url)
        self.assertStatusOk(response.status_code)
        return response
    
    def generic_lifecycle_test(
            self,
            model: Model,
            post_data: dict,
            patch_data: dict,
            api_suffix: str,
            api_name: str
    ):
        api_name = api_name or model.__name__.lower()
        
        post_response = self.generic_post_test(data=post_data, api_suffix=api_suffix, api_name=api_name)
        object_id = post_response.data["id"]
        obj = model.objects.get(id=object_id)
        
        self.generic_patch_test(obj=obj, data=patch_data, api_suffix=api_suffix, api_name=api_name)
        
        self.generic_delete_test(obj=obj, api_suffix=api_suffix, api_name=api_name)
        
        return obj
    
    def generic_retrieve_elements_test(
            self,
            obj,
            api_suffix: str,
            api_name: str = None
    ):
        api_name = api_name or obj.__class__.__name__.lower()
        
        self.generic_get_test(obj, api_suffix=api_suffix, api_name=api_name)
        self.generic_list_test(obj=obj, api_suffix=api_suffix, api_name=api_name)
    
    def generic_elements_test(
            self,
            model: Model,
            post_data: dict,
            patch_data: dict,
            api_suffix: str,
            api_name: str = None
    ):
        api_name = api_name or model.__name__.lower()
        
        # Create
        print(f"[Generic: {api_name}] Creating object")
        post_response = self.generic_post_test(data=post_data, api_suffix=api_suffix, api_name=api_name)
        object_id = post_response.data["id"]
        obj = model.objects.get(id=object_id)
        print(f"[Generic: {api_name}] Creating object -> Done")
        
        # Get
        print(f"[Generic: {api_name}] Getting objects")
        self.generic_get_test(obj, api_suffix=api_suffix, api_name=api_name)
        self.generic_list_test(obj=obj, api_suffix=api_suffix, api_name=api_name)
        print(f"[Generic: {api_name}] Getting objects -> Done")
        
        # Patch
        print(f"[Generic: {api_name}] Patching object")
        self.generic_patch_test(obj=obj, data=patch_data, api_suffix=api_suffix, api_name=api_name)
        print(f"[Generic: {api_name}] Patching object -> Done")
        
        # Delete
        print(f"[Generic: {api_name}] Deleting object")
        self.generic_delete_test(obj=obj, api_suffix=api_suffix, api_name=api_name)
        print(f"[Generic: {api_name}] Deleting object -> Done")


def joinkwargs(defaults: Dict[str, Callable], given: dict, /) -> dict:
    data = {}
    for key, value in defaults.items():
        if key in given:
            data[key] = given[key]
        else:
            data[key] = value()
    
    remaining_keys = set(given.keys()) - set(defaults.keys())
    
    for key in remaining_keys:
        data[key] = given[key]
    
    return data
