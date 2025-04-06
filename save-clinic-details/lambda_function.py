import json
import uuid
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FormSubmissions')  # Replace with your table name

def lambda_handler(event, context):
    try:
        # Parse the JSON body
        body = json.loads(event['queryStringParameters'])

        print(body)

        # Generate unique ID
        submission_id = str(uuid.uuid4())

        # Compose the item to insert
        item = {
            'submission_id': submission_id,
            'timestamp': datetime.utcnow().isoformat()
        }

        # Add all form fields to the item
        for key, value in body.items():
            item[key] = value

        # Save to DynamoDB
        table.put_item(Item=item)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Submission saved!',
                'id': submission_id
            }),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }

    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Something went wrong'}),
            'headers': {
                'Access-Control-Allow-Origin': '*'
            }
        }
