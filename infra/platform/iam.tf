locals {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "ecs-tasks.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

# ── Task execution role ───────────────────────────────────────────────────────
# Used by the ECS agent to pull the image from ECR and ship logs to CloudWatch.

resource "aws_iam_role" "execution" {
  name               = "${var.name}-execution-role"
  assume_role_policy = local.assume_role_policy

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "execution" {
  role       = aws_iam_role.execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

# ── Task role ─────────────────────────────────────────────────────────────────
# Used by the application process inside the container. Currently minimal;
# will be expanded when the Bedrock AgentCore integration is added.

resource "aws_iam_role" "task" {
  name               = "${var.name}-task-role"
  assume_role_policy = local.assume_role_policy

  tags = var.tags
}
