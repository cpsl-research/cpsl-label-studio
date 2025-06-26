#!/usr/bin/env bash

set -e

python convert_coco_to_oneclass.py \
    --seed 0 \
    --root /data/shared/rccars \
    --input "raw-detection-2025" \
    --output "oneclass-detection-2025" \
    --pct_train 0.70