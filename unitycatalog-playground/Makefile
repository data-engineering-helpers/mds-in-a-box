#
# File: https://github.com/data-engineering-helpers/mds-in-a-box/tree/main/unitycatalog-playground/Makefile
#

MODE_FILE := .cli-use-docker.var
MODE_FILE_SAMPLE := .cli-use-docker.var.sample

# Persisted local mode state. If the file is missing, Docker is the default.
USE_DOCKER ?= 1
-include $(MODE_FILE)

## Environment
AWS_REGION := us-east-1
AWS_ACCESS_KEY_ID := 1234567890DEMO0KEY00
AWS_SECRET_ACCESS_KEY := RediDemoKey0011223344556677ToBeReplaced0
S3_ENDPOINT := http://localhost:8333
AWS_ENDPOINT_URL := $(S3_ENDPOINT)

export AWS_REGION
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_ENDPOINT_URL

## UC source selection
# UC_SOURCE values: docker|brew|local
UC_SOURCE ?= $(if $(filter 1,$(USE_DOCKER)),docker,brew)
EFFECTIVE_UC_SOURCE := $(if $(filter 1,$(USE_DOCKER)),docker,$(UC_SOURCE))

## Unity Catalog (UC) CLI
# host.docker.internal is used (not localhost) because the UC and SeaweedFS
# containers run in separate Docker Compose networks; this matches aws.endpoint
# in etc/conf/server.properties.
UC_CONTAINER_S3_ENDPOINT := http://host.docker.internal:8333
UC_DOCKER := docker exec -e AWS_ENDPOINT_URL=$(UC_CONTAINER_S3_ENDPOINT) unity-catalog ./bin/uc
UC_BREW := uc
UC_LOCAL := $(UC_LOCAL_ROOT)/bin/uc
UC := $(if $(filter docker,$(EFFECTIVE_UC_SOURCE)),$(UC_DOCKER),$(if $(filter local,$(EFFECTIVE_UC_SOURCE)),$(UC_LOCAL),$(UC_BREW)))

AWS_S3 := aws --endpoint-url $(AWS_ENDPOINT_URL) s3

.PHONY: init-mode-file reset-mode-file use-docker use-local show-mode \
	container-start-seaweedfs container-start-uc container-start-all \
	container-stop-seaweedfs container-stop-uc container-stop-all \
	service-start-seaweedfs service-stop-seaweedfs service-start-uc service-stop-uc \
	service-start-all service-stop-all ensure-uc-brew-stopped validate-uc-source \
	validate-uc-local-root validate-uc-cli install-local-deps setup-seaweedfs-config \
	capture-ai-json-report \
	init-s3 init-uc-creds open-s3-browser browse-s3 init-uc-cat-sch-xt clean-uc-table-xt \
	init-uc-table-xt init-uc-cat-sch clean-uc-table init-uc-table list-tables list-tables-xt \
	get-table-marksheet get-table-dim_customer read-table-dim_customer


## Mode toggle and status
init-mode-file: ## Create .cli-use-docker.var from sample if missing
	@if [ -f "$(MODE_FILE)" ]; then \
		echo "$(MODE_FILE) already exists; keeping current file"; \
	else \
		cp "$(MODE_FILE_SAMPLE)" "$(MODE_FILE)"; \
		echo "Created $(MODE_FILE) from $(MODE_FILE_SAMPLE)"; \
	fi

reset-mode-file: ## Reset .cli-use-docker.var from sample (overwrite)
	@cp -f "$(MODE_FILE_SAMPLE)" "$(MODE_FILE)"
	@echo "Reset $(MODE_FILE) from $(MODE_FILE_SAMPLE)"

use-docker: ## Persist Docker mode (USE_DOCKER=1)
	@if [ ! -f "$(MODE_FILE)" ]; then \
		cp "$(MODE_FILE_SAMPLE)" "$(MODE_FILE)"; \
	fi
	@if grep -q '^USE_DOCKER=' "$(MODE_FILE)"; then \
		sed -i.bak 's/^USE_DOCKER=.*/USE_DOCKER=1/' "$(MODE_FILE)" && rm -f "$(MODE_FILE).bak"; \
	else \
		echo "USE_DOCKER=1" >> "$(MODE_FILE)"; \
	fi
	@echo "Saved USE_DOCKER=1 in $(MODE_FILE)"

