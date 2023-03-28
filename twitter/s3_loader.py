import boto3

def run_loader():

    # Get the topics from topic.txt
    topics = []
    with open('./topic.txt') as f:
        topics = [line.rstrip() for line in f]

    # Push json files into S3 bucket
    s3 = boto3.resource('s3')
    for topic in topics:
        s3.Bucket('scraper-data').upload_file(f'./{topic.replace(" ", "_")}.json', f'./{topic.replace(" ", "_")}.json')

run_loader()