# 📘 BenchLab v2.0 Usage Guide

## Quick Reference

### List All Available Tests
```bash
./run.sh --list-tests
```

### Run Specific Categories
```bash
# All tests (default)
./run.sh

# Single category
./run.sh --categories disk
./run.sh --categories cpu
./run.sh --categories memory
./run.sh --categories gpu

# Multiple categories
./run.sh --categories disk,cpu
./run.sh --categories cpu,memory,gpu
```

### Run Specific Individual Tests
```bash
# Single test
./run.sh --tests disk.seq-read

# Multiple tests
./run.sh --tests disk.seq-read,disk.seq-write
./run.sh --tests cpu.single-int,cpu.multi,mem.l1

# Mix across categories
./run.sh --tests disk.seq-write,cpu.multi,gpu.matrix
```

### Configure Test Parameters

#### Disk Configuration
```bash
# File size (in MB)
./run.sh --size 500

# Block size (in KB)
./run.sh --block 8

# Test directory
./run.sh --dir /Volumes/ExternalSSD

# Combine
./run.sh --categories disk --size 1000 --block 16 --dir /tmp
```

#### CPU Configuration
```bash
# Single-core test duration (seconds)
./run.sh --categories cpu --cpu-duration 10

# Multi-core test duration (seconds)
./run.sh --categories cpu --cpu-multi-duration 20

# Both
./run.sh --categories cpu --cpu-duration 10 --cpu-multi-duration 30
```

#### Memory Configuration
```bash
# Memory buffer size (in MB)
./run.sh --categories memory --mem-size 500

# Quick small test
./run.sh --categories memory --mem-size 50
```

#### GPU Configuration
```bash
# GPU iteration count
./run.sh --categories gpu --gpu-iterations 200

# Quick GPU test
./run.sh --categories gpu --gpu-iterations 50
```

---

## Common Use Cases

### 1. Quick System Check (30 seconds)
```bash
./demo.sh
# Or
./run.sh --categories disk --size 50
```

### 2. CPU Performance Test (2-5 minutes)
```bash
# Standard
./run.sh --categories cpu

# Quick
./run.sh --categories cpu --cpu-duration 3 --cpu-multi-duration 5

# Extended
./run.sh --categories cpu --cpu-duration 10 --cpu-multi-duration 20
```

### 3. Memory Bandwidth Test (2-5 minutes)
```bash
# Standard
./run.sh --categories memory

# Quick with smaller buffer
./run.sh --categories memory --mem-size 50

# Large buffer for sustained testing
./run.sh --categories memory --mem-size 500
```

### 4. GPU/AI Performance (2-10 minutes)
```bash
# Standard
./run.sh --categories gpu

# Quick test
./run.sh --categories gpu --gpu-iterations 50

# Thorough test
./run.sh --categories gpu --gpu-iterations 200
```

### 5. External Drive Testing
```bash
# Test external SSD
./run.sh --categories disk --dir /Volumes/ExternalSSD --size 500

# Test NAS
./run.sh --categories disk --dir /Volumes/NAS --size 200
```

### 6. Compare Storage Performance
```bash
# Internal drive
./run.sh --tests disk.seq-write,disk.seq-read,disk.rand-read --size 500

# External drive
./run.sh --tests disk.seq-write,disk.seq-read,disk.rand-read --size 500 --dir /Volumes/External
```

### 7. Selective Testing
```bash
# Only sequential disk tests
./run.sh --tests disk.seq-read,disk.seq-write

# Only cache tests
./run.sh --tests mem.l1,mem.l2,mem.l3

# AI-specific tests
./run.sh --tests gpu.matrix,gpu.transformer,gpu.inference

# CPU multi-core only
./run.sh --tests cpu.multi --cpu-multi-duration 30
```

### 8. Full System Benchmark with Custom Settings
```bash
./run.sh --size 500 --cpu-duration 10 --cpu-multi-duration 20 --mem-size 200 --gpu-iterations 150
```

---

## Test IDs Reference

### 💾 Disk Tests (4 total)
| Test ID | Description | Metrics |
|---------|-------------|---------|
| `disk.seq-write` | Sequential write | MB/s |
| `disk.seq-read` | Sequential read | MB/s |
| `disk.rand-write` | Random write | MB/s, IOPS |
| `disk.rand-read` | Random read | MB/s, IOPS |

### 🧠 CPU Tests (5 total)
| Test ID | Description | Metrics |
|---------|-------------|---------|
| `cpu.single-int` | Single-core integer | Score, Temp |
| `cpu.single-float` | Single-core float | Score, Temp |
| `cpu.multi` | Multi-core hash | Score, Temp |
| `cpu.compress` | Compression | Score, Temp |
| `cpu.crypto` | Cryptography | Score, Temp |

### 💿 Memory Tests (7 total)
| Test ID | Description | Metrics |
|---------|-------------|---------|
| `mem.seq-read` | Sequential read | GB/s |
| `mem.seq-write` | Sequential write | GB/s |
| `mem.l1` | L1 cache | GB/s |
| `mem.l2` | L2 cache | GB/s |
| `mem.l3` | L3 cache | GB/s |
| `mem.copy` | Memory copy | GB/s |
| `mem.random` | Random access | GB/s |

### 🎮 GPU/AI Tests (6 total)
| Test ID | Description | Metrics |
|---------|-------------|---------|
| `gpu.matrix` | Matrix multiply | GFLOPS, Score |
| `gpu.conv` | 2D convolution | Ops/sec, Score |
| `gpu.element` | Element-wise ops | Ops/sec, Score |
| `gpu.transformer` | Transformer attention | Ops/sec, Score |
| `gpu.memory` | GPU memory BW | GB/s, Score |
| `gpu.inference` | AI inference | FPS, Score |

