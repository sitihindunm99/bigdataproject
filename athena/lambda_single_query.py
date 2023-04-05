import boto3

# Query string to execute
query = "SELECT subreddit, sentiment, COUNT(*) AS sentiment_count\nFROM \"AwsDataCatalog\".\"cleaned-transformed-bigdata\".\"sentiment_analysistransformed\"\nGROUP BY subreddit, sentiment;"

# Database to execute the query against
DATABASE = 'cleaned-transformed-bigdata'

# Output location for query results
output='s3://bigdataproject-testing-raw-data/sentiment-analysis/'

def lambda_handler(event, context):
    # Initiate the Boto3 Client
    client = boto3.client('athena')

    # Start the query execution
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output
        }
    )

    # Return response after starting the query execution
    return response
