#!/bin/bash
# Test script for interactive menu

source venv/bin/activate

# Test 1: Quick test option
echo "=== Test 1: Quick Test Option ==="
echo "3" | timeout 5 python benchlab.py 2>&1 | head -20

echo ""
echo "=== Test 2: Exit option ==="
echo "4" | python benchlab.py 2>&1 | head -15
