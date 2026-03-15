output "registry_id" {
  description = "AWS account ID that owns the registry"
  value       = aws_ecr_repository.this.registry_id
}

output "repository_arn" {
  description = "ARN of the ECR repository"
  value       = aws_ecr_repository.this.arn
}

output "repository_url" {
  description = "Full ECR repository URL (used to tag and push images)"
  value       = aws_ecr_repository.this.repository_url
}
