NAMESPACE=dev
ENV_FILE=.env
ENV_SECRET=app-env
PGBOUNCER_TPL_DIR=pgbouncer/tpl/
PGBOUNCER_DIR=pgbouncer/
DOCKERFILE=kubernetes/app/docker/Dockerfile
APP_IMAGE=todotoo-app
CONTEXT=.
LOCAL_DB_PORT=30201
LOCAL_PGBOUNCER_PORT=30202
LOCAL_REDIS_PORT=30203
REDIS_SERVICE=redis

.DEFAULT_GOAL := help

# Load env
ifneq (,$(wildcard $(ENV_FILE)))
include $(ENV_FILE)
export
endif

env: ## Load .env into Kubernetes Secret
	kubectl delete secret $(ENV_SECRET) -n $(NAMESPACE) --ignore-not-found
	kubectl create secret generic $(ENV_SECRET) --from-env-file=$(ENV_FILE) -n $(NAMESPACE)
	@echo ".env loaded into Kubernetes Secret: $(ENV_SECRET)"

build-app:
	cd .. && minikube image build -t todotoo-app:latest -f $(DOCKERFILE) $(CONTEXT)


push-app: ## Push image to Docker Hub or another registry
	docker tag $(APP_IMAGE):latest klishinoleg/$(APP_IMAGE):latest
	docker push klishinoleg/$(APP_IMAGE):latest
	@echo "Pushed app image: klishinoleg/$(APP_IMAGE):latest"

pgbhash: ## Generate md5 hash for user password
	$(eval DB_PGBOUNCER_HASH := md5$(shell echo -n "$(DB_PASSWORD)$(DB_USER)" | md5sum | awk '{print $$1}'))
	@echo "Generated PgBouncer hash: $(DB_PGBOUNCER_HASH)"

pgbconf: pgbhash ## generate config files for pg bouncer
	envsubst < $(PGBOUNCER_TPL_DIR)pgbouncer.ini > $(PGBOUNCER_DIR)pgbouncer.ini
	@DB_PGBOUNCER_HASH=$(DB_PGBOUNCER_HASH) envsubst < $(PGBOUNCER_TPL_DIR)users.txt > $(PGBOUNCER_DIR)users.txt

pgb-resources: pgbconf ## Create/Update PgBouncer config resources from generated files
	kubectl create configmap pgbouncer-config --from-file=pgbouncer.ini=$(PGBOUNCER_DIR)pgbouncer.ini --dry-run=client -o yaml | kubectl apply -n $(NAMESPACE) -f -
	kubectl create secret generic pgbouncer-users --from-file=users.txt=$(PGBOUNCER_DIR)users.txt --dry-run=client -o yaml | kubectl apply -n $(NAMESPACE) -f -

apply-prod: env pgb-resources ## Apply all resources (namespace + postgres + app) PROD
	kubectl apply -f namespace.yaml
	kubectl apply -n $(NAMESPACE) -f postgres/
	kubectl apply -n $(NAMESPACE) -f minis3/pvc.yaml
	kubectl apply -n $(NAMESPACE) -f minis3/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f minis3/service.yaml
	kubectl delete -n $(NAMESPACE) job minis3-init-bucket --ignore-not-found
	kubectl apply -n $(NAMESPACE) -f minis3/bucket-job.yaml
	kubectl apply -n $(NAMESPACE) -f pgbouncer/service.yaml
	kubectl apply -n $(NAMESPACE) -f pgbouncer/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f redis/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f redis/service.yaml
	kubectl apply -n $(NAMESPACE) -f app/

delete: ## Delete all resources including namespace
	kubectl delete -n $(NAMESPACE) -f app/
	kubectl delete -n $(NAMESPACE) -f redis/ --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f minis3/
	kubectl delete -n $(NAMESPACE) -f postgres/
	kubectl delete -f namespace.yaml

db: env ## Deploy only PostgreSQL (with PostGIS)
	kubectl apply -f namespace.yaml
	kubectl apply -n $(NAMESPACE) -f postgres/

pgbouncer: env pgb-resources ## Deploy PgBouncer
	kubectl apply -n $(NAMESPACE) -f pgbouncer/service.yaml
	kubectl apply -n $(NAMESPACE) -f pgbouncer/deployment.yaml

app: env ## Deploy only the application
	kubectl apply -n $(NAMESPACE) -f app/

