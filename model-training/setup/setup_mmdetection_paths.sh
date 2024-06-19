#!/usr/bin/env bash

set -e

SAVEFOLDER=${1:-/data/$(whoami)/models}
SAVEFOLDER=${SAVEFOLDER%/}  # remove trailing slash
SAVEFOLDER="$SAVEFOLDER/mmdet"

THISDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

MMDET_CKPT="${SAVEFOLDER}/checkpoints"
MMDET_WKDIR="${SAVEFOLDER}/work_dirs"
mkdir -p "$MMDET_CKPT"
mkdir -p "$MMDET_WKDIR"

echo "Adding symbolic link to mmdet directory"
ln -sfnT $(realpath "$MMDET_CKPT") "$THISDIR/../third_party/mmdetection/checkpoints"
ln -sfnT $(realpath "$MMDET_WKDIR") "$THISDIR/../third_party/mmdetection/work_dirs"