---

## Configuration Parameter Details

### --size \<MB\>
- **Default**: 100
- **Range**: 10-10000
- **Affects**: Disk tests
- **Example**: `--size 500`
- **Notes**: Larger sizes take longer but better reflect sustained performance

### --block \<KB\>
- **Default**: 4
- **Range**: 1-1024
- **Affects**: Disk tests
- **Example**: `--block 8`
- **Notes**: 4KB is standard for random I/O, larger for sequential

### --dir \<path\>
- **Default**: System temp directory
- **Affects**: Disk tests
- **Example**: `--dir /Volumes/ExternalSSD`
- **Notes**: Specify which drive to test

### --cpu-duration \<seconds\>
- **Default**: 5
- **Range**: 3-60
- **Affects**: Single-core CPU tests
- **Example**: `--cpu-duration 10`
- **Notes**: Longer duration = more accurate but slower

### --cpu-multi-duration \<seconds\>
- **Default**: 10
- **Range**: 5-120
- **Affects**: Multi-core, compression CPU tests
- **Example**: `--cpu-multi-duration 20`
- **Notes**: Heat buildup may affect results on longer tests

### --mem-size \<MB\>
- **Default**: 100
- **Range**: 10-1000
- **Affects**: Memory sequential/copy/random tests
- **Example**: `--mem-size 500`
- **Notes**: Larger buffers test sustained memory bandwidth

### --gpu-iterations \<count\>
- **Default**: 100
- **Range**: 10-1000
- **Affects**: GPU/AI tests
- **Example**: `--gpu-iterations 200`
- **Notes**: More iterations = more accurate but slower

---

## Performance Tips

### 1. Minimize Background Activity
```bash
# Close browsers, IDEs, etc.
# Stop Time Machine backups
# Disable notifications
```

### 2. Temperature Management
```bash
# Run CPU tests with cooling
# Use sudo for temperature monitoring
sudo ./run.sh --categories cpu
```

### 3. Multiple Runs
```bash
# Run tests 2-3 times
./run.sh --categories cpu > run1.txt
./run.sh --categories cpu > run2.txt
./run.sh --categories cpu > run3.txt
```

### 4. Test Specific Workloads
```bash
# For video editing
./run.sh --tests disk.seq-read,disk.seq-write,mem.seq-read --size 1000

# For database
./run.sh --tests disk.rand-read,disk.rand-write,mem.random --size 500

# For AI/ML
./run.sh --categories gpu,memory --mem-size 500 --gpu-iterations 200
```

---

## Interpreting Results

### Disk Results
- **Sequential**: Higher MB/s = better for large files
- **Random IOPS**: Higher = better for databases/apps
- **SSD vs HDD**: SSDs 10-100x faster on random I/O

### CPU Results
- **Score**: Normalized metric, higher = better
- **Temperature**: <80°C good, >90°C may throttle
- **Single vs Multi**: Compare to see per-core scaling

### Memory Results
- **Bandwidth**: Higher GB/s = better
- **Cache hierarchy**: L1 > L2 > L3 > RAM
- **Unified memory**: Apple Silicon shows different patterns

### GPU Results
- **GFLOPS**: Raw compute, higher = better
- **Inference FPS**: Real-world AI speed
- **Score**: Normalized across tests

---

## Troubleshooting

### Tables Not Rendering
- Update Rich library: `pip install --upgrade rich`
- Try running in a different terminal

### GPU Tests Fail
```bash
# Ensure PyTorch with Metal is installed
pip install torch torchvision

# Check if GPU is available
python -c "import torch; print(torch.backends.mps.is_available())"
```

### Temperature Not Showing
```bash
# Run with sudo on macOS
sudo ./run.sh --categories cpu
```

### Tests Too Slow
```bash
# Reduce test durations
./run.sh --categories cpu --cpu-duration 3 --cpu-multi-duration 5

# Run only specific tests
./run.sh --tests cpu.single-int,cpu.multi

# Reduce file sizes
./run.sh --categories disk --size 50
```

### Tests Too Fast / Inaccurate
```bash
# Increase durations
./run.sh --categories cpu --cpu-duration 10 --cpu-multi-duration 30

# Larger files
./run.sh --categories disk --size 500

# More iterations
./run.sh --categories gpu --gpu-iterations 200
```

---

## Advanced Examples

### Benchmark Script for CI/CD
```bash
#!/bin/bash
# benchmark.sh - Automated benchmarking

./run.sh --categories all \
  --size 500 \
  --cpu-duration 10 \
  --cpu-multi-duration 20 \
  --mem-size 200 \
  --gpu-iterations 100 \
  > benchmark_results_$(date +%Y%m%d_%H%M%S).txt
```

### Compare Before/After Upgrade
```bash
# Before upgrade
./run.sh > before.txt

# After upgrade
./run.sh > after.txt

# Compare
diff before.txt after.txt
```

### Focus on Bottlenecks
```bash
# If disk is slow
./run.sh --categories disk --size 1000 --block 4,8,16,32

# If CPU is slow
sudo ./run.sh --categories cpu --cpu-duration 20 --cpu-multi-duration 40

# If memory is slow
./run.sh --categories memory --mem-size 500
```

---

## Getting Help

```bash
# Show all options
./run.sh --help

# List available tests
./run.sh --list-tests

# Quick start guide
cat QUICKSTART_V2.md

# Full documentation
cat README.md
```
