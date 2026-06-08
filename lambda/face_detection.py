import json
import boto3
import os
from urllib.parse import unquote_plus

rekognition = boto3.client('rekognition')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = os.environ['DYNAMODB_TABLE']
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # Get image details from Step Functions input
    bucket = event['bucket']
    key = event['key']
    
    try:
        # Call Rekognition
        response = rekognition.detect_faces(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            Attributes=['ALL']
        )
        
        faces = response.get('FaceDetails', [])
        face_detected = len(faces) > 0
        
        # Prepare metadata
        item = {
            'id': key,  # Fixed: Use actual string value instead of str type
            'image_id': key,
            'bucket': bucket,
            'upload_time': context.get_remaining_time_in_millis(),
            'face_detected': face_detected,
            'face_count': len(faces),
            'rekognition_details': json.dumps(faces[:2]) if faces else None
        }
        
        # Store in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item=item)
        
        # Send SNS notification
        message = f"Image processed: {key}\nFace detected: {face_detected}\nFaces found: {len(faces)}"
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Image Processing Result",
            Message=message
        )
        
        return {
            'status': 'success',
            'face_detected': face_detected,
            'face_count': len(faces),
            'image_key': key
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
