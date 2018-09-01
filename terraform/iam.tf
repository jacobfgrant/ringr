### Ringr IAM Resources ###

# IAM Role – Lambda
resource "aws_iam_role" "ringr_lambda_role" {
  name               = "ringr-lambda-role"
  description        = "Ringr Lambda IAM role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}


# DynamoDB Read/Write IAM Policy
resource "aws_iam_role_policy" "dynamodb_role_policy" {
  name   = "DynamoDBReadWritePolicy"
  role   = "${aws_iam_role.ringr_lambda_role.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:DeleteItem",
                "dynamodb:GetShardIterator",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem",
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords"
            ],
            "Resource": [
                "${aws_dynamodb_table.ringr_dynamodb_table.stream_arn}",
                "${aws_dynamodb_table.ringr_dynamodb_table.arn}",
                "${aws_dynamodb_table.ringr_dynamodb_table.arn}/index/*"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "dynamodb:ListStreams",
            "Resource": "*"
        }
    ]
}
EOF
}


# SNS Read/Write IAM Policy
resource "aws_iam_role_policy" "sns_subscription_role_policy" {
  name   = "SNSSubscriptionPolicy"
  role   = "${aws_iam_role.ringr_lambda_role.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "sns:Publish",
                "sns:Subscribe"
            ],
            "Resource": "${aws_sns_topic.ringr_topic.arn}"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "sns:Unsubscribe",
            "Resource": "*"
        }
    ]
}
EOF
}
