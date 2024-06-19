#!/usr/bin/env bash

set -e

SAVEFOLDER=${1:-/data/$(whoami)/models}
SAVEFOLDER=${SAVEFOLDER%/}  # remove trailing slash
SAVEFOLDER="$SAVEFOLDER/mmseg"

THISDIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

MMSEG_CKPT="${SAVEFOLDER}/checkpoints"
MMSEG_WKDIR="${SAVEFOLDER}/work_dirs"
mkdir -p "$MMSEG_CKPT"
mkdir -p "$MMSEG_WKDIR"

echo "Adding symbolic link to mmseg directory"
ln -sfnT $(realpath "$MMSEG_CKPT") "$THISDIR/../third_party/mmsegmentation/checkpoints"
ln -sfnT $(realpath "$MMSEG_WKDIR") "$THISDIR/../third_party/mmsegmentation/work_dirs"