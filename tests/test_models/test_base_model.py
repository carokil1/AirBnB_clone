#!/usr/bin/python3
"""Defines unittests for models/base_model.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the class BaseModel."""

    def test_no_args_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        bmdl1 = BaseModel()
        bmdl2 = BaseModel()
        self.assertNotEqual(bmdl1.id, bmdl2.id)

    def test_two_models_different_created_at(self):
        bmdl1 = BaseModel()
        sleep(0.05)
        bmdl2 = BaseModel()
        self.assertLess(bmdl1.created_at, bmdl2.created_at)

    def test_two_models_different_updated_at(self):
        bmdl1 = BaseModel()
        sleep(0.05)
        bmdl2 = BaseModel()
        self.assertLess(bmdl1.updated_at, bmdl2.updated_at)

    def test_str_representation(self):
        dtm = datetime.today()
        dtm_repr = repr(dtm)
        bmdl = BaseModel()
        bmdl.id = "123456"
        bmdl.created_at = bmdl.updated_at = dtm
        bmdlstr = bmdl.__str__()
        self.assertIn("[BaseModel] (123456)", bmdlstr)
        self.assertIn("'id': '123456'", bmdlstr)
        self.assertIn("'created_at': " + dtm_repr, bmdlstr)
        self.assertIn("'updated_at': " + dtm_repr, bmdlstr)

    def test_args_unused(self):
        bmdl = BaseModel(None)
        self.assertNotIn(None, bmdl.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dtm = datetime.today()
        dtm_iso = dtm.isoformat()
        bmdl = BaseModel(id="345", created_at=dtm_iso, updated_at=dtm_iso)
        self.assertEqual(bmdl.id, "345")
        self.assertEqual(bmdl.created_at, dtm)
        self.assertEqual(bmdl.updated_at, dtm)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_with_args_and_kwargs(self):
        dtm = datetime.today()
        dtm_iso = dtm.isoformat()
        bmdl = BaseModel("12", id="345", created_at=dtm_iso, updated_at=dtm_iso)
        self.assertEqual(bmdl.id, "345")
        self.assertEqual(bmdl.created_at, dtm)
        self.assertEqual(bmdl.updated_at, dtm)


class TestBaseModel_save(unittest.TestCase):
    """Unittests for testing save method of the class BaseModel."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        bmdl = BaseModel()
        sleep(0.05)
        first_updated_at = bmdl.updated_at
        bmdl.save()
        self.assertLess(first_updated_at, bmdl.updated_at)

    def test_two_saves(self):
        bmdl = BaseModel()
        sleep(0.05)
        first_updated_at = bmdl.updated_at
        bmdl.save()
        second_updated_at = bmdl.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bmdl.save()
        self.assertLess(second_updated_at, bmdl.updated_at)

    def test_save_with_arg(self):
        bmdl = BaseModel()
        with self.assertRaises(TypeError):
            bmdl.save(None)

    def test_save_updates_file(self):
        bmdl = BaseModel()
        bmdl.save()
        bmdlid = "BaseModel." + bmdl.id
        with open("file.json", "r") as json_file:
            self.assertIn(bmdlid, json_file.read())


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the class BaseModel."""

    def test_to_dict_type(self):
        bmdl = BaseModel()
        self.assertTrue(dict, type(bmdl.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        bmdl = BaseModel()
        self.assertIn("id", bmdl.to_dict())
        self.assertIn("created_at", bmdl.to_dict())
        self.assertIn("updated_at", bmdl.to_dict())
        self.assertIn("__class__", bmdl.to_dict())

    def test_to_dict_contains_added_attributes(self):
        bmdl = BaseModel()
        bmdl.name = "Alx"
        bmdl.my_number = 23
        self.assertIn("name", bmdl.to_dict())
        self.assertIn("my_number", bmdl.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        bmdl = BaseModel()
        bmdl_dict = bmdl.to_dict()
        self.assertEqual(str, type(bmdl_dict["created_at"]))
        self.assertEqual(str, type(bmdl_dict["updated_at"]))

    def test_to_dict_output(self):
        dtm = datetime.today()
        bmdl = BaseModel()
        bmdl.id = "123456"
        bmdl.created_at = bmdl.updated_at = dtm
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dtm.isoformat(),
            'updated_at': dtm.isoformat()
        }
        self.assertDictEqual(bmdl.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        bmdl = BaseModel()
        self.assertNotEqual(bmdl.to_dict(), bmdl.__dict__)

    def test_to_dict_with_arg(self):
        bmdl = BaseModel()
        with self.assertRaises(TypeError):
            bmdl.to_dict(None)


if __name__ == "__main__":
    unittest.main()
