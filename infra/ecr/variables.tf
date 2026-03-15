variable "region" {
  type        = string
  description = "AWS region"
  default     = "us-west-2"
}

variable "repository_name" {
  type        = string
  description = "Name of the ECR repository"
  default     = "cars-mcp-server"
}

variable "tags" {
  type        = map(string)
  description = "Tags applied to all resources"
  default     = {}
}
