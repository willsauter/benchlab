#!/bin/bash

# BenchLab Setup Script
# Creates virtual environment and installs dependencies

echo "🔧 Setting up BenchLab..."

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install Rich first
echo "🎨 Installing Rich library..."
pip install rich>=13.7.0

# Install PyTorch with Metal support for Apple Silicon (if on macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🎮 Installing PyTorch with Metal support for Apple Silicon..."
    pip install torch torchvision
    echo "✓ PyTorch installed with Metal/MPS support"
else
    echo "⚠️  Non-macOS system detected. GPU/AI tests will be unavailable."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run BenchLab:"
echo "  1. Full system benchmark: ./run.sh"
echo "  2. Specific categories: ./run.sh --categories disk,cpu,memory"
echo "  3. Quick demo: ./demo.sh"
echo ""
echo "Available categories: disk, cpu, memory, gpu"
