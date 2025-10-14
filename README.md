# ⚡ BenchLab

A colorful and vibrant Terminal UI (TUI) application for benchmarking disk performance with animated graphics.

## Features

- 📝 **Sequential Write** - Tests large file sequential write performance
- 📖 **Sequential Read** - Tests large file sequential read performance
- 🎲 **Random Write** - Tests random I/O write performance with IOPS metrics
- 🎯 **Random Read** - Tests random I/O read performance with IOPS metrics
- 🎨 **Animated TUI** - Beautiful, colorful interface with real-time progress
- 📊 **Detailed Results** - Throughput (MB/s) and IOPS metrics for each test

## Installation

### Quick Setup

1. Clone or navigate to the repository:
```bash
cd /Users/willsauter/Development/benchlab
```

2. Run the setup script:
```bash
./setup.sh
```

This creates a virtual environment and installs all dependencies automatically.

### Manual Setup

If you prefer manual setup:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Quick Start

Use the run script (recommended):
```bash
./run.sh
```

### Basic Usage

Or activate the virtual environment and run directly:
```bash
source venv/bin/activate
python benchlab.py
```

### Custom Configuration

Customize file size, block size, and test directory:
```bash
# Test with 500MB file
python benchlab.py --size 500

# Test with 8KB block size
python benchlab.py --block 8

# Test in specific directory
python benchlab.py --dir /path/to/test/directory

# Combine options
python benchlab.py --size 1000 --block 16 --dir /tmp/benchmarks
```

### Command Line Options

- `--size <MB>` - Test file size in megabytes (default: 100)
- `--block <KB>` - Block size in kilobytes (default: 4)
- `--dir <path>` - Test directory path (default: system temp directory)

## What It Tests

### Sequential Operations
Tests large continuous read/write operations, typical of:
- Large file transfers
- Video streaming
- Database backups
- Log file writing

### Random Operations
Tests random access patterns with IOPS measurement, typical of:
- Database queries
- Application loading
- Web server operations
- Virtual machine storage

## Understanding Results

### Throughput (MB/s)
- Higher is better
- Measures data transfer rate
- Important for large file operations

### IOPS (I/O Operations Per Second)
- Higher is better
- Measures random access performance
- Important for database and application workloads

## Requirements

- Python 3.7+
- Rich library (for TUI graphics)

## Architecture

```
benchlab/
├── benchmark.py         # Core benchmarking engine
├── benchlab_tui.py      # Rich-based TUI interface
├── benchlab.py          # Main entry point
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Example Output

```
⚡ BENCHLAB ⚡
Disk Performance Benchmarking Tool

┌─ Configuration ─────────────┐
│ 📁 Test Directory: /tmp     │
│ 📊 File Size: 100 MB        │
│ 🔲 Block Size: 4 KB         │
└─────────────────────────────┘

┌─ Benchmark Results ─────────┐
│ Test              │ MB/s    │
├───────────────────┼─────────┤
│ ✓ Sequential Write│ 450.23  │
│ ✓ Sequential Read │ 890.15  │
│ ✓ Random Write    │ 125.45  │
│ ✓ Random Read     │ 234.78  │
└─────────────────────────────┘
```

## Tips

1. **Close other applications** - For accurate results, minimize disk activity
2. **Test on target drive** - Use `--dir` to test specific drives/partitions
3. **Multiple runs** - Run multiple times and compare results
4. **SSD vs HDD** - SSDs typically show much higher IOPS
5. **File size matters** - Larger files may reveal caching effects

## License

Open source - feel free to use and modify!

## Author

Created with ⚡ by BenchLab
