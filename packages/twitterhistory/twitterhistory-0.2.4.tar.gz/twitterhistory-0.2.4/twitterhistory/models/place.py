#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.

"""A Twitter Place ORM data model."""


__all__ = ["Place"]


import dataclasses

import geoalchemy2
import shapely.geometry
import sqlalchemy
import sqlalchemy.orm

from .base import Base


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place


@dataclasses.dataclass
class PlaceType(Base):
    """A place type ORM data model."""

    place_type = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)
    places = sqlalchemy.orm.relationship("Place")


@dataclasses.dataclass
class Country(Base):
    """A country ORM data model."""

    __tablename__ = "countries"  # override "countrys"

    name = sqlalchemy.Column(sqlalchemy.Text)
    code = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)
    places = sqlalchemy.orm.relationship("Place")


@dataclasses.dataclass
class Place(Base):
    """A Twitter Place ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)

    contained_within = sqlalchemy.orm.relationship(
        "Place", back_populates="contains", remote_side=[id]
    )
    contains = sqlalchemy.orm.relationship("Place", back_populates="contained_within")
    container_id = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("places.id")
    )

    country_code = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("countries.code")
    )
    country = sqlalchemy.orm.relationship("Country", back_populates="places")

    geom = sqlalchemy.Column(geoalchemy2.Geometry(srid=4326))

    name = sqlalchemy.Column(sqlalchemy.Text)
    full_name = sqlalchemy.Column(sqlalchemy.Text)

    place_type_place_type = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("place_types.place_type")
    )
    place_type = sqlalchemy.orm.relationship("PlaceType", back_populates="places")

    tweets = sqlalchemy.orm.relationship("Tweet")

    @classmethod
    def from_api_data(cls, session, data):
        """Instantiate from “raw” API response data."""
        instance = session.merge(cls(data["id"]))

        instance.name = data["name"]
        instance.full_name = data["full_name"]
        instance.place_type = session.merge(PlaceType(place_type=data["place_type"]))

        if "contained_within" in data:
            for other_place in data["contained_within"]:
                other_place = session.merge(Place(id=other_place))
                if other_place not in instance.contained_within:
                    instance.contained_within.append(other_place)

        if "country" in data and "country_code" in data:
            country = session.merge(Country(code=data["country_code"]))
            country.name = data["country"]
            instance.country = country

        if "geometry" in data["geo"]:
            instance.geom = shapely.geometry.shape(data["geo"]["geometry"]).wkt
        elif "bbox" in data["geo"]:
            instance.geom = shapely.geometry.box(*data["geo"]["bbox"]).wkt

        return session.merge(instance)
