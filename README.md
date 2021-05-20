Fetch_EC2_info.py
    Used lambda function that triggers every hour and fetches running ec2 instance's computaional details and save it as a csv file to a S3 bucket.
    
Check_for_S3_tags.py
    used lambda function that triggers every time a S3 bucket is created and looks for necessary tags, if the tags are missing it deletes the bucket.
