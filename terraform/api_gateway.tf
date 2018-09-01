### Ringr API Gateway Resources ###

# API Gateway
resource "aws_api_gateway_rest_api" "ringr_api_gateway" {
  name        = "RingrAPI"
  description = "Ringr API Gateway for Lambda Functions"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}


# API Gateway Deployment
resource "aws_api_gateway_deployment" "prod_deployment" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  stage_name  = "prod"
  depends_on  = [
    "aws_api_gateway_integration.api_add_resource_lambda_integration",
    "aws_api_gateway_integration.api_remove_resource_lambda_integration",
    "aws_api_gateway_integration.api_publish_resource_lambda_integration",
  ]
}


## Add Endpoint ##

# API Gateway Resource – Add
resource "aws_api_gateway_resource" "api_add_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  parent_id   = "${aws_api_gateway_rest_api.ringr_api_gateway.root_resource_id}"
  path_part   = "add"
}


# API Gateway Method – Add
resource "aws_api_gateway_method" "api_add_method" {
  rest_api_id   = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id   = "${aws_api_gateway_resource.api_add_resource.id}"
  http_method   = "POST"
  authorization = "NONE"
}


# API Gateway Lambda Integration – Add
resource "aws_api_gateway_integration" "api_add_resource_lambda_integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id             = "${aws_api_gateway_resource.api_add_resource.id}"
  http_method             = "${aws_api_gateway_method.api_add_method.http_method}"
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.add_endpoint.arn}/invocations"
}


# API Gateway Method Response (200) – Add
resource "aws_api_gateway_method_response" "add_http_200" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id = "${aws_api_gateway_resource.api_add_resource.id}"
  http_method = "${aws_api_gateway_method.api_add_method.http_method}"
  status_code = "200"
}


# API Gateway Lambda Integration Response (200) – Add
resource "aws_api_gateway_integration_response" "add_http_200_lambda_response" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id = "${aws_api_gateway_resource.api_add_resource.id}"
  http_method = "${aws_api_gateway_method.api_add_method.http_method}"
  status_code = "${aws_api_gateway_method_response.add_http_200.status_code}"

  depends_on  = ["aws_api_gateway_integration.api_add_resource_lambda_integration"]
}


# API Gateway Lambda Permission – Add
resource "aws_lambda_permission" "add_api_lambda_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.add_endpoint.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ringr_api_gateway.execution_arn}/*/POST/add"
}


## Remove Endpoint ##

# API Gateway Resource – Remove
resource "aws_api_gateway_resource" "api_remove_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  parent_id   = "${aws_api_gateway_rest_api.ringr_api_gateway.root_resource_id}"
  path_part   = "remove"
}


# API Gateway Method – Remove
resource "aws_api_gateway_method" "api_remove_method" {
  rest_api_id   = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id   = "${aws_api_gateway_resource.api_remove_resource.id}"
  http_method   = "POST"
  authorization = "NONE"
}


# API Gateway Lambda Integration – Remove
resource "aws_api_gateway_integration" "api_remove_resource_lambda_integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id             = "${aws_api_gateway_resource.api_remove_resource.id}"
  http_method             = "${aws_api_gateway_method.api_remove_method.http_method}"
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.remove_endpoint.arn}/invocations"
}


# API Gateway Method Response (200) – Remove
resource "aws_api_gateway_method_response" "remove_http_200" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id = "${aws_api_gateway_resource.api_remove_resource.id}"
  http_method = "${aws_api_gateway_method.api_remove_method.http_method}"
  status_code = "200"
}


# API Gateway Lambda Integration Response (200) – Remove
resource "aws_api_gateway_integration_response" "remove_http_200_lambda_response" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id = "${aws_api_gateway_resource.api_remove_resource.id}"
  http_method = "${aws_api_gateway_method.api_remove_method.http_method}"
  status_code = "${aws_api_gateway_method_response.remove_http_200.status_code}"

  depends_on  = ["aws_api_gateway_integration.api_remove_resource_lambda_integration"]
}


# API Gateway Lambda Permission – Remove
resource "aws_lambda_permission" "remove_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.remove_endpoint.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ringr_api_gateway.execution_arn}/*/POST/remove"
}


## Publish Notification ##

# API Gateway Resource – Publish
resource "aws_api_gateway_resource" "api_publish_resource" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  parent_id   = "${aws_api_gateway_rest_api.ringr_api_gateway.root_resource_id}"
  path_part   = "publish"
}


# API Gateway Method – Publish
resource "aws_api_gateway_method" "api_publish_method" {
  rest_api_id   = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id   = "${aws_api_gateway_resource.api_publish_resource.id}"
  http_method   = "POST"
  authorization = "NONE"
}

# API Gateway Lambda Integration – Publish
resource "aws_api_gateway_integration" "api_publish_resource_lambda_integration" {
  rest_api_id             = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id             = "${aws_api_gateway_resource.api_publish_resource.id}"
  http_method             = "${aws_api_gateway_method.api_publish_method.http_method}"
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.publish_notification.arn}/invocations"
}


# API Gateway Method Response (200) – Publish
resource "aws_api_gateway_method_response" "publish_http_200" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id = "${aws_api_gateway_resource.api_publish_resource.id}"
  http_method = "${aws_api_gateway_method.api_publish_method.http_method}"
  status_code = "200"
}


# API Gateway Lambda Integration Response (200) – Publish
resource "aws_api_gateway_integration_response" "publish_http_200_lambda_response" {
  rest_api_id = "${aws_api_gateway_rest_api.ringr_api_gateway.id}"
  resource_id = "${aws_api_gateway_resource.api_publish_resource.id}"
  http_method = "${aws_api_gateway_method.api_publish_method.http_method}"
  status_code = "${aws_api_gateway_method_response.publish_http_200.status_code}"

  depends_on  = ["aws_api_gateway_integration.api_publish_resource_lambda_integration"]
}


# API Gateway Lambda Permission – Publish
resource "aws_lambda_permission" "publish_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.publish_notification.arn}"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.ringr_api_gateway.execution_arn}/*/POST/publish"
}
