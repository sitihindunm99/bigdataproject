import boto3

def run_loader():

    # Push json files into S3 bucket
    s3 = boto3.resource('s3')
    s3.Bucket('scraper-data').upload_file("twitter/twitter_output.json", "twitter_output.json")

run_loader()
