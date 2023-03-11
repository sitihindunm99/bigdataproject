Steps to create instance, transfer file, install dependencies and run scraper
1. Create EC2 instance (use everything free-tier like linux image, default SG etc) & generate key pem if needed (chmod 400 to reduce the permission for key pem)
2. Copy scraper file from local to instance using command "scp -i <path to pemfile.pem> <path to file to transfer> <user>@<public DNS>:<directory to transfer to>"
e.g. scp -i ~/Documents/Y4S2/IS459/project/big-data-scraper.pem ~/Documents/Y4S2/IS459/project/twitter_collector.py ec2-user@ec2-3-235-17-213.compute-1.amazonaws.com:~/
3. Gain remote access to instance using command "ssh -i <path to pemfile.pem> <username>@<public DNS>" (default username is ec2-user)
e.g. ssh -i big-data-scraper.pem ec2-user@ec2-3-235-17-213.compute-1.amazonaws.com
4. Verify that scraper has been copied into instance by running command "ls"
4. Install python for instance using command "sudo yum install python3"
5. Install relevent dependencies using command "sudo pip3 install <module>"
e.g. sudo pip3 install requests
6. Run scraper using command "python3 <scraper file>"
e.g. python3 twitter_collector.py

Extra:
- if sudo yum install does not work, try sudo apt-get install