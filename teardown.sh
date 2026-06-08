#!bin/bash
# teardown.sh - delete the stack and associated resources
set -e
STACK_NAME="image-processor-dev"
REGION="eu-west-2"

echo "Deleting stack: $STACK_NAME"
aws cloudformation delete-stack --stack-name $STACK_NAME --region $REGION
echo "Waiting for stack to be deleted"
aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME --region $REGION
echo "Stack deleted"