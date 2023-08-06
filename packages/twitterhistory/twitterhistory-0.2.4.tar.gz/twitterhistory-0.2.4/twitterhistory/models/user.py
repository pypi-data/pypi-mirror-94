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

"""A Twitter User ORM data model."""


__all__ = ["User"]


import dataclasses

import dateparser
import sqlalchemy
import sqlalchemy.orm

from .base import Base
from .hashtag import Hashtag
from .url import Url

# from .tweet import Tweet
# (this would be a circular import, that’s why now inside User.from_api_data())


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place


class Mention(Base):
    """A many-to-many relation table between users and tweets."""

    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"), primary_key=True
    )


@dataclasses.dataclass
class User(Base):
    """A Twitter User ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.Text)
    name = sqlalchemy.Column(sqlalchemy.Text)
    description = sqlalchemy.Column(sqlalchemy.Text)
    location = sqlalchemy.Column(sqlalchemy.Text)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))

    protected = sqlalchemy.Column(sqlalchemy.Boolean)
    verified = sqlalchemy.Column(sqlalchemy.Boolean)

    pinned_tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id")
    )
    pinned_tweet = sqlalchemy.orm.relationship("Tweet", foreign_keys=[pinned_tweet_id])

    profile_image_url_url = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("urls.url")
    )
    profile_image_url = sqlalchemy.orm.relationship("Url")

    hashtags = sqlalchemy.orm.relationship(
        "Hashtag", secondary="hashtag_user_associations", back_populates="users"
    )
    urls = sqlalchemy.orm.relationship(
        "Url", secondary="url_user_associations", back_populates="users"
    )

    tweets = sqlalchemy.orm.relationship(
        "Tweet", back_populates="author", foreign_keys="[Tweet.author_id]"
    )

    mentioned = sqlalchemy.orm.relationship(
        "Tweet", secondary="mentions", back_populates="mentions"
    )

    @classmethod
    def from_api_data(cls, session, data):
        """Instantiate from “raw” API response data."""
        from .tweet import Tweet

        if cls.pseudonymise_identifiers():
            data = cls._pseudonymise_api_data(data)

        instance = session.merge(cls(data["id"]))

        for key in [
            "id",
            "username",
            "name",
            "description",
            "location",
            "protected",
            "verified",
        ]:
            setattr(instance, key, data[key])

        instance.created_at = dateparser.parse(data["created_at"])
        instance.pinned_tweet = session.merge(Tweet(id=int(data["pinned_tweet_id"])))
        instance.profile_image_url = session.merge(Url(url=data["profile_image_url"]))

        if (
            "entities" in data
            and "description" in data["entities"]
            and "hashtags" in data["entities"]["description"]
        ):
            for hashtag in data["entities"]["description"]["hashtags"]:
                hashtag = session.merge(Hashtag(hashtag=hashtag))
                if hashtag not in instance.hashtags:
                    instance.hashtags.append(hashtag)

        if (
            "entities" in data
            and "url" in data["entities"]
            and "urls" in data["entities"]["url"]
        ):
            for url in data["entities"]["url"]["urls"]:
                url = session.merge(Url(url=url))
                if url not in instance.urls:
                    instance.urls.append(url)

        return session.merge(instance)

        @classmethod
        def _pseudonymise_api_data(cls, data):
            for identifier in [
                "id",
                "pinned_tweet_id",
            ]:
                try:
                    data[identifier] = cls.integer_hash(data[identifier])
                except KeyError:
                    pass

            for identifier in [
                "username",
                "name",
                "description",
            ]:
                data[identifier] = None

            return data
