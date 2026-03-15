output "alb_dns_name" {
  description = "Internal DNS name of the ALB — use this as the MCP endpoint base URL"
  value       = aws_lb.this.dns_name
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.this.name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.this.name
}

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.this.id
}

output "private_subnet_ids" {
  description = "IDs of the three private subnets"
  value       = aws_subnet.private[*].id
}

output "agentcore_runtime_arn" {
  description = "ARN of the AgentCore Runtime — use this to invoke the MCP server via InvokeAgentRuntime"
  value       = aws_bedrockagentcore_agent_runtime.this.agent_runtime_arn
}
