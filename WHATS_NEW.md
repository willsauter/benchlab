# 🎉 What's New in BenchLab v2.0

## ✅ Issues Fixed

### 1. Table Rendering Issue
**Problem**: Results tables were showing `<rich.table.Table object>` instead of actual data

**Fix**: Updated to use `rich.console.Group` for proper table rendering in panels

**Result**: Tables now display correctly with all results visible

### 2. Test Selection
**Problem**: Could only run entire categories, not individual tests

**Fix**: Added `--tests` parameter for granular test selection

**Result**: Can now run any combination of tests:
```bash
# Examples
./run.sh --tests disk.seq-read,cpu.multi
./run.sh --tests mem.l1,mem.l2,mem.l3
./run.sh --tests gpu.matrix,gpu.inference
```

### 3. Configuration Options
**Problem**: Limited ability to configure test parameters

**Fix**: Added comprehensive configuration options:
- `--size` - Disk file size
- `--block` - Disk block size
- `--cpu-duration` - CPU single-core test duration
- `--cpu-multi-duration` - CPU multi-core test duration
- `--mem-size` - Memory buffer size
- `--gpu-iterations` - GPU test iterations

**Result**: Full control over test parameters:
```bash
./run.sh --size 500 --cpu-duration 10 --mem-size 200
```

---

## 🆕 New Features

### 1. Test Discovery
```bash
# List all available tests with descriptions
./run.sh --list-tests
```

Shows 22 total tests across 4 categories with IDs and descriptions.

### 2. Individual Test Selection
```bash
# Run specific tests by ID
./run.sh --tests disk.seq-write,cpu.multi,mem.l1

# Mix tests from different categories
./run.sh --tests disk.seq-read,gpu.matrix
```

### 3. Enhanced Help System
```bash
# Show all options with examples
./run.sh --help
```

Includes:
- Parameter descriptions
- Example commands
- Test category information
- Configuration guidance

### 4. Flexible Configuration
Every test type now has configurable parameters:

**Disk Tests**:
- File size: `--size 500` (MB)
- Block size: `--block 8` (KB)
- Directory: `--dir /path`

**CPU Tests**:
- Single-core duration: `--cpu-duration 10` (seconds)
- Multi-core duration: `--cpu-multi-duration 20` (seconds)

**Memory Tests**:
- Buffer size: `--mem-size 200` (MB)

**GPU Tests**:
- Iterations: `--gpu-iterations 150`

### 5. Memory Random Access Test
Added new memory test: `mem.random` - Tests random memory access patterns

---

## 📊 Test Catalog

### All Available Tests (22 total)

#### 💾 Disk (4 tests)
- `disk.seq-write` - Sequential write
- `disk.seq-read` - Sequential read
- `disk.rand-write` - Random write with IOPS
- `disk.rand-read` - Random read with IOPS

#### 🧠 CPU (5 tests)
- `cpu.single-int` - Single-core integer
- `cpu.single-float` - Single-core float
- `cpu.multi` - Multi-core hash
- `cpu.compress` - Compression
- `cpu.crypto` - Cryptography

#### 💿 Memory (7 tests)
- `mem.seq-read` - Sequential read
- `mem.seq-write` - Sequential write
- `mem.l1` - L1 cache
- `mem.l2` - L2 cache
- `mem.l3` - L3 cache
- `mem.copy` - Memory copy
- `mem.random` - Random access ⭐ NEW

#### 🎮 GPU/AI (6 tests)
- `gpu.matrix` - Matrix multiply
- `gpu.conv` - 2D convolution
- `gpu.element` - Element-wise ops
- `gpu.transformer` - Transformer attention
- `gpu.memory` - GPU memory bandwidth
- `gpu.inference` - AI inference

---

## 🚀 Usage Examples

### Before (Limited Options)
```bash
# Could only run entire categories
./run.sh --categories disk
./run.sh --categories cpu,memory
```

### After (Full Flexibility)
```bash
# Run specific tests
./run.sh --tests disk.seq-read,disk.seq-write

# Configure parameters
./run.sh --categories disk --size 500 --block 8

# Combine both
./run.sh --tests cpu.multi,mem.l1 --cpu-multi-duration 20 --mem-size 200

# Quick focused test
./run.sh --tests gpu.matrix,gpu.inference --gpu-iterations 50
```

---

## 💡 Use Case Examples

### 1. Quick Storage Check
```bash
./run.sh --tests disk.seq-read,disk.seq-write --size 100
```
⏱️ **Time**: ~10 seconds

### 2. CPU Stress Test
```bash
sudo ./run.sh --tests cpu.multi --cpu-multi-duration 60
```
⏱️ **Time**: ~1 minute  
🌡️ **Monitors**: Temperature under sustained load

### 3. Cache Hierarchy Analysis
```bash
./run.sh --tests mem.l1,mem.l2,mem.l3 --mem-size 100
```
⏱️ **Time**: ~15 seconds  
📊 **Shows**: Memory subsystem performance

