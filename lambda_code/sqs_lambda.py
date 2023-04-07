import json
import boto3


def lambda_handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    dynamodb = boto3.client('dynamodb')
    for record in event['Records']:
        print(record['body'])
        payload = record['body']
        dynamodb.put_item(
            TableName='idTable',
            Item={
                'id':
                    {'S': payload}
            }
        )
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': "Hello from cdk project"
    }
