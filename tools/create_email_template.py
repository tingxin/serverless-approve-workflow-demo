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
  <p>点击这里 <a href="{{link}}">批准申请</a>.</p>
</body>
</html>
"""

text_template = """
{{content}}\r\n
点击这里批准申请:\r\n
{{link}}
"""

ses = boto3.client('ses')

response = ses.create_template(
    
        Template={
            "TemplateName": "approve_template",
            "SubjectPart": "{{subject}}!",
            "HtmlPart": html_template,
            "TextPart": text_template
        }
    
)
print(response)