use-local: ## Persist local mode (USE_DOCKER=0)
	@if [ ! -f "$(MODE_FILE)" ]; then \
		cp "$(MODE_FILE_SAMPLE)" "$(MODE_FILE)"; \
	fi
	@if grep -q '^USE_DOCKER=' "$(MODE_FILE)"; then \
		sed -i.bak 's/^USE_DOCKER=.*/USE_DOCKER=0/' "$(MODE_FILE)" && rm -f "$(MODE_FILE).bak"; \
	else \
		echo "USE_DOCKER=0" >> "$(MODE_FILE)"; \
	fi
	@echo "Saved USE_DOCKER=0 in $(MODE_FILE)"

show-mode: ## Show effective infra mode and UC source
	@echo "USE_DOCKER=$(USE_DOCKER)"
	@if [ "$(USE_DOCKER)" = "1" ]; then \
		echo "UC_SOURCE=docker (forced by USE_DOCKER=1)"; \
	else \
		echo "UC_SOURCE=$(EFFECTIVE_UC_SOURCE)"; \
	fi
	@if [ -f "$(MODE_FILE)" ]; then \
		echo "mode_source=$(MODE_FILE)"; \
	else \
		echo "mode_source=default"; \
	fi


## Validation and setup helpers
validate-uc-source:
	@case "$(EFFECTIVE_UC_SOURCE)" in \
		docker|brew|local) ;; \
		*) echo "Invalid UC_SOURCE=$(EFFECTIVE_UC_SOURCE). Allowed values: docker, brew, local"; exit 1 ;; \
	esac

ensure-uc-brew-stopped:
	@if command -v brew >/dev/null 2>&1; then \
		brew services stop unitycatalog >/dev/null 2>&1 || true; \
	fi

validate-uc-local-root: validate-uc-source
	@if [ "$(EFFECTIVE_UC_SOURCE)" = "local" ]; then \
		if [ -z "$(UC_LOCAL_ROOT)" ]; then \
			echo "UC_SOURCE=local requires UC_LOCAL_ROOT to be provided"; \
			echo "Example: make $@ UC_SOURCE=local UC_LOCAL_ROOT=~/dev/infra/unitycatalog"; \
			exit 1; \
		fi; \
		if [ ! -x "$(UC_LOCAL_ROOT)/bin/uc" ]; then \
			echo "Cannot execute $(UC_LOCAL_ROOT)/bin/uc"; \
			echo "Check UC_LOCAL_ROOT points to a valid unitycatalog checkout/build"; \
			exit 1; \
		fi; \
	fi

validate-uc-cli: validate-uc-source validate-uc-local-root
	@if [ "$(EFFECTIVE_UC_SOURCE)" = "brew" ]; then \
		if ! command -v uc >/dev/null 2>&1; then \
			echo "uc is not available in PATH"; \
			echo "Install with: brew install unitycatalog"; \
			echo "Then ensure uc is available in PATH"; \
			exit 1; \
		fi; \
	fi
	@if [ "$(EFFECTIVE_UC_SOURCE)" = "local" ]; then \
		$(MAKE) ensure-uc-brew-stopped; \
	fi

install-local-deps: ## Install local dependencies (SeaweedFS, AWS CLI, optional UC)
	@if ! command -v seaweedfs >/dev/null 2>&1; then brew install seaweedfs; fi
	@if ! command -v aws >/dev/null 2>&1; then brew install awscli; fi
	@if [ "$(EFFECTIVE_UC_SOURCE)" = "brew" ] && ! command -v uc >/dev/null 2>&1; then brew install unitycatalog; fi

