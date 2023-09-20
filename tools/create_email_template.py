import boto3
import json
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


html_template1 = """
<html>
<head></head>
<body>
  <h3>{{content}}</h3>
  <p>点击这里 <a href="{{link1}}">批准申请</a>.</p>
  <p>点击这里 <a href="{{link2}}">拒绝申请</a>.</p>
</body>
</html>
"""

text_template1 = """
{{content}}\r\n
点击这里批准申请:\r\n
{{link1}}
点击这里拒绝申请:\r\n
{{link2}}
"""

html_template2 = """
<html>
<head></head>
<body>
  <h3>{{content}}</h3>
</body>
</html>
"""

text_template2 = """
{{content}}\r\n
"""

ses = boto3.client('ses')

response = ses.create_template(
    
        Template={
            "TemplateName": "approve_workflow_result",
            "SubjectPart": "{{subject}}!",
            "HtmlPart": html_template2,
            "TextPart": text_template2
        }
    
)
print(response)