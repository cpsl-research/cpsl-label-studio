#!/usr/bin/env bash

set -e

MMDET_BASE="../../third_party/avstack-core/third_party/mmdetection/"
CFG_FILE="$MMDET_BASE/configs/rccars/faster_rcnn_r50_fpn_1x_rccars.py"

python "$MMDET_BASE/tools/analysis_tools/browse_dataset.py" \
    $CFG_FILE \
    --show-interval 0.4