setup-seaweedfs-config: ## Copy SeaweedFS S3 config to /etc/seaweedfs (requires sudo)
	@echo "Preparing /etc/seaweedfs/s3.json"
	@sudo mkdir -p /etc/seaweedfs
	@sudo cp etc/conf/s3.json /etc/seaweedfs/s3.json

capture-ai-json-report: ## Capture JSON diagnostics report in tests/mds-test-<timestamp>.json
	@mkdir -p tests
	@USE_DOCKER="$(USE_DOCKER)" \
	EFFECTIVE_UC_SOURCE="$(EFFECTIVE_UC_SOURCE)" \
	UC_LOCAL_ROOT="$(UC_LOCAL_ROOT)" \
	AWS_ENDPOINT_URL="$(AWS_ENDPOINT_URL)" \
	UC_CMD='$(UC)' \
	bash tests/capture_ai_json_report.sh


## Local service start/stop (Homebrew)
service-start-seaweedfs: ## Start SeaweedFS local service
	@brew services start seaweedfs

service-stop-seaweedfs: ## Stop SeaweedFS local service
	@brew services stop seaweedfs

service-start-uc: validate-uc-source validate-uc-local-root ## Start UC local service when UC_SOURCE=brew
	@if [ "$(EFFECTIVE_UC_SOURCE)" = "brew" ]; then \
		brew services start unitycatalog; \
	elif [ "$(EFFECTIVE_UC_SOURCE)" = "local" ]; then \
		echo "UC_SOURCE=local; not starting Homebrew unitycatalog service"; \
		$(MAKE) ensure-uc-brew-stopped; \
	else \
		echo "UC_SOURCE=docker; UC service is managed by Docker"; \
	fi

service-stop-uc: validate-uc-source ## Stop UC local service when UC_SOURCE=brew
	@if [ "$(EFFECTIVE_UC_SOURCE)" = "brew" ]; then \
		brew services stop unitycatalog; \
	elif [ "$(EFFECTIVE_UC_SOURCE)" = "local" ]; then \
		$(MAKE) ensure-uc-brew-stopped; \
	fi

service-start-all: validate-uc-source validate-uc-local-root ## Start all local services
	@$(MAKE) service-start-seaweedfs
	@$(MAKE) service-start-uc

service-stop-all: validate-uc-source ## Stop all local services
	@$(MAKE) service-stop-uc
	@$(MAKE) service-stop-seaweedfs


## Container start/stop
container-start-seaweedfs: ## Start SeaweedFS Docker containers
	@docker compose -f docker-compose-seaweedfs.yaml up --remove-orphans -d

container-start-uc: ## Start Unity Catalog (UC) Docker containers
	@docker compose -f docker-compose.yaml up --remove-orphans -d

container-start-all: ## Start all services (Docker or local)
	@if [ "$(USE_DOCKER)" = "1" ]; then \
		$(MAKE) container-start-seaweedfs; \
		$(MAKE) container-start-uc; \
	else \
		$(MAKE) service-start-all; \
	fi

container-stop-seaweedfs: ## Stop SeaweedFS Docker containers
	@docker compose -f docker-compose-seaweedfs.yaml down

container-stop-uc: ## Stop Unity Catalog (UC) Docker containers
	@docker compose -f docker-compose.yaml down

container-stop-all: ## Stop all services (Docker or local)
	@if [ "$(USE_DOCKER)" = "1" ]; then \
		$(MAKE) container-stop-seaweedfs; \
		$(MAKE) container-stop-uc; \
	else \
		$(MAKE) service-stop-all; \
	fi


## Init
init-s3: ## Create the lakehouse bucket on S3
	@$(AWS_S3) mb s3://lakehouse
	@$(AWS_S3) cp README.md s3://lakehouse/
	@$(AWS_S3) ls --human --summarize --recursive s3://lakehouse/

init-uc-creds: validate-uc-cli ## Initialize the UC credentials
	@$(UC) credential create --name lh_aws_cred \
		--aws_iam_role_arn arn:aws:iam::987654321:role/UCDbRole-EXAMPLE
	@$(UC) external_location create --name lh_ext_loc \
		--url s3://lakehouse/unitycatalog/storage \
		--credential_name lh_aws_cred


