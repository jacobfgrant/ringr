### Ringr SNS Resources ###

# SNS Topic
resource "aws_sns_topic" "ringr_topic" {
  provider = "aws.east"
  name     = "RingrSNSTopic"
}
