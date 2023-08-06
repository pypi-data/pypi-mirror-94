#!/usr/bin/env bash

if [ $1 = "train" ]; then
    python ./src/container/training/train
else
    python ./src/container/prediction/serve
fi
