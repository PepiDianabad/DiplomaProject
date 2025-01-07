# Create the SNS Topic
resource "aws_sns_topic" "prediction_alerts" {
  name = "prediction-alerts"
}

# Create an Email Subscription
resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.prediction_alerts.arn
  protocol  = "email"
  endpoint  = "pepipetrow2005@gmail.com" # Replace with your desired email
}

# Output the SNS Topic ARN
output "sns_topic_arn" {
  value = aws_sns_topic.prediction_alerts.arn
}
