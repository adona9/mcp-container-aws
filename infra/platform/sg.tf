# ── ALB ───────────────────────────────────────────────────────────────────────

resource "aws_security_group" "alb" {
  name        = "${var.name}-alb"
  description = "Internal ALB: accepts HTTP from the VPC, forwards to ECS on 8000"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "HTTP from within the VPC"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }

  egress {
    description = "To ECS tasks"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }

  tags = merge(var.tags, { Name = "${var.name}-alb-sg" })
}

# ── ECS tasks ─────────────────────────────────────────────────────────────────

resource "aws_security_group" "ecs" {
  name        = "${var.name}-ecs"
  description = "ECS tasks: accepts MCP traffic from ALB, reaches out to VPC endpoints"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "MCP server from ALB"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }

  egress {
    # All HTTPS egress stays within the VPC (no IGW/NAT, so nothing reaches the
    # internet); traffic is routed to interface endpoints and the S3 gateway endpoint.
    description = "HTTPS to VPC endpoints (ECR, CloudWatch Logs, S3)"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${var.name}-ecs-sg" })
}

# ── VPC interface endpoints ───────────────────────────────────────────────────

resource "aws_security_group" "vpc_endpoints" {
  name        = "${var.name}-vpc-endpoints"
  description = "VPC interface endpoints: accepts HTTPS from within the VPC"
  vpc_id      = aws_vpc.this.id

  ingress {
    description = "HTTPS from VPC"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [aws_vpc.this.cidr_block]
  }

  tags = merge(var.tags, { Name = "${var.name}-vpc-endpoints-sg" })
}
