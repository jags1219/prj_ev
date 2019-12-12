import boto3
import json
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    print(json_file_name)
    print(bucket)
    print(str(event))
    # TODO implement
    json_object = s3_client.get_object(Bucket=bucket,Key=json_file_name)
    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader)
    print(jsonDict)
    table = dynamodb.Table('ACCOUNTS')
    for x in jsonDict:
        table.put_item(Item=x)
    return 'Success'
