# ⚡ BenchLab

A comprehensive system performance benchmarking suite with a colorful and vibrant Terminal UI (TUI). Test your entire system: Disk, CPU, Memory, and GPU/AI capabilities.

## Features

### 💾 Disk I/O
- 📝 **Sequential Write** - Large file write performance
- 📖 **Sequential Read** - Large file read performance
- 🎲 **Random Write** - Random I/O with IOPS metrics
- 🎯 **Random Read** - Random I/O with IOPS metrics

### 🧠 CPU Performance
- 🔢 **Single-Core Integer** - Prime number calculations
- ➗ **Single-Core Float** - Floating point operations
- 🔐 **Multi-Core Hash** - Parallel hashing across all cores
- 📦 **Compression** - Real-world compression workload
- 🔒 **Cryptography** - Cryptographic operations
- 🌡️ **Temperature Monitoring** - CPU temperature tracking (macOS)

### 💿 Memory Bandwidth
- 📖 **Sequential Read/Write** - Memory bandwidth testing
- ⚡ **L1/L2/L3 Cache** - Cache hierarchy performance
- 🎲 **Random Access** - Random memory access patterns
- 📋 **Memory Copy** - Copy bandwidth testing

### 🎮 GPU/AI (Apple Silicon)
- 🔢 **Matrix Multiply** - GEMM performance (GFLOPS)
- 🎨 **2D Convolution** - CNN operations
- ➕ **Element-wise Ops** - GPU compute operations
- 🤖 **Transformer Attention** - Modern AI workloads
- 💾 **GPU Memory Bandwidth** - GPU memory throughput
- 🧠 **AI Inference** - Neural network inference speed

### 🎨 Interface
- **Animated TUI** - Beautiful, colorful real-time interface
- **Live Progress** - Smooth 10 FPS progress bars
- **Category Results** - Organized results by subsystem
- **Comprehensive Metrics** - Throughput, IOPS, bandwidth, scores

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

Run specific test categories or customize settings:
```bash
# Run only disk tests
./run.sh --categories disk

# Run only CPU and memory tests
./run.sh --categories cpu,memory

# Run all tests with custom disk settings
./run.sh --size 500 --block 8 --dir /path/to/test

# GPU/AI tests only
./run.sh --categories gpu
```

### Command Line Options

- `--categories <list>` - Categories to test: all, disk, cpu, memory, gpu (comma-separated, default: all)
- `--size <MB>` - Disk test file size in megabytes (default: 100)
- `--block <KB>` - Disk block size in kilobytes (default: 4)
- `--dir <path>` - Disk test directory path (default: system temp directory)

### Examples

```bash
# Quick CPU benchmark only
./run.sh --categories cpu

# Test external SSD
./run.sh --categories disk --dir /Volumes/ExternalSSD

# Complete system benchmark with large disk test
./run.sh --size 1000

# Memory and GPU only
./run.sh --categories memory,gpu
```

## What It Tests

### 💾 Disk I/O Tests
**Sequential Operations** - Large continuous read/write:
- Large file transfers
- Video streaming
- Database backups
- Log file writing

**Random Operations** - Random access with IOPS:
- Database queries
- Application loading
- Web server operations
- Virtual machine storage

### 🧠 CPU Tests
**Integer Performance** - Prime number calculations test single-core integer throughput

**Floating Point** - Mathematical operations test FPU performance

**Multi-Core** - Parallel hashing tests all CPU cores simultaneously

**Compression** - Real-world workload testing sustained performance

**Cryptography** - Hash algorithms test crypto acceleration

**Temperature** - Monitors CPU temperature under load (requires sudo on macOS)

### 💿 Memory Tests
**Sequential Bandwidth** - Measures RAM read/write speeds

**Cache Hierarchy** - Tests L1, L2, L3 cache performance at different buffer sizes

**Random Access** - Tests non-sequential memory access patterns

**Memory Copy** - Measures memory-to-memory transfer speeds

### 🎮 GPU/AI Tests (Apple Silicon Only)
**Matrix Multiply** - Core AI operation measuring GFLOPS

**Convolution** - Tests CNN layers common in image processing

**Element-wise** - GPU compute shader performance

**Transformer Attention** - Modern LLM workload simulation

**GPU Memory** - Tests bandwidth between GPU and its memory

**AI Inference** - Complete neural network inference speed

## Understanding Results

### Disk Metrics
**Throughput (MB/s)** - Higher is better, measures data transfer rate

**IOPS** - I/O operations per second, critical for random access workloads

### CPU Metrics
**Ops/sec** - Operations per second for the specific workload

**Score** - Normalized performance score for easy comparison

**Temperature** - CPU temperature in Celsius (requires sudo on macOS)

### Memory Metrics
**Bandwidth (GB/s)** - Memory transfer speed, higher is better

**Buffer Size** - Size of data tested (shows cache hierarchy performance)

### GPU Metrics
**Ops/sec** - GPU operations per second

**Score** - Normalized GPU performance score

**GFLOPS** - Floating point operations per second (matrix multiply)

### Typical Results (MacBook Pro M1/M2)
- **Disk SSD**: 500-3000 MB/s sequential, 50K-250K IOPS
- **CPU**: Score 5-15 single-core, 20-50 multi-core
- **Memory**: 50-200 GB/s bandwidth, L1 cache: 400+ GB/s
- **GPU**: Matrix multiply 2-5 TFLOPS, Inference 20-100 fps

## Requirements

- Python 3.7+
- Rich library (for TUI graphics)
- PyTorch 2.0+ (for GPU/AI tests on Apple Silicon)

## Architecture

```
benchlab/
├── benchmark.py           # Disk I/O benchmarking engine
├── cpu_benchmark.py       # CPU performance tests
├── memory_benchmark.py    # Memory bandwidth tests
├── gpu_benchmark.py       # GPU/AI tests (Metal/PyTorch)
├── benchlab_tui_full.py   # Comprehensive TUI interface
├── benchlab.py            # Main entry point
├── requirements.txt       # Python dependencies
├── setup.sh               # Automated setup
└── README.md              # This file
```

## Example Output

```
⚡ BENCHLAB ⚡
System Performance Benchmarking Suite

┌─ Configuration ─────────────────┐
│ 💾 Disk Test: 100 MB file       │
│ 🔲 Block Size: 4 KB             │
│ 🧠 CPU Cores: 10                │
│ 🎮 GPU: Metal (Apple Silicon)   │
│ 📊 Categories: DISK,CPU,MEM,GPU │
└─────────────────────────────────┘

┌─ 💾 DISK I/O ───────────────────┐
│ ✓ Sequential Write │ 640 MB/s  │
│ ✓ Sequential Read  │ 2838 MB/s │
│ ✓ Random Write     │ 14K IOPS  │
│ ✓ Random Read      │ 261K IOPS │
└─────────────────────────────────┘

┌─ 🧠 CPU ────────────────────────┐
│ ✓ Single-Core Int  │ Score: 8.5│
│ ✓ Multi-Core Hash  │ Score: 42 │
│ ✓ Compression      │ Score: 15 │
│ Average Temp: 68.3°C            │
└─────────────────────────────────┘

┌─ 💿 MEMORY ─────────────────────┐
│ ✓ Sequential Read  │ 85.2 GB/s │
│ ✓ L1 Cache         │ 450 GB/s  │
│ ✓ L2 Cache         │ 380 GB/s  │
│ ✓ L3 Cache         │ 180 GB/s  │
└─────────────────────────────────┘

┌─ 🎮 GPU/AI ─────────────────────┐
│ ✓ Matrix Multiply  │ 3.2 TFLOPS│
│ ✓ Transformer Attn │ Score: 45 │
│ ✓ AI Inference     │ 85 fps    │
└─────────────────────────────────┘
```

## Tips

### General
1. **Close other applications** - Minimize background activity for accurate results
2. **Multiple runs** - Run tests 2-3 times and compare for consistency
3. **Category selection** - Use `--categories` to run only specific tests
4. **Time estimates** - Full suite: ~8 minutes, individual categories: 30s-3min

### Disk Tests
5. **Test target drives** - Use `--dir` to test specific drives/partitions
6. **SSD vs HDD** - SSDs show much higher IOPS (50K+ vs 100-200)
7. **File size** - Larger files reveal caching behavior

### CPU Tests
8. **Temperature monitoring** - Run with sudo for accurate temps: `sudo ./run.sh`
9. **Cooling matters** - CPU throttling affects multi-core scores
10. **Single vs Multi** - Compare single-core to see per-core performance

### Memory Tests
11. **Cache hierarchy** - L1 > L2 > L3 > RAM shows memory subsystem quality
12. **Bandwidth varies** - Unified memory (Apple Silicon) shows different patterns

### GPU/AI Tests  
13. **Metal requirement** - Requires Apple Silicon and PyTorch
14. **Inference speed** - Good indicator for local AI workloads
15. **Matrix performance** - GFLOPS indicate raw compute capability

## License

Open source - feel free to use and modify!

## Author

Created with ⚡ by BenchLab
