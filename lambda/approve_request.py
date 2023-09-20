import boto3
import json
from botocore.exceptions import ClientError
import urllib.parse

html_response = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8"> <!-- 设置字符编码为 UTF-8 -->
        <title>申请批复状态</title>
    </head>
    <body>
        <h1>{0}!</h1>
    </body>
    </html>
"""


def lambda_handler(event, context):
    print(event)
    rawQueryString = event['rawQueryString']


    # 对编码后的查询字符串进行 URL 解码
    decoded_query = urllib.parse.unquote(rawQueryString)
    if len(decoded_query) <=5:
        return {
            'statusCode': 404,
            'body': json.dumps('miss rawQueryString')
        }
    
    
    query_parts = decoded_query.split('&')
    token = query_parts[0][len("token="):]
    behaviour = query_parts[1][len("behaviour="):]
    print(f"token={token} behaviour = {behaviour}")

    if not token:
        return {
            'statusCode': 404,
            'body': json.dumps('miss task token')
        }
    # TODO implement
    sfn = boto3.client('stepfunctions')
    print(token)
    params = {
                'output': json.dumps({
                    "behaviour":True if behaviour == '1' else False,
                }),
                'taskToken': token
            }
    try:
        if behaviour == '1':
           
            sfn.send_task_success(**params)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': html_response.format('您已经批准了该申请！')
            }
        else:
            sfn.send_task_failure(**params)
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html',
                },
                'body': html_response.format('您已经拒绝了该申请！')
            }
    except Exception as e:
        print(str(e))
        raise e

