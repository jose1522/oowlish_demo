run: update-weights start-worker
update-weights:
	source scripts/downdload_model_weights.sh
start-worker:
	docker compose up -d --build summarizer-api
remove:
	docker compose rm --force -v
stop:
	docker compose stop
clean: stop remove