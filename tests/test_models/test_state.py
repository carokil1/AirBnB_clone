#!/usr/bin/python3
"""Defines unittests for models/state.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State

class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the class State."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        stt = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(stt))
        self.assertNotIn("name", stt.__dict__)

    def test_two_states_unique_ids(self):
        stt1 = State()
        stt2 = State()
        self.assertNotEqual(stt1.id, stt2.id)

    def test_two_states_different_created_at(self):
        stt1 = State()
        sleep(0.05)
        stt2 = State()
        self.assertLess(stt1.created_at, stt2.created_at)

    def test_two_states_different_updated_at(self):
        stt1 = State()
        sleep(0.05)
        stt2 = State()
        self.assertLess(stt1.updated_at, stt2.updated_at)

    def test_str_representation(self):
        dtm = datetime.today()
        dtm_repr = repr(dtm)
        stt = State()
        stt.id = "123456"
        stt.created_at = stt.updated_at = dtt
        sttstr = stt.__str__()
        self.assertIn("[State] (123456)", sttstr)
        self.assertIn("'id': '123456'", sttstr)
        self.assertIn("'created_at': " + dtm_repr, sttstr)
        self.assertIn("'updated_at': " + dtm_repr, sttstr)

    def test_args_unused(self):
        stt = State(None)
        self.assertNotIn(None, stt.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dtm = datetime.today()
        dtm_iso = dtm.isoformat()
        stt = State(id="345", created_at=dtm_iso, updated_at=dtm_iso)
        self.assertEqual(stt.id, "345")
        self.assertEqual(stt.created_at, dtm)
        self.assertEqual(stt.updated_at, dtm)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the class State."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

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
        stt = State()
        sleep(0.05)
        first_updated_at = stt.updated_at
        stt.save()
        self.assertLess(first_updated_at, stt.updated_at)

    def test_two_saves(self):
        stt = State()
        sleep(0.05)
        first_updated_at = stt.updated_at
        stt.save()
        second_updated_at = stt.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        stt.save()
        self.assertLess(second_updated_at, st.updated_at)

    def test_save_with_arg(self):
        stt = State()
        with self.assertRaises(TypeError):
            stt.save(None)

    def test_save_updates_file(self):
        stt = State()
        stt.save()
        sttid = "State." + stt.id
        with open("file.json", "r") as json_file:
            self.assertIn(sttid, json_file.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the class State."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        stt = State()
        self.assertIn("id", stt.to_dict())
        self.assertIn("created_at", stt.to_dict())
        self.assertIn("updated_at", stt.to_dict())
        self.assertIn("__class__", stt.to_dict())

    def test_to_dict_contains_added_attributes(self):
        stt = State()
        stt.middle_name = "Alx"
        stt.my_number = 23
        self.assertEqual("Alx", stt.middle_name)
        self.assertIn("my_number", stt.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        stt = State()
        stt_dict = stt.to_dict()
        self.assertEqual(str, type(stt_dict["id"]))
        self.assertEqual(str, type(stt_dict["created_at"]))
        self.assertEqual(str, type(stt_dict["updated_at"]))

    def test_to_dict_output(self):
        dtm = datetime.today()
        stt = State()
        stt.id = "123456"
        stt.created_at = stt.updated_at = dtm
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dtm.isoformat(),
            'updated_at': dtm.isoformat(),
        }
        self.assertDictEqual(stt.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        stt = State()
        self.assertNotEqual(stt.to_dict(), stt.__dict__)

    def test_to_dict_with_arg(self):
        stt = State()
        with self.assertRaises(TypeError):
            stt.to_dict(None)


if __name__ == "__main__":
    unittest.main()
