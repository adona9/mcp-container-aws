terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  # Uncomment and configure to store state remotely (recommended for team use):
  # backend "s3" {
  #   bucket = "my-tf-state"
  #   key    = "mcp-container-aws/platform/terraform.tfstate"
  #   region = "us-west-2"
  # }
}
