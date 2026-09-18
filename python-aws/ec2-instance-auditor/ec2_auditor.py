import csv
import boto3
from datetime import datetime, timedelta, timezone

REQUIRED_TAGS = ['Name', 'Environment', 'Owner']

ec2 = boto3.client('ec2')
response = ec2.describe_instances()
# print(response)
cloudwatch = boto3.client('cloudwatch')

end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=14)

# Learning moment as new coder: the pattern is a dict key is always accessed with dict['KeyName']
# and a for loop goes through a list not a dict

csv_file = open('ec2_audit_report.csv', 'w', newline='')
writer = csv.writer(csv_file)
writer.writerow(['InstanceId', 'Status', 'MissingTags'])

for reservation in response['Reservations']:
# list of reservations, each time through this loop reservation becomes one dict
    for instance in reservation['Instances']:
    # nested inside the first loop, lsit of instanced inside that specific reservaton,
    # with every loop through instance becomes one dict
        instance_id = instance['InstanceId']
        # instance is a dict, pull out the value at the key 'InstanceID' and store in a variable
        state = instance['State']['Name']
        # state is a nested dict, chain two lookups, first getting the state dict, then name key
        tags = instance.get('Tags')

        if tags is None:
            tags = []

        existing_keys = []
        for tag in tags:
            key_name = tag['Key']
            existing_keys.append(key_name)

        missing_tags = []
        for required_tag in REQUIRED_TAGS:
            if required_tag not in existing_keys:
                missing_tags.append(required_tag)

        if len(missing_tags) == 0:
            tag_summary = 'No missing tags'
        else: 
            tag_summary = ', '.join(missing_tags) 


        if state == 'running':
            cw_response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {'Name': 'InstanceId', 'Value': instance_id}
                ],
                StartTime = start_time,
                EndTime = end_time,
                Period=86400,
                Statistics=['Average']
            )
            datapoints = cw_response['Datapoints']
            if len(datapoints) == 0:
                status = 'running - no CloudWatch data yet'
            else:
                cpu_averages = []
                for datapoint in datapoints:
                    avg = datapoint['Average']
                    cpu_averages.append(avg)

                overall_avg = sum(cpu_averages) / len(cpu_averages)

                if overall_avg <= 5:
                    status = 'idle - average CPU below 5%'
                else:
                    status = 'active - ' + str(overall_avg) + '% average CPU'

        elif state == 'stopped':
            status = 'stopped - review for termination'

        print(instance_id, '|', status, '|', tag_summary) 
        writer.writerow([instance_id, status, tag_summary]) # for my CSv 

csv_file.close()
# source venv/bin/activate



