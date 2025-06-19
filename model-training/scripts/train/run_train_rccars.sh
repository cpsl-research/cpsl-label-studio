#!/usr/bin/env bash

set -x


MMDET_DIR="../../third_party/avstack-core/third_party/mmdetection/"
cd $MMDET_DIR

MODEL=${1:?"missing arg 1 for MODEL"}


if [ $MODEL = "fasterrcnn" ]; then
    config="configs/rccars/faster_rcnn_r50_fpn_1x_rccars.py"
elif [ $MODEL = "rtmdet_m_oneclass" ]; then
    config="configs/rccars/rtmdet_m_8xb32-300e_rccars-oneclass.py"
elif [ $MODEL = "rtmdet_tiny_oneclass" ]; then
    config="configs/rccars/rtmdet_tiny_8xb32-300e_rccars-oneclass.py"
else
    echo "Incompatible model passed!" 1>&2
    exit 64
fi

CUDA_VISIBLE_DEVICES="0,1"
CONFIG="$config"
GPUS=2
NNODES=${NNODES:-1}
NODE_RANK=${NODE_RANK:-0}
PORT=${PORT:-29501}
MASTER_ADDR=${MASTER_ADDR:-"127.0.0.1"}

PYTHONPATH="$(dirname $0)/..":$PYTHONPATH \
python -m torch.distributed.launch \
    --nnodes=$NNODES \
    --node_rank=$NODE_RANK \
    --master_addr=$MASTER_ADDR \
    --nproc_per_node=$GPUS \
    --master_port=$PORT \
    $(dirname "$0")/tools/train.py \
    $CONFIG \
    --launcher pytorch ${@:3}
