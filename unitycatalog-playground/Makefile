#
# File: https://github.com/data-engineering-helpers/mds-in-a-box/tree/main/unitycatalog-playground/Makefile
#

## Environment
AWS_ACCESS_KEY_ID := 1234567890DEMO0KEY00
AWS_SECRET_ACCESS_KEY := RediDemoKey0011223344556677ToBeReplaced0
S3_ENDPOINT := http://localhost:8333
AWS_REGION := us-east-1


## Container start/stop
container-start: ## Start Docker containers
	@docker compose up --remove-orphans -d

container-stop: ## Stop Docker containers
	@docker compose down

## Init

init-s3: ## Create the lakehouse bucket on S3
	@aws s3 mb s3://lakehouse
	@aws s3 cp README.md s3://lakehouse/
	aws s3 ls --human --summarize --recursive s3://lakehouse/

init-uc-creds: ## Initialize the UC credentials
	@uc credential create --name lh_aws_cred \
		--aws_iam_role_arn arn:aws:iam::987654321:role/UCDbRole-EXAMPLE
	@uc external_location create --name lh_ext_loc \
		--url s3://lakehouse/unitycatalog/storage \
		--credential_name lh_aws_cred

## S3

open-s3-browser: ## Browse the SeadweedFS S3-compatible file-system
	@open http://localhost:8888/

browse-s3: ## Browse the SeadweedFS S3-compatible file-system
	@aws s3 ls --human --summarize --recursive s3://lakehouse/

## UC

init-uc-cat-sch: ## Create catalog and schema with S3 location
	@uc catalog create --name unityxt \
		--storage_root s3://lakehouse/warehouse --comment "Extended catalog"
	@uc schema create --catalog unityxt --name bronze \
		--storage_root s3://lakehouse/warehouse --comment "Bronze schema"

init-uc-table: ## Create table on UC
	@uc table create \
		--full_name unityxt.bronze.dim_customer \
		--columns "address string, birthdate date, blood_group string, \
              company string, job string, mail string, name string, residence string, \
              sex string, ssn string, username string, website string, \
              current_location_lat double, current_location_lon double, \
              start_date date, end_date date, is_current boolean" \
		--table_type MANAGED --format DELTA \
		--properties '{"key1": "value1", "key2": "value2"}'

list-tables: ## List tables in UC
	@uc table list --catalog unity --schema default

get-table-marksheet: ## Get the details of the marksheet table
	@uc table get --full_name unity.default.marksheet
