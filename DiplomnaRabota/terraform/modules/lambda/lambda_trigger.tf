# EventBridge Rule for 5-Minute Trigger
resource "aws_cloudwatch_event_rule" "every_5_minutes" {
  name                = "Every5MinutesRule"
  schedule_expression = "rate(5 minutes)"
}

# EventBridge Rule Target (Lambda)
resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_5_minutes.name
  target_id = "my_lambda_target"
  arn       = aws_lambda_function.my_lambda.arn
}

# Permission for EventBridge to Invoke Lambda
resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowEventBridgeInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.my_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_5_minutes.arn
}
