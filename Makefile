run: start-worker
start-worker:
	docker compose up -d --build summarizer-api
remove:
	docker compose rm --force -v
stop:
	docker compose stop
clean: stop remove