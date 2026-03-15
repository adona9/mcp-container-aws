IMAGE    ?= cars-mcp-server
TAG      ?= latest
RUNTIME  ?= podman
# Auto-detect the local platform; override with PLATFORM=linux/arm64 etc.
PLATFORM ?= linux/$(shell uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
HOST     ?= localhost
PORT     ?= 8000

.PHONY: build build-amd64 build-arm64 run smoke-test

build:
	$(RUNTIME) build \
		--platform $(PLATFORM) \
		-f container/Containerfile \
		-t $(IMAGE):$(TAG) \
		container/

build-amd64:
	$(MAKE) build PLATFORM=linux/amd64

build-arm64:
	$(MAKE) build PLATFORM=linux/arm64

run:
	$(RUNTIME) run --rm \
		-p $(PORT):8000 \
		$(IMAGE):$(TAG)

smoke-test:
	@echo ">>> initialize"
	@response=$$(curl -sf -X POST http://$(HOST):$(PORT)/mcp \
		-H "Content-Type: application/json" \
		-H "Accept: application/json, text/event-stream" \
		-d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"smoke-test","version":"0.0.1"}}}'); \
	echo "$$response"; \
	echo "$$response" | grep -q '"result"' && echo "\n>>> OK"
