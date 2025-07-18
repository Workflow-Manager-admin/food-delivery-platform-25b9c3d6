#!/bin/bash
cd /home/kavia/workspace/code-generation/food-delivery-platform-25b9c3d6/food_delivery_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

