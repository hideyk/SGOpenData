#!/usr/bin/make -fg

init:
	@terraform -chdir=terraform init -backend-config="bucket=${BUCKET}"

plan: 
	@terraform -chdir=terraform plan -parallelism=50

apply: 
	@terraform -chdir=terraform apply -parallelism=50