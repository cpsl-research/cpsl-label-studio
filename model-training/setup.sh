#!/usr/bin/env bash

set -x

cd third_party/avstack-core/models
"./download_mmdet_models.sh"
"./download_mmseg_models.sh"