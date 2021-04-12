#importing required packages
import boto3 
import json
import datetime         #to get timeStamp
import csv              #to make csv files
# from pprint import pprint

def lambda_handler(event, context):
    # TODO implement
    client=boto3.client("ec2")              #Making client variable to use boto3 library for ec2 service
    metric=boto3.client("cloudwatch")       #Making metric variable to use boto3 library for cloudwatch service
    s3=boto3.client('s3')                   #Making s3 variable to use boto3 library for s3 service

    
    # starting time of function
    time=datetime.datetime.utcnow() - datetime.timedelta(seconds=600)
    
    #getiing status of the ec2 instance in status variable
    status=client.describe_instance_status()
    
    
    #getting the instance Id
    instanceID=status['InstanceStatuses'][0]['InstanceId']
        
    
    
    #CPU Utilization Metrics retreival
    CpuUtilization=metric.get_metric_statistics(
       
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0047e8ead152024e4'
                },
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            EndTime=datetime.datetime.utcnow(),
            Period=300,
            Statistics=[
                'Average'
            ],
            
            Unit='Percent'
        )
        
    CPUperData=CpuUtilization['Datapoints'][0]['Average']           #utilization percentage
    CPUunit=CpuUtilization['Datapoints'][0]['Unit']                 #unit of the metric
    name1='CPUUtilization'                                          #name of the metric
        
    
    
    #disk reads Metrics retreival
    DiskReadops=metric.get_metric_statistics(
       
            Namespace='AWS/EC2',
            MetricName='DiskReadOps',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0047e8ead152024e4'
                },
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            EndTime=datetime.datetime.utcnow(),
            Period=300,
            Statistics=[
                'Average'
            ],
            
            Unit='Count'
        )
        
        
    DiskReadsdata=DiskReadops['Datapoints'][0]['Average']           
    DiskReadunit=DiskReadops['Datapoints'][0]['Unit']               #unit of the metric
    name2='DiskReadOps'                                             #name of the metric
    
    
    # diskWrite ops    
    DiskWriteops=metric.get_metric_statistics(
       
            Namespace='AWS/EC2',
            MetricName='DiskWriteOps',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0047e8ead152024e4'
                },
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            EndTime=datetime.datetime.utcnow(),
            Period=300,
            Statistics=[
                'Average'
            ],
            
            Unit='Count'
        )
        
        
    DiskWritedata=DiskWriteops['Datapoints'][0]['Average']
    DiskWriteunit=DiskWriteops['Datapoints'][0]['Unit']
    name3='DiskWriteOps'    
        
        
        
        
    #network Input
    NetworkIn=metric.get_metric_statistics(
       
            Namespace='AWS/EC2',
            MetricName='NetworkIn',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0047e8ead152024e4'
                },
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            EndTime=datetime.datetime.utcnow(),
            Period=300,
            Statistics=[
                'Average'
            ],
            
            Unit='Bytes'
        )
        
    NetworkIndata=NetworkIn['Datapoints'][0]['Average']
    NetworkInunit=NetworkIn['Datapoints'][0]['Unit']
    name4='NetworkIn'
        
        
        
        
    #NetworkOut  
    
    NetworkOut=metric.get_metric_statistics(
       
            Namespace='AWS/EC2',
            MetricName='NetworkOut',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0047e8ead152024e4'
                },
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            EndTime=datetime.datetime.utcnow(),
            Period=300,
            Statistics=[
                'Average'
            ],
            
            Unit='Bytes'
        )
    
    NetworkOutdata=NetworkOut['Datapoints'][0]['Average']
    NetworkOutunit=NetworkOut['Datapoints'][0]['Unit']
    name5='NetworkOut'
    
    
    #Cpu credit usage
    CpuCredits=metric.get_metric_statistics(
       
            Namespace='AWS/EC2',
            MetricName='CPUCreditUsage',
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': 'i-0047e8ead152024e4'
                },
            ],
            StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
            EndTime=datetime.datetime.utcnow(),
            Period=300,
            Statistics=[
                'Average'
            ],
            
            Unit='Count'
        )
        
    CPUcreditData=CpuCredits['Datapoints'][0]['Average']
    CPUcreditunit=CpuCredits['Datapoints'][0]['Unit']
    name6='CPUUtilization'
    
    
    
    #writing all the data in a csv file
    
    with open('/tmp/myCsv.csv','w')as f:
        thewriter=csv.writer(f)
        thewriter.writerow(['Time Stamp','Instance Id','Metric Name','Metric Value'])
        thewriter.writerow([time,instanceID,name1,f'{CPUperData} {CPUunit}'])
        thewriter.writerow([time,instanceID,name2,f'{DiskReadsdata} {DiskReadunit}'])
        thewriter.writerow([time,instanceID,name3,f'{DiskWritedata} {DiskWriteunit}'])
        thewriter.writerow([time,instanceID,name4,f'{NetworkIndata} {NetworkInunit}'])
        thewriter.writerow([time,instanceID,name5,f'{NetworkOutdata} {NetworkOutunit}'])
        thewriter.writerow([time,instanceID,name6,f'{CPUcreditData} {CPUcreditunit}'])
    f.close()
    
    bucketName='datagrokrtest123'                   #name of the s3 bucket 
    file=open('/tmp/myCsv.csv','rb')
    key=str(time)+'datagrokrtest'+'.csv'            #setting the name of the file according to the time stamp
    s3.put_object(Bucket=bucketName, Key=key, Body=file)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('file stored in S3 bucket')
    }
