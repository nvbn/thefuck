#!/usr/bin/env sh

set -e

BUILD_DIR="$(git rev-parse --show-toplevel)/build"

mkdir -p "$BUILD_DIR"
docker build .. -f ./thefuck-appimage.Dockerfile -t tmp/thefuck-appimage --no-cache --force-rm
docker run --rm -v "$BUILD_DIR":/result tmp/thefuck-appimage
echo "Done. Appimage saved in $BUILD_DIR directory: $(ls -sh1 "$BUILD_DIR")"