## S3
open-s3-browser: ## Browse the SeaweedFS S3-compatible file-system
	@open http://localhost:8888/

browse-s3: ## Browse the SeaweedFS S3-compatible file-system
	@$(AWS_S3) ls --human --summarize --recursive s3://lakehouse/


## UC
init-uc-cat-sch-xt: ## Create catalog and schema with local filesystem storage
	@uc catalog create --name unitysw \
		--storage_root /home/unitycatalog/warehouse --comment "Extended catalog"
	@uc schema create --catalog unitysw --name bronze \
		--storage_root /home/unitycatalog/warehouse --comment "Bronze schema"

clean-uc-table-xt: ## Clean the table in Unity Catalog (UC)
	@$(eval TBL_NAME=$(shell uc table list --catalog unityxt --schema bronze --output json | jq -r '.[]|select(.name|contains("dim_customer"))|.name'))
	@if [ "$(TBL_NAME)" = "dim_customer" ]; then \
		uc table delete --full_name unityxt.bronze.dim_customer ; \
	else \
		echo "Table dim_customer has not been created on UC in unityxt.bronze yet"; \
		echo "No need to delete it" ; \
	fi

init-uc-table-xt: ## Initialize the dim_customer table in Unity Catalog (UC)
	@uc table create \
		--full_name unityxt.bronze.dim_customer \
		--columns "uuid string, address string, birthdate date, blood_group string, \
		company string, job string, mail string, name string, residence string, \
		sex string, ssn string, username string, website string, \
		current_location_lat double, current_location_lon double, \
		extraction_date date, start_date date, end_date date, is_current boolean" \
		--table_type MANAGED --format DELTA \
		--properties '{"key1": "value1", "key2": "value2"}'

init-uc-cat-sch: validate-uc-cli ## Create catalog and schema with SeaweedFS S3 storage
	@$(UC) catalog create --name unitysw \
		--storage_root s3://lakehouse/warehouse --comment "Extended catalog"
	@$(UC) schema create --catalog unitysw --name bronze \
		--storage_root s3://lakehouse/warehouse --comment "Bronze schema"

clean-uc-table: validate-uc-cli ## Clean the table in Unity Catalog (UC)
	@$(eval TBL_NAME=$(shell $(UC) table list --catalog unitysw --schema bronze --output json | jq -r '.[]|select(.name|contains("dim_customer"))|.name'))
	@if [ "$(TBL_NAME)" = "dim_customer" ]; then \
		$(UC) table delete --full_name unitysw.bronze.dim_customer ; \
	else \
		echo "Table dim_customer has not been created on UC in unitysw.bronze yet"; \
		echo "No need to delete it" ; \
	fi

init-uc-table: validate-uc-cli ## Initialize the dim_customer table in Unity Catalog (UC)
	@$(UC) table create \
		--full_name unitysw.bronze.dim_customer \
		--columns "uuid string, address string, birthdate date, blood_group string, \
		company string, job string, mail string, name string, residence string, \
		sex string, ssn string, username string, website string, \
		current_location_lat double, current_location_lon double, \
		extraction_date date, start_date date, end_date date, is_current boolean" \
		--table_type MANAGED --format DELTA \
		--properties '{"key1": "value1", "key2": "value2"}'

list-tables: validate-uc-cli ## List tables in UC with SeaweedFS storage
	@$(UC) table list --catalog unitysw --schema bronze

list-tables-xt: ## List tables in UC extended (xt)
	@uc table list --catalog unityxt --schema bronze

get-table-marksheet: ## Get the details of the marksheet table
	@uc table get --full_name unity.default.marksheet

get-table-dim_customer: validate-uc-cli ## Get details of the dim_customer table
	@$(UC) table get --full_name unitysw.bronze.dim_customer

read-table-dim_customer: validate-uc-cli ## Browse the dim_customer table
	@$(UC) table read --full_name unitysw.bronze.dim_customer --max_results 3
