!/bin/bash
set -e
DIR=$(dirname "$0")
FUNCTION_NAME=${FUNCTION_NAME:-StockDataFetcher}
RULE_NAME=${RULE_NAME:-stock-data-schedule}
# Schedule every 5 minutes by default
SCHEDULE_EXPRESSION=${SCHEDULE_EXPRESSION:-"rate(5 minutes)"}

aws events put-rule --name $RULE_NAME --schedule-expression "$SCHEDULE_EXPRESSION" >/dev/null
aws lambda add-permission --function-name $FUNCTION_NAME --statement-id ${RULE_NAME}-perm --action 'lambda:InvokeFunction' --principal events.amazonaws.com --source-arn $(aws events describe-rule --name $RULE_NAME --query 'Arn' --output text) >/dev/null || true
aws events put-targets --rule $RULE_NAME --targets "Id"="1","Arn"="$(aws lambda get-function --function-name $FUNCTION_NAME --query 'Configuration.FunctionArn' --output text)" >/dev/null
