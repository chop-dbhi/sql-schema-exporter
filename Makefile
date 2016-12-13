IMAGE_NAME := dbhi/sql-schema-exporter

GIT_SHA := $(shell git log -1 --pretty=format:"%h" .)
GIT_TAG := $(shell git describe --tags --exact-match 2>/dev/null)
GIT_BRANCH := $(shell git symbolic-ref -q --short HEAD)

docker:
	docker build -t ${IMAGE_NAME}:${GIT_SHA} .
	docker tag ${IMAGE_NAME}:${GIT_SHA} ${IMAGE_NAME}:${GIT_BRANCH}
	if [ -n "${GIT_TAG}" ] ; then \
		docker tag ${IMAGE_NAME}:${GIT_SHA} ${IMAGE_NAME}:${GIT_TAG} ; \
  fi;

docker-push:
	docker push ${IMAGE_NAME}:${GIT_SHA}
	docker push ${IMAGE_NAME}:${GIT_BRANCH}
	if [ -n "${GIT_TAG}" ]; then \
		docker push ${IMAGE_NAME}:${GIT_TAG} ; \
  fi;

.PHONY: docker
