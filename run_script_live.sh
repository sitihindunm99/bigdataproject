#! /bin/bash

echo "Bash script executing"
/usr/bin/python3 ~/twitter_collector_live.py
/usr/bin/python3 ~/reddit_collector_live.py
# aws s3 cp ~/twitter_output.json s3://is459_group5_project/raw/twitter/twitter_output.json
# aws s3 cp ~/reddit_output_excel.xlsx s3://is459_group5_project/raw/reddit/reddit_output.xlsx
echo "Bash script executed"