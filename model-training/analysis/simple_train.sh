#!/usr/bin/env bash

set -x

MODEL=${1:?"missing arg 1 for MODEL"}

MMDET_DIR="../third_party/lib-avstack-core/third_party/mmdetection/"
cd $MMDET_DIR

if [ $MODEL = "fasterrcnn" ]; then
    config="configs/rccars/faster_rcnn_r50_fpn_1x_rccars.py"
elif [ $MODEL = "rtmdet-tiny" ]; then
    config="configs/rccars/rtmdet_tiny_8xb32-300e_rccars-oneclass.py"
elif [ $MODEL = "rtmdet-m" ]; then
    config="configs/rccars/rtmdet_m_8xb32-300e_rccars-oneclass.py"
elif [ $MODEL = "rtmdet-ins-tiny" ]; then
    config="configs/rccars/rtmdet-ins_tiny_8xb32-300e_rccars-oneclass.py"
elif [ $MODEL = "rtmdet-ins-m" ]; then
    config="configs/rccars/rtmdet-ins_m_8xb32-300e_rccars-oneclass.py"
else
    echo "Incompatible model passed!" 1>&2
    exit 64
fi

python tools/train.py $config