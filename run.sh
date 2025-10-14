#!/bin/bash

# BenchLab Run Script
# Activates virtual environment and runs the application

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run BenchLab
python benchlab.py "$@"

# Deactivate when done
deactivate
