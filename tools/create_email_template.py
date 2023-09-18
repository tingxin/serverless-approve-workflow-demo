import imp
import boto3
import json
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


html_template = """
<html>
<head></head>
<body>
  <h3>{{content}}</h3>
  <p>点击这里 <a href="{{link1}}">批准申请</a>.</p>
  <p>点击这里 <a href="{{link2}}">拒绝申请</a>.</p>
</body>
</html>
"""

text_template = """
{{content}}\r\n
点击这里批准申请:\r\n
{{link1}}
点击这里拒绝申请:\r\n
{{link2}}
"""

ses = boto3.client('ses')

response = ses.create_template(
    
        Template={
            "TemplateName": "approve_workflow_template2",
            "SubjectPart": "{{subject}}!",
            "HtmlPart": html_template,
            "TextPart": text_template
        }
    
)
print(response)