import os
import sys
import random
import time

import boto3

ec2 = boto3.resource('ec2')

instance_tag = f'prod_server_{random.randint(0, 100)}'
image_id = 'ami-0fd303abd14827300'
cfg_file_path = os.getcwd() + '/cloud-cfg.txt'

if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path, 'r').read()
else:
    sys.exit("cloud-cfg.txt is not in current working directory.")

instance = ec2.create_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName='hardy_ec2_key',
        SecurityGroups=['hardy_sg_eunorth1'],
        TagSpecifications=[
        {
	        'ResourceType': 'instance',
	         'Tags': [{
	         	'Key': 'Name',
	            'Value': instance_tag,
	         }],
        }
        ],
        UserData=userdata,
        )

print('Sleeping for 10 seconds..')
time.sleep(10)

instance = instance[0]
state = instance.state
while state['Name'] != 'running':
    print(f"Current state: {instance.state['Code']} {instance.state['Name']}")
    time.sleep(5)

print(f"\n\nFinal state: {instance.state['Code']} {instance.state['Name']}")
