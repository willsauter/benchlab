#!/bin/bash

# BenchLab Setup Script
# Creates virtual environment and installs dependencies

echo "🔧 Setting up BenchLab..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To run BenchLab:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the application: python benchlab.py"
echo ""
echo "Or use the run script: ./run.sh"
