import boto3
import requests
import json
from datetime import datetime

def get_secret(secret_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager')
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    return json.loads(get_secret_value_response['SecretString'])

def get_cost_data(start_date, end_date):
    cost_explorer = boto3.client('ce')
    return cost_explorer.get_cost_and_usage(
        TimePeriod={
            'Start': start_date,
            'End': end_date
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[
            {
                'Type': 'DIMENSION',
                'Key': 'SERVICE'
            }
        ]
    )

def lambda_handler(event, context):
    # Retrieve your stored secrets
    secrets = get_secret("PushoverCredentials")
    pushover_user_key = secrets['pushover_user_key']
    pushover_app_token = secrets['pushover_app_token']

    # Define the billing period
    today = datetime.now()
    start_of_month = datetime(today.year, today.month, 1).strftime('%Y-%m-%d')
    today_date = today.strftime('%Y-%m-%d')

    # Get cost data
    cost_data = get_cost_data(start_of_month, today_date)

    # Process and format the data
    total_cost = 0.0
    message = "AWS Cost for Current Billing Period:\n"
    for item in cost_data['ResultsByTime'][0]['Groups']:
        service_cost = float(item['Metrics']['UnblendedCost']['Amount'])
        total_cost += service_cost
        message += f"{item['Keys'][0]}: ${service_cost:.2f}\n"

    # Add total cost
    message += f"Total: ${total_cost:.2f}"

    # Send notification via Pushover
    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": pushover_app_token,
        "user": pushover_user_key,
        "message": message
    })

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }

