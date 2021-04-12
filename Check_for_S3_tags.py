import json
import boto3
from pprint import pprint
def lambda_handler(event, context):
    
    
    flag=0                                                  #variable to store status of tag found or not
   
    s3=boto3.client('s3')                                   #creating s3 object to access the bucket
    
    nameofBucket=event['requestParameters']['bucketName']   #storing name of bucket created from event that triggered it
    
    # adding exception handling to check if bucket is tagged or not
    try:
        taglist=s3.get_bucket_tagging(
        Bucket=nameofBucket,
        ExpectedBucketOwner='971082289164 '
        )
        
        #storing list of tags to list_of_tags 
        list_of_tags=taglist['TagSet']
        
        for key in list_of_tags:                            #traversing list of tags to search for Environment t
            if(key['Key']=='Environment')
                flag=1                                      #if tag is found changing value of flag to 1
                
        if(flag==0)                                         # tag not found
           s3.delete_bucket(
               Bucket=nameofBucket,
               ExpectedBucketOwner='971082289164'
               ) 
        
    
    except Exception as e:
        s3.delete_bucket(
               Bucket=nameofBucket,
               ExpectedBucketOwner='971082289164'
               ) 
    
    
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
