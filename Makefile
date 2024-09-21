IMAGE_NAME=medal-bulk-downloader
build:
	docker build -t $(IMAGE_NAME) .
run:
	python src/main.py
run-docker:
	docker run -it --rm \
	-v $(PWD)/src/config.py:/app/config.py \
	-v $(PWD)/src/main.py:/app/main.py \
	-v $(PWD)/src/helpers.py:/app/helpers.py \
	-v $(PWD)/src/requestHelper.py:/app/requestHelper.py \
	-v $(PWD)/config.json:/app/config.json \
	-v $(PWD)/downloads:/downloads \
	$(IMAGE_NAME)