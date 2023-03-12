Steps to setup project:
1. Create a .env file containing bearer=<bearer token> (Retrieve from Asnawi)

Steps to create instance, transfer file, install dependencies and run scraper:
1. Create EC2 instance (use everything free-tier like linux image, default SG etc) & generate key pem if needed (chmod 400 to reduce the permission for key pem)
2. Copy scraper file (twitter_collector.py), env file (.env) and topic file (topic.txt) from local file system to instance file system using command "scp -i <path to pemfile.pem> <path to file to transfer> <user>@<public DNS>:<directory to transfer to>"
e.g. scp -i "big-data-scraper.pem" topic.txt ec2-user@ec2-54-236-62-41.compute-1.amazonaws.com:~/ 
3. Gain remote access to instance using command "ssh -i <path to pemfile.pem> <username>@<public DNS>" (default username is ec2-user)
e.g. ssh -i "big-data-scraper.pem" ec2-user@ec2-54-236-62-41.compute-1.amazonaws.com 
4. Verify that files have been copied into instance by running command "ls"
4. Install python for instance using command "sudo yum install python3"
5. Install relevant dependencies using command "sudo pip3 install <module>" (python-dotenv, requests)
e.g. sudo pip3 install requests
6. Run scraper using command "python3 <scraper file>"
e.g. python3 twitter_collector.py
7. Exit the instance by using command "exit"

Steps to create S3 bucket, run loader:
1. Create S3 bucket (use everything free-tier)
2. Under IAM > Roles, create new role and attach AmazonS3FullAccess policy
3. Under EC2 instance created above, click on Actions > Security > Modify IAM Role. Click on the newly created role. This allows the EC2 instance to have access to S3 bucket
4. Copy loader file (s3_loader.py) from local file system to instance file system using command "scp -i <path to pemfile.pem> <path to file to transfer> <user>@<public DNS>:<directory to transfer to>"
e.g. scp -i "big-data-scraper.pem" s3_loader.py ec2-user@ec2-54-236-62-41.compute-1.amazonaws.com:~/ 
5. Gain remote access to instance using command "ssh -i <path to pemfile.pem> <username>@<public DNS>" (default username is ec2-user)
e.g. ssh -i "big-data-scraper.pem" ec2-user@ec2-54-236-62-41.compute-1.amazonaws.com 
6. Verify that files have been copied into instance by running command "ls"
7. Install relevant dependencies using command "sudo pip3 install <module>" (boto3)
e.g. sudo pip3 install boto3
8. Run loader using command "python3 <scraper file>"
e.g. python3 s3_loader.py
9. Exit the instance by using command "exit"

Extra:
- if sudo yum install does not work, try sudo apt-get install