#! /bin/bash

echo "Bash script executing"
/usr/bin/python3 ~/twitter/twitter_collector_live.py
/usr/bin/python3 ~/reddit/reddit_collector_live.py
/usr/bin/python3 ~/s3_loader_live.py
echo "Bash script executed"