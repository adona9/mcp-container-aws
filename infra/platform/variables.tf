variable "desired_count" {
  type        = number
  description = "Number of Fargate tasks to run"
  default     = 1
}

variable "image_tag" {
  type        = string
  description = "ECR image tag to deploy"
  default     = "latest"
}

variable "name" {
  type        = string
  description = "Name prefix applied to all resources"
  default     = "cars-mcp"
}

variable "region" {
  type        = string
  description = "AWS region"
  default     = "us-west-2"
}

variable "tags" {
  type        = map(string)
  description = "Tags applied to all resources"
  default     = {}
}

variable "task_cpu" {
  type        = number
  description = "Fargate task CPU units (256 = 0.25 vCPU)"
  default     = 256
}

variable "task_memory" {
  type        = number
  description = "Fargate task memory in MiB"
  default     = 512
}

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC (RFC 6598 carrier-grade NAT space)"
  default     = "100.64.0.0/16"
}
