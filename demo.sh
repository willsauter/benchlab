#!/bin/bash

# BenchLab Demo Script
# Runs a quick demo with disk tests only for fast demonstration

echo "🎬 Starting BenchLab Demo..."
echo "Running quick disk benchmark (disk tests only)..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run BenchLab with demo settings (disk only, smaller file)
python benchlab.py --categories disk --size 50

# Deactivate when done
deactivate
