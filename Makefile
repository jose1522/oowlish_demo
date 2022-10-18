run: update-weights start-worker start-ui
update-weights:
	/bin/bash scripts/download_model_weights.sh
start-worker:
	docker-compose up -d --build summarizer-api
start-ui:
	docker-compose up -d --build summarizer-ui
remove:
	docker-compose rm --force -v
stop:
	docker-compose stop
clean: stop remove