#!/bin/bash

set -e

JOB_TOKEN=$1
USER=$2
SECRET=$3
REGISTRY=$4
REGISTRY_IMAGE=$5

IMAGE_TAG="trunk"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

${SCRIPT_DIR}/add-pypi-indices.sh $JOB_TOKEN

pushd "${SCRIPT_DIR}/.." || exit

docker login -u $USER -p $SECRET $REGISTRY
docker build --secret id=pypi,src=$HOME/.config/uv/uv.toml --secret id=netrc,src=$HOME/.netrc -t $REGISTRY_IMAGE:$IMAGE_TAG -f docker/trunk.Dockerfile .
docker push $REGISTRY_IMAGE:$IMAGE_TAG

popd || exit