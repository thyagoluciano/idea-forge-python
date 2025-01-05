import json

from src.core.reddit_client import RedditClient
from src.extractors.post_extractor import PostExtractor


def main():
    reddit_client = RedditClient()
    reddit_instance = reddit_client.get_reddit_instance()
    post_extractor = PostExtractor(reddit_instance)

    # Exemplo de uso para extrair posts de um subreddit
    subreddit_name = "SaaS"
    sort_criteria = "top"
    batch_size = 5
    days_ago = 1
    limit = 1

    for posts in post_extractor.extract_posts_from_subreddit(subreddit_name, sort_criteria, batch_size, days_ago, limit):
        for post in posts:
            print(f"Post ID: {post.id}, \nTitle: {post.title}, \nDescription: {post.text}, \nURL: {post.url} \nUpvotes: {post.ups}, \nComments: {post.num_comments}")
            for comment in post.comments:
                print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
            print("--------------------------")

    # Exemplo de uso para extrair posts por pesquisa
    # query = "eleições 2022"
    # sort_criteria = "relevance"
    # batch_size = 5
    # days_ago = 1
    #
    # for posts in post_extractor.extract_posts_from_search(query, sort_criteria, batch_size, days_ago):
    #     for post in posts:
    #         print(f"Post ID: {post.id}, Title: {post.title}, Upvotes: {post.ups}, Comments: {post.num_comments}")
    #         for comment in post.comments:
    #             print(f"   Comment Author: {comment.author}, Text: {comment.text}, Upvotes: {comment.ups}")
    #         print("--------------------------")


if __name__ == "__main__":
    main()
