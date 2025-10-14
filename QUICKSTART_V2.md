# 🚀 BenchLab v2.0 Quick Start

## First Time Setup

```bash
cd /Users/willsauter/Development/benchlab
./setup.sh
```

⏱️ **Time**: ~30 seconds (downloads PyTorch + dependencies)

## Running BenchLab

### Full System Benchmark (Recommended)
```bash
./run.sh
```
Tests: Disk, CPU, Memory, GPU/AI  
⏱️ **Time**: ~8 minutes

### Quick Demo (Disk Only)
```bash
./demo.sh
```
⏱️ **Time**: ~30 seconds

### Category-Specific Tests

```bash
# CPU tests only (~2 minutes)
./run.sh --categories cpu

# Memory tests only (~2 minutes)
./run.sh --categories memory

# GPU/AI tests only (~3 minutes)
./run.sh --categories gpu

# Disk tests only (~30 seconds)
./run.sh --categories disk

# Multiple categories
./run.sh --categories cpu,memory
```

## What Gets Tested

| Category | Tests | Time | Key Metrics |
|----------|-------|------|-------------|
| 💾 **Disk** | Sequential R/W, Random R/W | ~30s | MB/s, IOPS |
| 🧠 **CPU** | Integer, Float, Multi-core, Compression, Crypto | ~2min | Score, Temp |
| 💿 **Memory** | Sequential, L1/L2/L3 Cache, Random, Copy | ~2min | GB/s Bandwidth |
| 🎮 **GPU/AI** | Matrix Multiply, Convolution, Transformer, Inference | ~3min | GFLOPS, Score |

## Command Options

```bash
./run.sh [OPTIONS]

--categories <list>    Categories: all, disk, cpu, memory, gpu (default: all)
--size <MB>           Disk file size in MB (default: 100)
--block <KB>          Disk block size in KB (default: 4)  
--dir <path>          Disk test directory (default: temp)
```

## Examples

**Test external drive:**
```bash
./run.sh --categories disk --dir /Volumes/ExternalSSD
```

**Quick CPU+Memory check:**
```bash
./run.sh --categories cpu,memory
```

**Full benchmark with large disk test:**
```bash
./run.sh --size 500
```

**GPU performance only:**
```bash
./run.sh --categories gpu
```

## Understanding Your Results

### 💾 Disk
- **Good SSD**: 500+ MB/s sequential, 50K+ IOPS
- **Great SSD**: 2000+ MB/s sequential, 200K+ IOPS

### 🧠 CPU  
- **Single-Core Score**: 5-10 (good), 10-20 (great)
- **Multi-Core Score**: 20-40 (good), 40-80 (great)
- **Temperature**: <80°C normal, >90°C throttling

### 💿 Memory
- **RAM Bandwidth**: 40-80 GB/s (good), 80-150 GB/s (great)
- **L1 Cache**: 300-500 GB/s typical
- **L2 Cache**: 200-400 GB/s typical

### 🎮 GPU (Apple Silicon)
- **Matrix Multiply**: 2-4 TFLOPS (good), 4-8 TFLOPS (great)
- **AI Inference**: 30-60 fps (good), 60-120 fps (great)

## Troubleshooting

**GPU tests fail?**
- Ensure you're on Apple Silicon (M1/M2/M3)
- Run `./setup.sh` to install PyTorch

**Temperature not showing?**
- Run with sudo: `sudo ./run.sh`
- Temperature monitoring requires elevated privileges on macOS

**Tests too slow?**
- Close other applications
- Ensure adequate cooling for CPU tests
- Use SSD for disk tests

**Want faster tests?**
- Use `--categories` to run specific tests
- Reduce `--size` for smaller disk tests
- Use `./demo.sh` for quickest check

## Tips

✅ **Best practices:**
- Close Chrome/browsers (memory hog)
- Unplug from charger for battery test
- Multiple runs for consistency
- Compare against similar hardware

❌ **Avoid:**
- Running during Time Machine backup
- Testing network drives (slow)
- Running on battery (CPU throttling)
- Multiple benchmarks simultaneously

## Next Steps

After running, you'll see results organized by category:

```
💾 Disk Average: 1200 MB/s
🧠 CPU Average Score: 28.5 (Temp: 72.3°C)
💿 Memory Average: 95.2 GB/s
🎮 GPU Average Score: 42.8
```

Compare these to:
- Your previous runs (track over time)
- Similar hardware specs
- Before/after system changes

---

**Ready to benchmark?** Run `./run.sh` now! ⚡

*See README.md for complete documentation*
