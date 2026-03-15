# ── Bedrock AgentCore Runtime ─────────────────────────────────────────────────
# Deploys the same container image as the ECS service into the AgentCore
# managed hosting environment. AgentCore adds OAuth/SigV4 authentication,
# session isolation, and managed scaling on top of the same MCP contract.

resource "aws_bedrockagentcore_agent_runtime" "this" {
  agent_runtime_name = replace("${var.name}_runtime", "-", "_")
  role_arn           = aws_iam_role.agentcore.arn

  agent_runtime_artifact {
    container_configuration {
      container_uri = local.container_image
    }
  }

  network_configuration {
    network_mode = "VPC"
    network_mode_config {
      subnets         = toset(aws_subnet.private[*].id)
      security_groups = toset([aws_security_group.agentcore.id])
    }
  }

  protocol_configuration {
    server_protocol = "MCP"
  }

  tags = var.tags
}
