#!/usr/bin/env bash

set -e

python split_train_val.py \
    --input /data/cpsl-interns/rccars-raw/result.json \
    --output /data/cpsl-interns/rccars-split \
    --val_ratio 0.2 \
    --see 42