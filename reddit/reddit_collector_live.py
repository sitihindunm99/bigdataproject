import praw
import pandas as pd
from openpyxl import workbook # pip install this

# Interact with reddit praw API
reddit = praw.Reddit(client_id='pPZ0qlVkD3x10Lax-FnXNQ', client_secret='gMYonicoK5AxBIW-sWb1I8FbUsgiwA', user_agent='Crypto WebScraping')

def subreddit_and_keyword_scraper(subreddit, keyword, submissions):
#     for submission in reddit.subreddit(subreddit).search(keyword, limit=5000): 
    for submission in reddit.subreddit(subreddit).search('title:"{}" selftext:"{}"'.format(keyword, keyword)):
        submission.comments.replace_more(limit=None)
        print(submission.selftext)

        submissions.append([submission.title, submission.score, submission.id, submission.subreddit, keyword, submission.num_comments, submission.selftext])

        for comment in submission.comments.list():
            submissions.append([submission.title, submission.score, submission.id, submission.subreddit, keyword, submission.num_comments, comment.body])
        print(subreddit)
        print(keyword)


def run_reddit_collector():

    subreddits = {"tech":["ChatGPT", "OpenAI"], "edu": ["Teachers", "Student", "College", "Highschool", "Professors", "CSEducation", "Internationalteachers"]}
    topics = {"tech":["ChatGPT"], "edu":["student", "class", "education", "college", "school","assignment", "final", "course", "university", "elementary", "highschool", "teacher", "educator", "professor", "undergraduate", "learn"]}

    submissions = []

    for subreddit in subreddits["tech"]:
        for topic in topics["edu"]:
            subreddit_and_keyword_scraper(subreddit, topic, submissions)

    for subreddit in subreddits["edu"]:
        for topic in topics["tech"]:
            subreddit_and_keyword_scraper(subreddit, topic, submissions)


    submissions = pd.DataFrame(submissions,columns=['title', 'score', 'id', 'subreddit', 'topic','num_comments','comment'])


    # Save to a excel file
    submissions.to_excel('reddit_output_excel.xlsx', index=False)
