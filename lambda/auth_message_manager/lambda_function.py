import os, logging, boto3, json, botocore.exceptions

if __name__ != "__main__":
    from aws_xray_sdk.core import xray_recorder
    from aws_xray_sdk.core import patch_all
    patch_all()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    if event["triggerSource"] == "CustomMessage_ForgotPassword":
        reset_link = f"https://tetraforce.io/reset_password?reset_code={event['request']['codeParameter']}"
        event["response"] = {
                "smsMessage" : f"Hi there!\nIt's the TetraForce team.\n\nClick here to reset your password: {reset_link}",
                "emailSubject" : "Forgot your password? | TetraForce",
                "emailMessage" : f"<a href=\"{reset_link}\">Click here to reset your password</a>"
            }
    elif event["triggerSource"] == "CustomMessage_SignUp":
        confirm_link = event["request"]["linkParameter"]
        event["response"] = {
            "smsMessage" : f"Hi there!\nWelcome to TetraForce!\n\nClick here to confirm your device: {confirm_link}",
            "emailSubject" : "Confirm Email | TetraForce",
            "emailMessage" : load_email_template("verify_email.html", confirm_link)
        }
    
    return event

def load_email_template(template_name, link):
    
    email_body = ""
    
    with open(f"email_templates/{template_name}", "r") as template:
        email_body=template.read()
    
    email_body.replace("##", link)

    return email_body