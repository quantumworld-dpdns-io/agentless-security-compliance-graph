terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
    kubernetes = { source = "hashicorp/kubernetes", version = "~> 2.0" }
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

provider "aws" {
  region = var.region
}

resource "aws_ecs_cluster" "compliance_graph" {
  name = "compliance-graph-${var.environment}"
}

resource "aws_ecs_service" "api" {
  name            = "compliance-graph-api-${var.environment}"
  cluster         = aws_ecs_cluster.compliance_graph.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 2
  launch_type     = "FARGATE"
}

resource "aws_ecs_task_definition" "api" {
  family                   = "compliance-graph-api-${var.environment}"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "1024"
  memory                   = "2048"
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  container_definitions = jsonencode([
    {
      name  = "api"
      image = "ghcr.io/quantumworld-dpdns-io/agentless-security-compliance-graph:latest"
      portMappings = [{ containerPort = 8000, protocol = "tcp" }]
      environment = [
        { name = "CG_ENVIRONMENT", value = var.environment },
        { name = "CG_DATABASE_URL", value = "duckdb:///data/compliance.db" }
      ]
    }
  ])
}

resource "aws_iam_role" "ecs_execution" {
  name = "compliance-graph-ecs-execution-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
    }]
  })
}

output "cluster_name" {
  value = aws_ecs_cluster.compliance_graph.name
}
