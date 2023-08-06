#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2020 Christoph Fink, University of Helsinki
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


"""Worker threads wrapping an APIDownloader."""


__all__ = ["TweetDownloaderThread"]


import datetime
import threading
import time

import dateparser
import sqlalchemy

from .engine import Session
from .models import MediaItem, Place, Tweet, User
from .timespan import TimeSpan
from .tweetdownloader import (
    MontlyQuotaExceededError,
    RateLimitExceededError,
    TweetDownloader,
)


class TweetDownloaderThread(threading.Thread):
    """Wraps a TweetDownloader to run in a separate thread."""

    def __init__(self, api_key_manager, todo_deque, done_queue):
        """
        Intialize an PhotoDownloaderThread.

        Args:
            api_key_manager: instance of an ApiKeyManager
            todo_deque: collections.deque that serves (search_term, TimeSpan)
                        tuples that need to be downloaded
            done_queue: queue.Queue into which to put (search_term, TimeSpan)
                        tuples that have been downloaded

        """
        super().__init__()

        self.count = 0

        self._api_key_manager = api_key_manager
        self._todo_deque = todo_deque
        self._done_queue = done_queue

        self.shutdown = threading.Event()

    def _save_batch_and_return_earliest_tweet_datetime(self, batch):
        earliest_tweet_created_at = datetime.datetime.now(datetime.timezone.utc)
        if "data" in batch:
            if "includes" in batch["data"]:
                self._save_includes(batch["data"]["includes"])
            for tweet in batch["data"]:
                self._save_tweet(tweet)
                self.count += 1
                earliest_tweet_created_at = min(
                    earliest_tweet_created_at, dateparser.parse(tweet["created_at"])
                )
        else:
            if "title" in batch and batch["title"] == "UsageCapExceeded":
                raise MontlyQuotaExceededError()
        return earliest_tweet_created_at

    def _save_includes(self, includes):
        if "media" in includes:
            for media_item in includes["media"]:
                self._save_media_item(self, media_item)
        if "places" in includes:
            for place in includes["places"]:
                self._save_place(place)
        if "tweets" in includes:
            for tweet in includes["tweets"]:
                self._save_tweet(tweet)
        if "users" in includes:
            for user in includes["users"]:
                self._save_user(user)

    def _save_media_item(self, media_item):
        return self._save_item(MediaItem, media_item)

    def _save_place(self, place):
        return self._save_item(Place, place)

    def _save_tweet(self, tweet):
        tweet = self._save_item(
            Tweet, tweet | {"search_term": self._current_search_term}
        )
        self.count += 1
        return tweet

    def _save_user(self, user):
        return self._save_item(User, user)

    def _save_item(self, model, data):
        try:
            with Session() as session, session.begin():
                return model.from_api_data(session, data)
        except sqlalchemy.exc.IntegrityError:
            # race conditions?!
            time.sleep(1.0)
            with Session() as session, session.begin():
                return model.from_api_data(session, data)

    def run(self):
        """Get TimeSpans off todo_deque and download photos."""
        while not self.shutdown.is_set():
            try:
                search_term, timespan = self._todo_deque.pop()
                self._current_search_term = search_term
            except IndexError:
                break

            tweet_downloader = TweetDownloader(
                search_term, timespan, self._api_key_manager
            )

            earliest_tweet = timespan.end  # haven’t covered anything yet
            try:
                for batch in tweet_downloader.batches:
                    earliest_tweet = min(
                        earliest_tweet,
                        self._save_batch_and_return_earliest_tweet_datetime(batch),
                    )

                    if self.shutdown.is_set():
                        timespan.start = earliest_tweet
                        break

            except RateLimitExceededError as exception:
                # report what we managed to download ...
                self._done_queue.put(
                    (search_term, TimeSpan(earliest_tweet, timespan.end))
                )

                # and remember what we haven’t been able to download
                timespan.end = earliest_tweet
                self._todo_deque.append((search_term, timespan))

                # then wait until we’re allowed again
                wait_seconds = (
                    exception.reset_time - datetime.datetime.now(datetime.timezone.utc)
                ).total_seconds()
                for _ in range(wait_seconds):
                    time.sleep(1)
                    if self.shutdown.is_set():
                        break
                else:
                    continue

            except MontlyQuotaExceededError as exception:
                # TODO: report error properly,
                # for now, re-raise exception to escalte to parent thread
                raise exception from None

            # … report to parent thread how much we worked
            self._done_queue.put((search_term, timespan))
