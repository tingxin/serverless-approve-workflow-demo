############
# 请用客户端通过http post方法调用
# body 类似如下:
# {
#   "title": "休假申请",
#    "request": "最近身体不舒服，请求休假3天，请老板批准"
#   }
############
import json
import boto3

sfn_arn = 'arn:aws:states:ap-northeast-1:515491257789:stateMachine:WaitForCallbackStateMachine-Q9Mt6F3ZNMin'

def lambda_handler(event, context):
    # 从事件中提取 POST 请求的数据
    if 'body' in event:
        data = json.loads(event['body'])
    else:
        data = {}

    sfn = boto3.client('stepfunctions')

    response = sfn.start_execution(
        stateMachineArn=sfn_arn,
        input=event['body']
    )

    result = dict()
    result['headers'] = {
            'Content-Type': 'application/json',
    }
    if 'executionArn' in response:
        result['statusCode'] = 200
        result['body'] = {
            'msg':'申请提交成功！'
        }
        print("Execution ARN:", response['executionArn'])
    else:
        result['statusCode'] = 404
        result['body'] = {
            'msg':'申请提交失败，请联系管理员！'
        }

    # 返回响应
    return result