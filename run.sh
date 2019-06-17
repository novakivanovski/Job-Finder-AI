#!/bin/bash

find . -name '*.pyc' -delete
find . -type d -name "__pycache__" -delete

cd ./src
pytest --junitxml=report.xml
