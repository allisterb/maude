@echo off
pip install wheel
pip install ext\nsfw_model\
pip install ext\NudeNet\
pip install -r maude\requirements.txt
python -m spacy download en_core_web_lg