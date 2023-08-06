#!/bin/bash

HOST=$1
PAYLOAD=$2
CONTENT_TYPE=${3:-text/csv}

curl -X POST -H 'Content-Type: text/csv' --data-binary @${PAYLOAD} -v ${HOST}/invocations
