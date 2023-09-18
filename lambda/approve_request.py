import imp
from operator import itemgetter
import boto3
import json
from botocore.exceptions import ClientError


table_name = 'approve_workflow_rec2'

def read_status(key:str):
    # 创建 DynamoDB 客户端
    dynamodb = boto3.client('dynamodb')

 
    # 准备要检索的主键值
    key_to_retrieve = {
        'key': {'S': key}
    }

    try:
        # 从 DynamoDB 表中检索数据
        response = dynamodb.get_item(
            TableName=table_name,
            Key=key_to_retrieve
        )
        item = response.get('Item', {})
        if item:
            print("Retrieved item:", item)
        else:
            print("Item not found.")
        return item['token']['S']
    except Exception as e:
        print("Error retrieving item:", e)  
    return None

def lambda_handler(event, context):
    print(event)
    rawQueryString = event['rawQueryString']
    if len(rawQueryString) <=5:
        return {
            'statusCode': 404,
            'body': json.dumps('miss rawQueryString')
        }
    
    
    query_parts = rawQueryString.split('&')
    uuidp=query_parts[0]
    behaviourp=query_parts[1]
    
    uuidpp = uuidp.split('=')
    uuid = uuidpp[1]
    
    behaviourpp = behaviourp.split('=')
    behaviour = behaviourpp[1]
    print(f"token={uuid} behaviour = {behaviour}")

    token = read_status(uuid)
    if not token:
        return {
            'statusCode': 404,
            'body': json.dumps('miss task token')
        }
    # TODO implement
    sfn = boto3.client('stepfunctions')
    print(token)

    try:
        if behaviour == '1':
            params = {
                'output': '"批准流程."',
                'taskToken': token
            }
            sfn.send_task_success(**params)
            print(params)
            return {
                'statusCode': 200,
                'body': json.dumps('已批准')
            }
        else:
            params = {
                'error': '"拒绝流程."',
                'taskToken': token
            }
            sfn.send_task_failure(**params)
            print(params)
            return {
                'statusCode': 200,
                'body': json.dumps('已拒绝')
            }
    except Exception as e:
        print(str(e))
        raise e

