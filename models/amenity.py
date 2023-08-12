#!/usr/bin/python3
"""Defines the Amenity class that inherits from BaseModel."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents avilable amenities.

    Attributes:
        name (str): The name of amenity.
    """

    name = ""
