#!/usr/bin/env bash

set -e

python postprocess_tracking_labels.py \
    --root /data/shared/rccars \
    --input "raw-tracking-2025"