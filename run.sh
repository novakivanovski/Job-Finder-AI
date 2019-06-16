#!/bin/bash

find . -name '*.pyc' -delete
find . -type d -name "__pycache__" -delete

pytest --junitxml=report.xml
