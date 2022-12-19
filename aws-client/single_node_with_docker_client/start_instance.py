import os
import sys
import random
import time

import boto3
from dotenv import dotenv_values

DOTENV_VALUES = dotenv_values('.env')
KeyName = DOTENV_VALUES['KeyName']
SecurityGroups = DOTENV_VALUES['SecurityGroups']
Instance_Tag = f'prod_server_docker_{random.randint(0, 100)}'
Image_ID = 'ami-0fd303abd14827300'
InstanceType = 't3.medium'
cfg_file_path = os.getcwd() + '/cloud-cfg.txt'

ec2 = boto3.resource('ec2')

if os.path.isfile(cfg_file_path):
    UserData = open(cfg_file_path, 'r').read()
else:
    sys.exit("cloud-cfg.txt is not in current working directory.")

instances = ec2.create_instances(
        ImageId=Image_ID,
        MinCount=1,
        MaxCount=1,
        InstanceType=InstanceType,
        KeyName=KeyName,
        SecurityGroups=[SecurityGroups],
        TagSpecifications=[
        {
	        'ResourceType': 'instance',
	         'Tags': [{
	         	'Key': 'Name',
	            'Value': Instance_Tag,
	         }],
        }
        ],
        UserData=UserData,
        )

print('Sleeping for 10 seconds..\n')
time.sleep(10)
instance = instances[0]
print('Waiting for instance to be created..')
instance_exists = instance.wait_until_exists()
instance.reload()
print(f"Instance with id={instance.instance_id} and public_ip_address={instance.public_ip_address} is created.")
print('\nWaiting for instance to start running..')
running = instance.wait_until_running()
print('Instance is running!')
