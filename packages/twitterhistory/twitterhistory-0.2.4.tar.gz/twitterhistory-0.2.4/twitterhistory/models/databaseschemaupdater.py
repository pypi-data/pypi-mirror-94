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

"""Update the database schema if necessary."""


__all__ = ["DatabaseSchemaUpdater"]


import dataclasses

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.sql.functions

from .base import Base
from ..engine import Session


# for now, schema updates are SQL only and work on PostgreSQL, only.
# GeoAlchemy2 doesn’t really support SQLite, anyway
SCHEMA_UPDATES = {
    # 0 -> 1
    1: """
        BEGIN;

        ALTER TABLE
            places
        ADD COLUMN
            country_code TEXT;

        UPDATE
            places p
        SET
            country_code = c.code
        FROM
            countries c
        WHERE
            p.country_name = c.name;

        ALTER TABLE
            places
        DROP COLUMN
            country_name
                CASCADE;

        ALTER TABLE
            countries
        DROP CONSTRAINT
            countries_pkey,
        DROP CONSTRAINT
            countries_code_key,
        ADD CONSTRAINT
            countries_pkey PRIMARY KEY (code);

        ALTER TABLE
            places
        ADD CONSTRAINT
            places_country_code_fkey
                FOREIGN KEY (country_code)
                REFERENCES countries (code);

        COMMIT;
    """,
    # 1 -> 2
    2: """
        BEGIN;

        ALTER TABLE
            places
        ADD COLUMN
            geom GEOMETRY('GEOMETRYCOLLECTION', 4326);

        COMMIT;
    """
}


@dataclasses.dataclass
class SchemaVersion(Base):
    """An ORM mapping to store the database schema’s version ."""

    update = sqlalchemy.Column(
        sqlalchemy.DateTime, server_default=sqlalchemy.sql.functions.now()
    )
    version = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=False
    )


class DatabaseSchemaUpdater:
    """Update the database schema if necessary."""
    @property
    def installed_version(self):
        """Current version."""
        with Session() as session:
            try:
                installed_version = (
                    session.execute(
                        sqlalchemy
                        .select(SchemaVersion)
                        .order_by(SchemaVersion.version.desc())
                        .limit(1)
                    )
                    .scalars()
                    .first()
                ).version
            except AttributeError:
                installed_version = 0
        return installed_version

    def update_to_latest(self):
        """Update to the latest schema version."""
        while self.installed_version < max(SCHEMA_UPDATES.keys()):
            with Session() as session, session.begin():
                next_version = self.installed_version + 1
                session.execute(SCHEMA_UPDATES[next_version])
                session.merge(SchemaVersion(version=next_version))
