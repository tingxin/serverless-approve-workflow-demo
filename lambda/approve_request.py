import imp
import boto3
import json
from botocore.exceptions import ClientError



def lambda_handler(event, context):
    print(event)
    rawPath = event['rawPath']

    token = rawPath.split('/')[-1]
    # TODO implement
    sfn = boto3.client('stepfunctions')

    params = {
            'output': '"Callback task completed successfully."',
            'taskToken': token
        }

    print(f'Calling Step Functions to complete callback task with params {json.dumps(params)}')

    try:
        sfn.send_task_success(**params)
    except Exception as e:
        print(str(e))
        raise e
