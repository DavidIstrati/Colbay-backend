import boto3
import json

client = boto3.client('ses', region_name="us-east-1")

def sendVerificationEmail(code, recipientEmail, recipientName):

    templateData = {
        "name": recipientName,
        "code": code,
    }

    response = client.send_templated_email(
        Source='david@colbay.shop',
        Destination={
            'ToAddresses': [
                recipientEmail,
            ],
        },
        Template='EmailVerification',
        TemplateData=json.dumps(templateData)
    )
    return response