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

"""A Tweet ORM data model."""


__all__ = ["Tweet"]


import dataclasses

import dateparser
import geoalchemy2
import shapely
import sqlalchemy
import sqlalchemy.ext.associationproxy
import sqlalchemy.orm

from .base import Base
from .conversation import Conversation
from .hashtag import Hashtag
from .language import Language
from .mediaitem import MediaItem
from .place import Place
from .searchterm import SearchTerm
from .url import Url
from .user import User


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet


@dataclasses.dataclass
class TweetReferenceType(Base):
    """A media type ORM data model."""

    reference_type = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)


@dataclasses.dataclass
class TweetReference(Base):
    """An ORM model to represent the relationship between two tweets."""

    referenced_tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )
    referenced_tweet = sqlalchemy.orm.relationship(
        "Tweet", foreign_keys=[referenced_tweet_id]
    )

    referencing_tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )
    referencing_tweet = sqlalchemy.orm.relationship(
        "Tweet", foreign_keys=[referencing_tweet_id]
    )

    reference_type_reference_type = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("tweet_reference_types.reference_type")
    )
    reference_type = sqlalchemy.orm.relationship("TweetReferenceType")


@dataclasses.dataclass
class Tweet(Base):
    """A Tweet ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True))
    possibly_sensitive = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.Text)

    geom = sqlalchemy.Column(geoalchemy2.Geometry("POINT", 4326))

    author_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id")
    )
    author = sqlalchemy.orm.relationship(
        "User", back_populates="tweets", foreign_keys=[author_id]
    )

    in_reply_to_user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id")
    )
    in_reply_to = sqlalchemy.orm.relationship(
        "User", foreign_keys=[in_reply_to_user_id]
    )

    conversation_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("conversations.id")
    )
    conversation = sqlalchemy.orm.relationship("Conversation", back_populates="tweets")

    language_language = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("languages.language")
    )
    language = sqlalchemy.orm.relationship("Language", back_populates="tweets")

    place_id = sqlalchemy.Column(sqlalchemy.Text, sqlalchemy.ForeignKey("places.id"))
    place = sqlalchemy.orm.relationship("Place", back_populates="tweets")

    referenced_tweets = sqlalchemy.orm.relationship(
        "TweetReference",
        primaryjoin="(Tweet.id==TweetReference.referencing_tweet_id)",
        back_populates="referencing_tweet",
    )
    referencing_tweets = sqlalchemy.orm.relationship(
        "TweetReference",
        primaryjoin="(Tweet.id==TweetReference.referenced_tweet_id)",
        back_populates="referenced_tweet",
    )

    hashtags = sqlalchemy.orm.relationship(
        "Hashtag", secondary="hashtag_tweet_associations", back_populates="tweets"
    )
    media = sqlalchemy.orm.relationship(
        "MediaItem", secondary="media_item_tweet_associations", back_populates="tweets"
    )
    mentions = sqlalchemy.orm.relationship(
        "User", secondary="mentions", back_populates="mentioned"
    )
    urls = sqlalchemy.orm.relationship(
        "Url", secondary="url_tweet_associations", back_populates="tweets"
    )

    search_terms = sqlalchemy.orm.relationship(
        "SearchTerm",
        secondary="search_term_tweet_associations",
        back_populates="tweets",
    )

    @classmethod
    def from_api_data(cls, session, data):
        """Instantiate from “raw” API response data."""
        if cls.pseudonymise_identifiers():
            data = cls._pseudonymise_api_data(data)

        instance = session.merge(cls(id=data["id"]))

        instance.created_at = dateparser.parse(data["created_at"])
        instance.possibly_sensitive = data["possibly_sensitive"]
        instance.text = data["text"]

        if (
            "geo" in data
            and "coordinates" in data["geo"]
            and "coordinates" in data["geo"]["coordinates"]
        ):
            instance.geom = shapely.geometry.Point(
                *data["geo"]["coordinates"]["coordinates"]
            ).wkt

        if "geo" in data and "place_id" in data["geo"]:
            instance.place = session.merge(Place(id=data["geo"]["place_id"]))

        instance.author = session.merge(User(id=data["author_id"]))

        if "in_reply_to_user_id" in data:
            instance.in_reply_to = session.merge(User(id=data["in_reply_to_user_id"]))

        if "conversation_id" in data:
            instance.conversation = session.merge(
                Conversation(id=data["conversation_id"])
            )

        instance.language = session.merge(Language(language=data["lang"]))

        if "referenced_tweets" in data:
            for referenced_tweet in data["referenced_tweets"]:
                tweet_reference = session.merge(
                    TweetReference(
                        referenced_tweet_id=referenced_tweet["id"],
                        referencing_tweet_id=instance.id,
                        reference_type=session.merge(
                            TweetReferenceType(
                                referenced_tweet["type"]
                            )
                        )
                    )
                )
                if tweet_reference not in instance.referenced_tweets:
                    instance.referenced_tweets.append(tweet_reference)

        if "attachments" in data and "media_keys" in data["attachments"]:
            for media_key in data["attachments"]["media_keys"]:
                media_item = session.merge(MediaItem(media_key=media_key))
                if media_item not in instance.media:
                    instance.media.append(media_item)

        if "entities" in data and "mentions" in data["entities"]:
            for mention in data["entities"]["mentions"]:
                # if everything went in order, then we should already
                # have saved the user (mention is by username)
                mentioned_user = (
                    session.execute(
                        sqlalchemy
                        .select(User(username=mention["username"]))
                        .limit(1)
                    )
                    .scalars
                    .first()
                )
                if mentioned_user and (mentioned_user not in instance.mensions):
                    instance.mentions.append(mentioned_user)

        if "entities" in data and "hashtags" in data["entities"]:
            for hashtag in data["entities"]["hashtags"]:
                hashtag = session.merge(Hashtag(hashtag=hashtag))
                if hashtag not in instance.hashtags:
                    instance.hashtags.append(hashtag)

        if "entities" in data and "urls" in data["entities"]:
            for url in data["entities"]["urls"]:
                url = session.merge(Url(url=url))
                if url not in instance.urls:
                    instance.urls.append(url)

        search_term = session.merge(SearchTerm(search_term=data["search_term"]))
        if search_term not in instance.search_terms:
            instance.search_terms.append(search_term)

        return session.merge(instance)

    @classmethod
    def _pseudonymise_api_data(cls, data):
        for identifier in [
            "id",
            "author_id",
            "in_reply_to_user_id",
            "conservation_id",
        ]:
            try:
                data[identifier] = cls.integer_hash(data[identifier])
            except KeyError:
                pass

        if "referenced_tweets" in data:
            for i in range(len(data["referenced_tweets"])):
                data["referenced_tweets"][i]["id"] = cls.integer_hash(
                    data["referenced_tweets"][i]["id"]
                )

        for identifier in []:
            data[identifier] = None

        return data