infra-start: env pgb-resources ## Start infra stack (postgres + minis3 + pgbouncer + redis)
	kubectl apply -f namespace.yaml
	kubectl apply -n $(NAMESPACE) -f postgres/
	kubectl apply -n $(NAMESPACE) -f minis3/pvc.yaml
	kubectl apply -n $(NAMESPACE) -f minis3/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f minis3/service.yaml
	kubectl delete -n $(NAMESPACE) job minis3-init-bucket --ignore-not-found
	kubectl apply -n $(NAMESPACE) -f minis3/bucket-job.yaml
	kubectl apply -n $(NAMESPACE) -f pgbouncer/service.yaml
	kubectl apply -n $(NAMESPACE) -f pgbouncer/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f redis/deployment.yaml
	kubectl apply -n $(NAMESPACE) -f redis/service.yaml

infra-stop: ## Stop infra stack (postgres + minis3 + pgbouncer + redis)
	kubectl delete -n $(NAMESPACE) -f redis/ --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f pgbouncer/ --ignore-not-found
	kubectl delete -n $(NAMESPACE) job minis3-init-bucket --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f minis3/service.yaml --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f minis3/deployment.yaml --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f minis3/pvc.yaml --ignore-not-found
	kubectl delete -n $(NAMESPACE) -f postgres/ --ignore-not-found

infra-stot: infra-stop ## Alias for infra-stop

infra-reload: ## Reload infra stack (stop + start)
	$(MAKE) infra-stop
	$(MAKE) infra-start

status: ## Show pods and services status
	kubectl get pods -n $(NAMESPACE)
	kubectl get svc -n $(NAMESPACE)

logs-app: ## Show logs for app
	kubectl logs -n $(NAMESPACE) deployment/app

logs-db: ## Show logs for Postgres
	kubectl logs -n $(NAMESPACE) deployment/postgres

logs-dbb: ## Show logs for PG Bouncer
	kubectl logs -n $(NAMESPACE) deployment/pgbouncer

logs-minis3: ## Show logs for MiniS3
	kubectl logs -n $(NAMESPACE) deployment/minis3

connect-db: ## Port-forward Postgres to localhost:30201
	kubectl port-forward -n $(NAMESPACE) service/postgres $(LOCAL_DB_PORT):5432

connect-pgbouncer: ## Port-forward PgBouncer to localhost:30202
	kubectl port-forward -n $(NAMESPACE) service/pgbouncer $(LOCAL_PGBOUNCER_PORT):6432

connect-redis: ## Port-forward Redis to localhost:30203 (if service exists)
	@kubectl get svc $(REDIS_SERVICE) -n $(NAMESPACE) > /dev/null 2>&1 || (echo "Service '$(REDIS_SERVICE)' not found in namespace '$(NAMESPACE)'"; exit 1)
	kubectl port-forward -n $(NAMESPACE) service/$(REDIS_SERVICE) $(LOCAL_REDIS_PORT):6379

app-restart: ## Restart the app pod
	kubectl rollout restart deployment/app -n $(NAMESPACE)

app-shell: ## Open a shell inside the app container
	kubectl exec -n $(NAMESPACE) -it deployment/app -- bash

start:
	minikube start --driver=docker

create:
	minikube start --driver=docker
	kubectl create namespace dev

stop:
	minikube stop

show:
	kubectl get pods -n $(NAMESPACE)


help: ## Show this help message
	@echo ""
	@echo "Available commands:"
	@echo "  make apply         - Apply all resources (namespace + postgres + app)"
	@echo "  make delete        - Delete all resources including namespace"
	@echo "  make postgres      - Deploy only PostgreSQL with PostGIS"
	@echo "  make app           - Deploy only the application"
	@echo "  make infra-start   - Start infra stack (postgres + minis3 + pgbouncer + redis)"
	@echo "  make infra-stop    - Stop infra stack (postgres + minis3 + pgbouncer + redis)"
	@echo "  make infra-stot    - Alias for infra-stop"
	@echo "  make infra-reload  - Reload infra stack (stop + start)"
	@echo "  make status        - Show pods and services status"
	@echo "  make logs-app      - Show logs for the app"
	@echo "  make logs-db       - Show logs for Postgres"
	@echo "  make connect-db    - Port-forward Postgres to localhost:30201"
	@echo "  make connect-pgbouncer - Port-forward PgBouncer to localhost:30202"
	@echo "  make connect-redis - Port-forward Redis to localhost:30203"
	@echo "  make restart-app   - Restart the app deployment"
	@echo "  make app-shell     - Enter shell inside app container"
	@echo "  make app-shell     - Enter shell inside app container"
	@echo ""
	@echo "Usage:"
	@echo "  make <command>"
	@echo ""
