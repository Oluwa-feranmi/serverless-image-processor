#!bin/bash
# deploy the Serverless Image Processor

set -e
STACK_NAME="image-processor-dev"
REGION="eu-west-2" #change this to your preferred region
NOTIFICATION_EMAIL="youremail@example.com" #change this to your email

echo "Deploying stack $STACK_NAME"
aws cloudformation deploy \
  --template-file cloudformation/template.yaml \
  --stack-name $STACK_NAME \
  --parameter-overrides EmailAddress=$NOTIFICATION_EMAIL \
  --capabilities CAPABILITY_IAM \
  --region $REGION

echo "stack deployment successful"

