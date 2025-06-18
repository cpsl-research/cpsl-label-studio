#!/usr/bin/env bash

# should run this in a python environment

set -e

python "../third_party/avstack-core/third_party/mmdetection/tools/analysis_tools/browse_dataset.py" \
    "../third_party/avstack-core/third_party/mmdetection/configs/rccars/faster_rcnn_r50_fpn_1x_rccars.py" \
    --show-interval 0.4