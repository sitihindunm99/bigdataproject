import boto3
import time
s3 = boto3.resource("s3")

# Query string to execute
subreddit_sentiment_query = "SELECT subreddit, sentiment, COUNT(*) AS sentiment_count\nFROM \"AwsDataCatalog\".\"cleaned-transformed-bigdata\".\"sentiment_analysistransformed\"\nGROUP BY subreddit, sentiment;"

overall_sentiment_query = "SELECT sentiment, COUNT(*) as sentiment_count\nFROM \"AwsDataCatalog\".\"cleaned-transformed-bigdata\".\"sentiment_analysistransformed\"\nGROUP BY sentiment;"

education_level_query = "SELECT topic, sentiment, COUNT(*) AS sentiment_count\nFROM \"AwsDataCatalog\".\"cleaned-transformed-bigdata\".\"sentiment_analysistransformed\"\nWHERE topic IN ('elementary', 'highschool', 'college', 'university')\nGROUP BY topic, sentiment;"

queries = {"subreddit_sentiment_query": subreddit_sentiment_query, 
            "overall_sentiment_query" : overall_sentiment_query, 
            "education_level_query": education_level_query}

def lambda_handler(event, context):
    # Start the query execution
    for filename, actual_query in queries.items():
        run_athena_query(actual_query, filename)

def run_athena_query(actual_query, filename):

    # Initiate the Boto3 Client
    client = boto3.client('athena')
    
    # Database to execute the query against
    DATABASE = 'cleaned-transformed-bigdata'
    
    # Output location for query results
    output='s3://bigdataproject-testing-raw-data/sentiment-analysis/'
        
    queryStart = client.start_query_execution(
        QueryString=actual_query,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': output
        }
    )
    
    queryId = queryStart['QueryExecutionId']
    time.sleep(3)
    queryLoc = "bigdataproject-testing-raw-data/sentiment-analysis/" + queryId + ".csv"

    #destination location and file name
    s3.Object("bigdataproject-testing-raw-data", "sentiment-analysis/" + filename + ".csv").copy_from(CopySource = queryLoc)
    
    #deletes Athena generated csv and it's metadata file
    response = s3.Object('bigdataproject-testing-raw-data','sentiment-analysis/'+queryId+".csv").delete()
    response = s3.Object('bigdataproject-testing-raw-data','sentiment-analysis/'+queryId+".csv.metadata").delete()
    print(actual_query + ' csv generated')


    # Return response after starting the query execution
    return response
