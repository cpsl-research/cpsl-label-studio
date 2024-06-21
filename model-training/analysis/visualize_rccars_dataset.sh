#!/usr/bin/env bash

# should run this in a python environment

set -e

python "../third_party/mmdetection/tools/analysis_tools/browse_dataset.py" \
    "../third_party/mmdetection/configs/_base_/datasets/rccars_detection.py" \
    --show-interval 1