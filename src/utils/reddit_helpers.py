# utils/reddit_helpers.py

from praw import Reddit
from praw.models import Subreddit
from datetime import datetime, timedelta


class RedditHelpers:

    @staticmethod
    def get_listing_generator_by_sort(reddit_instance: Reddit, subreddit: Subreddit, sort_criteria: str,
                                      start_date: datetime = None, end_date: datetime = None):
        """
        Returns the Listing Generator based on the sort criteria for subreddits.
        """
        listing = None
        if sort_criteria == "hot":
            listing = subreddit.hot()
        elif sort_criteria == "top":
            listing = subreddit.top()
        elif sort_criteria == "new":
            listing = subreddit.new()
        elif sort_criteria == "controversial":
            listing = subreddit.controversial()
        else:
            raise ValueError(
                "Invalid sort criteria. Choose from 'hot', 'top', 'new', 'controversial'."
            )

        return RedditHelpers.filter_by_date(listing, start_date, end_date)

    @staticmethod
    def get_search_listing_generator_by_sort(reddit_instance: Reddit, query: str, sort_criteria: str,
                                             start_date: datetime = None, end_date: datetime = None):
        """
        Returns the Listing Generator based on the sort criteria for search.
        """
        listing = None
        if sort_criteria == "relevance":
            listing = reddit_instance.subreddit("all").search(query, sort="relevance")
        elif sort_criteria == "top":
            listing = reddit_instance.subreddit("all").search(query, sort="top")
        elif sort_criteria == "new":
            listing = reddit_instance.subreddit("all").search(query, sort="new")
        elif sort_criteria == "comments":
            listing = reddit_instance.subreddit("all").search(query, sort="comments")
        else:
            raise ValueError(
                "Invalid search sort criteria. Choose from 'relevance', 'top', 'new', 'comments'."
            )

        return RedditHelpers.filter_by_date(listing, start_date, end_date)

    @staticmethod
    def filter_by_date(listing, start_date: datetime = None, end_date: datetime = None):
        """
        Filters the listing by date range.
        """
        if start_date or end_date:
            return (
                post for post in listing
                if (not start_date or datetime.fromtimestamp(post.created_utc) >= start_date) and
                   (not end_date or datetime.fromtimestamp(post.created_utc) <= end_date)
            )

        return listing
