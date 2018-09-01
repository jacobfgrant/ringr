### Ringr Lambda Resources ###

# Lambda Function – Create Endpoint
resource "aws_lambda_function" "add_endpoint" {
  function_name = "RingrAddEndpoint"
  description   = "Add/update Ringr endpoints."
  filename      = "${var.add_function_zip_file_path}"
  role          = "${aws_iam_role.ringr_lambda_role.arn}"
  handler       = "add_endpoint.lambda_handler"
  runtime       = "python3.6"
  timeout       = 3

  environment {
    variables = {
      auth_key       = "${var.ringr_auth_key}",
      dynamodb_table = "${aws_dynamodb_table.ringr_dynamodb_table.id}",
      topic_arn      = "${aws_sns_topic.ringr_topic.arn}",
      ttl            = "${var.ringr_endpoint_ttl}",
    }
  }
}


# Lambda Function – Remove Endpoint
resource "aws_lambda_function" "remove_endpoint" {
  function_name = "RingrRemoveEndpoint"
  description   = "Remove Ringr endpoints."
  filename      = "${var.remove_function_zip_file_path}"
  role          = "${aws_iam_role.ringr_lambda_role.arn}"
  handler       = "remove_endpoint.lambda_handler"
  runtime       = "python3.6"
  timeout       = 3

  environment {
    variables = {
      auth_key       = "${var.ringr_auth_key}",
      dynamodb_table = "${aws_dynamodb_table.ringr_dynamodb_table.id}",
    }
  }
}


# Lambda Function – Manage Endpoints
resource "aws_lambda_function" "manage_endpoints" {
  function_name = "RingrManageEndpoints"
  description   = "Manage Ringr endpoints."
  filename      = "${var.manage_function_zip_file_path}"
  role          = "${aws_iam_role.ringr_lambda_role.arn}"
  handler       = "manage_endpoints.lambda_handler"
  runtime       = "python3.6"
  timeout       = 10

  environment {
    variables = {
      dynamodb_table = "${aws_dynamodb_table.ringr_dynamodb_table.id}",
    }
  }
}


# Lambda Function – Publish Notification
resource "aws_lambda_function" "publish_notification" {
  function_name = "RingrPublishNotification"
  description   = "Publish notification message to Ringr endpoints."
  filename      = "${var.publish_function_zip_file_path}"
  role          = "${aws_iam_role.ringr_lambda_role.arn}"
  handler       = "publish_notification.lambda_handler"
  runtime       = "python3.6"
  timeout       = 10

  environment {
    variables = {
      auth_key        = "${var.ringr_auth_key}",
      default_message =  "${var.default_message}",
      topic_arn       = "${aws_sns_topic.ringr_topic.arn}",
    }
  }
}
