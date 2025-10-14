#!/bin/bash

# BenchLab Demo Script
# Runs a quick demo with smaller file size for demonstration

echo "🎬 Starting BenchLab Demo..."
echo "Running quick benchmark with 50MB file size..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run BenchLab with demo settings (smaller file for faster demo)
python benchlab.py --size 50 --block 4

# Deactivate when done
deactivate
