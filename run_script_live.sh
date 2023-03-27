#! /bin/bash

echo "Bash script executing"
~/opt/anaconda3/bin/python ~/Desktop/bigdataproject/twitter_collector.py
~/opt/anaconda3/bin/python ~/Desktop/bigdataproject/s3_loader.py
echo "Bash script executed"