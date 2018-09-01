### Ringr DynamoDB Resources ###

# DynamoDB Table
resource "aws_dynamodb_table" "ringr_dynamodb_table" {
  name             = "RingrEndpoints"
  read_capacity    = 5
  write_capacity   = 5
  hash_key         = "endpoint"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"

  attribute {
    name = "endpoint"
    type = "S"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

}


# DynamoDB Stream -> Lambda
resource "aws_lambda_event_source_mapping" "dynamodb_stream_mapping" {
  batch_size        = 100
  event_source_arn  = "${aws_dynamodb_table.ringr_dynamodb_table.stream_arn}"
  enabled           = true
  function_name     = "${aws_lambda_function.manage_endpoints.arn}"
  starting_position = "LATEST"
}
