import os
import sys
import random
import time

import boto3
from dotenv import dotenv_values

idf = random.randint(0, 100)
DOTENV_VALUES = dotenv_values('.env')
KeyName = DOTENV_VALUES['KeyName']
SecurityGroups = DOTENV_VALUES['SecurityGroups']
Prod_Instance_Tag = f'prod_server_docker_{idf}'
Dev_Instance_Tag = f'dev_server_docker_{idf}'
Image_ID = 'ami-0fd303abd14827300'
InstanceType = 't3.medium'
prod_cfg_file_path = os.getcwd() + '/prod-cloud-cfg.txt'
dev_cfg_file_path = os.getcwd() + '/dev-cloud-cfg.txt'

ec2 = boto3.resource('ec2')

if os.path.isfile(prod_cfg_file_path):
    ProdUserData = open(prod_cfg_file_path, 'r').read()
else:
    sys.exit("prod-cloud-cfg.txt is not in current working directory.")

if os.path.isfile(dev_cfg_file_path):
    DevUserData = open(dev_cfg_file_path, 'r').read()
else:
    sys.exit("dev_cfg_file_path is not in current working directory.")

prod_instances = ec2.create_instances(
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
            'Value': Prod_Instance_Tag,
         }],
    }
    ],
    UserData=ProdUserData,
    )

dev_instances = ec2.create_instances(
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
            'Value': Dev_Instance_Tag,
         }],
    }
    ],
    UserData=DevUserData,
    )

print('Sleeping for 10 seconds..\n')
time.sleep(10)
prod_instance = prod_instances[0]
dev_instance = dev_instances[0]
print('Waiting for both prod and dev instances to be created..')

for instance, name in zip([prod_instance, dev_instance], ['Prod', 'Dev']):
    instance_exists = instance.wait_until_exists()
    instance.reload()
    print(f"{name} instance with id={instance.instance_id}, public_ip_address={instance.public_ip_address} "
          f"and private_ip_address={instance.private_ip_address} is created.")
    print(f'\nWaiting for {name} instance to start running..')
    running = instance.wait_until_running()
    print(f'{name} instance is running!')
