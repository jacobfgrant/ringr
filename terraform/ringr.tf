##### Ringr Variables & Resources #####

### Configure Variables ###

variable "aws_access_key" {
  type        = "string"
  description = "AWS Access Key"
}

variable "aws_secret_key" {
  type        = "string"
  description = "AWS Secret Key"
}

variable "aws_region" {
  type        = "string"
  description = "AWS Region"
  default     = "us-east-1"
}

variable "ringr_auth_key" {
  type        = "string"
  description = "Ringr authorization key"
}

variable "ringr_endpoint_ttl" {
  type        = "string"
  description = "Ringr endpoint TTL"
  default     = 3600
}

variable "default_message" {
  type        = "string"
  description = "Default SNS message"
}

variable "add_function_zip_file_path" {
  type        = "string"
  description = "Path to .zip file"
}

variable "remove_function_zip_file_path" {
  type        = "string"
  description = "Path to .zip file"
}

variable "manage_function_zip_file_path" {
  type        = "string"
  description = "Path to .zip file"
}

variable "publish_function_zip_file_path" {
  type        = "string"
  description = "Path to .zip file"
}


### Configure Providers ###

# Configure default AWS Provider
provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region     = "${var.aws_region}"
}


# Configure AWS Provider (N. Virginia)
provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region     = "us-east-1"
  alias      = "east"
}
