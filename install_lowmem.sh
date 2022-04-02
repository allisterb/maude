#! /bin/bash
set -e

pip install wheel
pip install ext/nsfw_model --no-cache-dir
pip install ext/NudeNet
pip install -r maude/requirements.txt
