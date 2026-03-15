# container_image is referenced by both main.tf (task definition) and agentcore.tf
locals {
  container_image = "${data.terraform_remote_state.ecr.outputs.repository_url}:${var.image_tag}"
}
