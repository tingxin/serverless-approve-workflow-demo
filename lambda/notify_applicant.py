import boto3
import json
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid



recipient_email = ['friendship-119@163.com']
source_email = "tingxinxu@nwcdcloud.cn"
mail_template_name = 'approve_workflow_result'

class SesDestination:
    """Contains data about an email destination."""
    def __init__(self, tos, ccs=None, bccs=None):
        """
        :param tos: The list of recipients on the 'To:' line.
        :param ccs: The list of recipients on the 'CC:' line.
        :param bccs: The list of recipients on the 'BCC:' line.
        """
        self.tos = tos
        self.ccs = ccs
        self.bccs = bccs

    def to_service_format(self):
        """
        :return: The destination data in the format expected by Amazon SES.
        """
        svc_format = {'ToAddresses': self.tos}
        if self.ccs is not None:
            svc_format['CcAddresses'] = self.ccs
        if self.bccs is not None:
            svc_format['BccAddresses'] = self.bccs
        return svc_format

class SesMailSender:
    """Encapsulates functions to send emails with Amazon SES."""
    def __init__(self, ses_client):
        """
        :param ses_client: A Boto3 Amazon SES client.
        """
        self.ses_client = ses_client

    def send_templated_email(
            self, source, destination, template_name, template_data,
            reply_tos=None):
        """
        Sends an email based on a template. A template contains replaceable tags
        each enclosed in two curly braces, such as {{name}}. The template data passed
        in this function contains key-value pairs that define the values to insert
        in place of the template tags.

        Note: If your account is in the Amazon SES  sandbox, the source and
        destination email accounts must both be verified.

        :param source: The source email account.
        :param destination: The destination email account.
        :param template_name: The name of a previously created template.
        :param template_data: JSON-formatted key-value pairs of replacement values
                              that are inserted in the template before it is sent.
        :return: The ID of the message, assigned by Amazon SES.
        """
        send_args = {
            'Source': source,
            'Destination': destination.to_service_format(),
            'Template': template_name,
            'TemplateData': json.dumps(template_data)
        }
        if reply_tos is not None:
            send_args['ReplyToAddresses'] = reply_tos
        try:
            response = self.ses_client.send_templated_email(**send_args)
            message_id = response['MessageId']
            print(
                "Sent templated mail %s from %s to %s.", message_id, source,
                destination.tos)
        except ClientError:
            print(
                "Couldn't send templated mail from %s to %s.", source, destination.tos)
            raise
        else:
            return message_id

def lambda_handler(event, context):
    behaviour= event['behaviour']
    ses = boto3.client('ses')
    m = SesMailSender(ses)
    if behaviour:
        t_data ={
                'subject':'申请批复通知',
                'content':'您的申请已经被同意！'
            }
        
    else:
        t_data ={
                'subject':'申请批复通知',
                'content':'您的申请已经被拒绝！'
            }

    m.send_templated_email(source_email, 
            SesDestination(recipient_email),
            mail_template_name,
            t_data)

