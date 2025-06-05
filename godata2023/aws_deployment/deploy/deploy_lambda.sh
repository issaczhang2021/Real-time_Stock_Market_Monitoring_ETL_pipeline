#!/bin/bash
set -e
DIR=$(dirname "$0")
FUNCTION_NAME=${FUNCTION_NAME:-StockDataFetcher}
ROLE_NAME=${ROLE_NAME:-stock-data-lambda-role}
ZIP_FILE="$DIR/../lambda_function.zip"
POLICY_FILE="$DIR/lambda_iam_policy.json"

aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"Service":"lambda.amazonaws.com"},"Action":"sts:AssumeRole"}]}' >/dev/null || true
aws iam put-role-policy --role-name $ROLE_NAME --policy-name lambda-policy --policy-document file://$POLICY_FILE >/dev/null
aws lambda create-function --function-name $FUNCTION_NAME \
  --runtime python3.9 --role $(aws iam get-role --role-name $ROLE_NAME --query 'Role.Arn' --output text) \
  --handler fetch_stock_data.lambda_handler --zip-file fileb://$ZIP_FILE >/dev/null || \
aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file fileb://$ZIP_FILE >/dev/null
