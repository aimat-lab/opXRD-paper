#!/bin/bash

# Define the root directory where the script and build should be located
ROOT_DIR="$HOME/xrd_data_collect"

if [ ! -d "$ROOT_DIR" ]; then
    mkdir -p "$ROOT_DIR"
fi


DIST_DIR="$ROOT_DIR/dist"
BUILD_DIR="$ROOT_DIR/build"

pyinstaller prod_run.spec --distpath "$DIST_DIR" --workpath "$BUILD_DIR"
echo "-> Built executable at: $ROOT_DIR/dist/your_app_name"
echo "done"
