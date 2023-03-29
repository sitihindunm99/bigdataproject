import praw
import pandas as pd

# Interact with reddit praw API
reddit = praw.Reddit(client_id='pPZ0qlVkD3x10Lax-FnXNQ', client_secret='gMYonicoK5AxBIW-sWb1I8FbUsgiwA', user_agent='Crypto WebScraping')

def subreddit_and_keyword_scraper(subreddit, keyword, submissions):
    # Filter based on title, post content as well as comments
    # for submission in reddit.subreddit(subreddit).search(keyword, limit=None): 

    # Filter based on title and post content
    for submission in reddit.subreddit(subreddit).search('title:"{}" selftext:"{}"'.format(keyword, keyword)):
        submission.comments.replace_more(limit=None)

        submissions.append([submission.title, submission.score, submission.id, submission.subreddit, keyword, submission.num_comments, submission.selftext])

        for comment in submission.comments.list():
            submissions.append([submission.title, submission.score, submission.id, submission.subreddit, keyword, submission.num_comments, comment.body])


def run_reddit_collector():

    submissions = []

    subreddit_and_keyword_scraper('ChatGPT', 'student', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'class', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'education', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'college', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'school', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'assignment', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'final', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'course', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'university', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'elementary', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'highschool', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'teacher', submissions)
    subreddit_and_keyword_scraper('ChatGPT', 'educator', submissions)

    subreddit_and_keyword_scraper('OpenAI', 'student', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'class', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'education', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'college', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'school', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'assignment', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'final', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'course', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'university', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'elementary', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'highschool', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'teacher', submissions)
    subreddit_and_keyword_scraper('OpenAI', 'educator', submissions)

    subreddit_and_keyword_scraper('Teachers', 'ChatGPT', submissions)

    submissions = pd.DataFrame(submissions,columns=['title', 'score', 'id', 'subreddit', 'keyword','num_comments','comment'])


    # Save to a csv file
    submissions.to_csv('reddit_output_new.csv', encoding='utf-8', index=False)


run_reddit_collector()