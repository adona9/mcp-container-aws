# MCP server as a container in AWS

This is a demo repo to illustrate how to build an MCP server as a container and how to run it in AWS as a Fargate service.

## Repo Structure

* the "container" folder contains the Containerfile and the application code that implements the MCP capabilities
* the "infra" folder contains the Terraform configuration that deploys the ECS cluster, service, task configuration, and the Bedrock AgentCore resources that provides the MCP service middleware

## Prerequisites and Assumptions

### Knowledge
- Basic Python (reading and understanding a simple script)
- Familiarity with containers (building an image, running a container)
- For the AWS section: a working knowledge of AWS services (ECS, IAM, networking) and Terraform basics

### Tools
- Python 3.11+
- Podman
- `qemu-user-static` — required to build arm64 images on an x86_64 host (`sudo apt-get install qemu-user-static`)
- AWS CLI (for the AWS section)
- Terraform 1.5+ (for the AWS section)

### Accounts
- An AWS account with permissions to create ECS, ECR, IAM, and VPC resources (for the AWS section)
- Access to Amazon Bedrock AgentCore in your target region (for the AWS section)

---

## Container

The container-based application is a simple demo app that includes a small SQLite database with a handful of tables (car manufacturers, car models, car parts, etc). The app is a Python program that implements MCP using FastMCP and offers a set of read-only tools to query the data:

- `list_manufacturers` — list all car manufacturers
- `list_models` — list car models, with optional filtering by manufacturer
- `get_model` — get details about a specific car model
- `list_parts` — list parts, with optional filtering by model or category
- `search_parts` — search parts by keyword across name and description
- `get_part` — get details about a specific part

## Running locally

All container commands are driven by the `Makefile` in the repo root.

### Build

```bash
make build
```

This builds the image for the local machine's architecture (auto-detected). To target a specific architecture:

```bash
make build-amd64   # x86_64 — for local testing on Intel/AMD hardware
make build-arm64   # aarch64 — for AWS Graviton (used in the AWS section)
```

The image is tagged `cars-mcp-server:latest` by default. Override with `IMAGE` and `TAG`:

```bash
make build IMAGE=myrepo/cars-mcp-server TAG=v1.0
```

### Run

```bash
make run
```

This starts the container and maps port `8000` on the host to the MCP server inside the container. The server listens for MCP requests at `http://localhost:8000/mcp`.

Press `Ctrl+C` to stop it.

### Smoke test

With the container running in one terminal, open a second terminal and run:

```bash
make smoke-test
```

This sends a valid MCP `initialize` request to the server and prints the result. A passing run looks like:

```
>>> initialize
"result":{"protocolVersion":"2024-11-05","capabilities":{...}

>>> OK
```

If the server returns an error, or is unreachable, the target exits non-zero.