### 4. AI Workload Simulation
```bash
./run.sh --tests gpu.matrix,gpu.transformer,gpu.inference --gpu-iterations 100
```
⏱️ **Time**: ~2 minutes  
🤖 **Tests**: Real AI operations

### 5. External Drive Testing
```bash
./run.sh --categories disk --dir /Volumes/ExternalSSD --size 500 --block 4
```
⏱️ **Time**: ~30 seconds  
💾 **Compares**: Different drives

### 6. Custom Full Benchmark
```bash
./run.sh \
  --size 500 \
  --cpu-duration 10 \
  --cpu-multi-duration 20 \
  --mem-size 200 \
  --gpu-iterations 150
```
⏱️ **Time**: ~10 minutes  
🔬 **Thorough**: Complete system profile

---

## 📝 Configuration Guidelines

### Quick Tests (1-2 minutes)
```bash
--size 50
--cpu-duration 3
--cpu-multi-duration 5
--mem-size 50
--gpu-iterations 50
```

### Standard Tests (5-8 minutes) ⭐ DEFAULT
```bash
--size 100
--cpu-duration 5
--cpu-multi-duration 10
--mem-size 100
--gpu-iterations 100
```

### Thorough Tests (15-20 minutes)
```bash
--size 500
--cpu-duration 10
--cpu-multi-duration 30
--mem-size 500
--gpu-iterations 200
```

### Extended Tests (30-60 minutes)
```bash
--size 1000
--cpu-duration 20
--cpu-multi-duration 60
--mem-size 1000
--gpu-iterations 500
```

---

## 🎯 Best Practices

### 1. Start with List
```bash
# See what's available
./run.sh --list-tests
```

### 2. Test Incrementally
```bash
# Start with one category
./run.sh --categories disk

# Then add others
./run.sh --categories disk,cpu
```

### 3. Use Specific Tests for Debugging
```bash
# If disk seems slow
./run.sh --tests disk.rand-read,disk.rand-write

# If CPU throttling suspected
sudo ./run.sh --tests cpu.multi --cpu-multi-duration 30
```

### 4. Configure for Your Use Case
```bash
# Video editing workload
./run.sh --tests disk.seq-read,disk.seq-write,mem.seq-read --size 1000

# Database workload
./run.sh --tests disk.rand-read,disk.rand-write,mem.random --size 500

# AI/ML workload
./run.sh --categories gpu,memory --mem-size 500 --gpu-iterations 200
```

### 5. Save Results
```bash
# Create dated logs
./run.sh > results_$(date +%Y%m%d).txt

# Compare over time
./run.sh --categories cpu > cpu_$(date +%Y%m%d).txt
```

---

## 🔧 Technical Changes

### Code Updates
1. **benchlab_tui_full.py**:
   - Fixed table rendering with `rich.console.Group`
   - Added `should_run_test()` method for test filtering
   - Added `config` dictionary for parameters
   - Updated all test calls to use configuration

2. **Argument Parser**:
   - Added `--tests` for individual test selection
   - Added `--list-tests` for test discovery
   - Added configuration parameters for all test types
   - Enhanced help text with examples

3. **Test Execution**:
   - Tests now check if they should run via `should_run_test()`
   - All tests use configured parameters
   - Proper test ID mapping (e.g., `disk.seq-write`, `cpu.multi`)

---

## 📚 New Documentation

1. **USAGE_GUIDE.md** - Comprehensive usage guide
   - All test IDs and descriptions
   - Configuration parameter details
   - Common use cases with examples
   - Performance tips
   - Troubleshooting guide

2. **WHATS_NEW.md** - This file
   - What changed and why
   - New features explained
   - Usage examples
   - Migration guide

---

## ⬆️ Upgrading from v1.0

### What's Compatible
- All v1.0 commands still work
- Default parameters unchanged
- Output format similar

### What's New
- Can now select individual tests
- Can configure all parameters
- Better table rendering
- More memory tests

### Migration Examples

**v1.0 Style** (still works):
```bash
./run.sh
./run.sh --categories disk
./run.sh --size 500
```

**v2.0 Style** (new capabilities):
```bash
./run.sh --list-tests
./run.sh --tests disk.seq-read,cpu.multi
./run.sh --categories cpu --cpu-duration 10
```

---

## 🚀 Next Steps

1. **Try the new features:**
   ```bash
   ./run.sh --list-tests
   ./run.sh --tests disk.seq-read
   ```

2. **Explore configuration:**
   ```bash
   ./run.sh --help
   ./run.sh --categories disk --size 500
   ```

3. **Read the guides:**
   - `USAGE_GUIDE.md` - Complete usage reference
   - `QUICKSTART_V2.md` - Quick start guide
   - `README.md` - Full documentation

4. **Run your workload:**
   ```bash
   # Find the tests that match your use case
   ./run.sh --list-tests
   
   # Run those specific tests
   ./run.sh --tests <your-tests>
   ```

---

**BenchLab v2.0 - More flexible, more powerful, same ease of use!** ⚡
