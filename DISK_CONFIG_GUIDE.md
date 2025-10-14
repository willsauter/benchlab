# 💾 Disk Test Configuration Guide

## Overview

All disk tests now support dynamic configuration of file size and block size parameters. You can customize these settings globally via command-line arguments, and they will apply to all disk tests in that run.

---

## Configuration Parameters

### --size \<MB\>
**Description**: Test file size in megabytes  
**Default**: 100 MB  
**Range**: 10 - 10,000 MB  
**Affects**: All disk tests (sequential and random)

**Purpose**:
- Larger files test sustained performance
- Smaller files for quick checks
- Match your typical workload size

### --block \<KB\>
**Description**: Block size for I/O operations in kilobytes  
**Default**: 4 KB  
**Range**: 1 - 1024 KB  
**Affects**: All disk tests

**Purpose**:
- 4 KB: Standard for random I/O, databases
- 8 KB: Common for filesystems
- 16-32 KB: Better for sequential workloads
- 64-128 KB: Large sequential transfers
- 1024 KB (1 MB): Maximum throughput testing

---

## Usage Examples

### Standard Test
```bash
# Default: 100 MB file, 4 KB blocks
./run.sh --categories disk
```

### Quick Test
```bash
# Small file for fast testing
./run.sh --categories disk --size 50
```

### Large File Test
```bash
# Large file for sustained performance
./run.sh --categories disk --size 500
```

### Different Block Sizes
```bash
# 8 KB blocks
./run.sh --categories disk --block 8

# 16 KB blocks
./run.sh --categories disk --block 16

# 128 KB blocks for sequential
./run.sh --categories disk --block 128
```

### Combined Configuration
```bash
# 500 MB file with 16 KB blocks
./run.sh --categories disk --size 500 --block 16

# 1 GB file with 64 KB blocks
./run.sh --categories disk --size 1000 --block 64
```

### Specific Tests with Custom Settings
```bash
# Only sequential tests, 200 MB, 32 KB blocks
./run.sh --tests disk.seq-write,disk.seq-read --size 200 --block 32

# Only random tests, 100 MB, 4 KB blocks
./run.sh --tests disk.rand-write,disk.rand-read --size 100 --block 4
```

### External Drive Testing
```bash
# Test external SSD with large file
./run.sh --categories disk --dir /Volumes/ExternalSSD --size 1000 --block 8

# Test network drive with appropriate settings
./run.sh --categories disk --dir /Volumes/NetworkShare --size 200 --block 64
```

---

## Performance Impact

### File Size Effects

**Small Files (10-50 MB)**:
- ✅ Fast execution (~5-10 seconds)
- ✅ Good for quick checks
- ⚠️ May not reflect sustained performance
- ⚠️ Cache effects more prominent

**Medium Files (100-200 MB)**:
- ✅ Balanced testing (~10-20 seconds)
- ✅ Default recommended size
- ✅ Good mix of speed and accuracy
- ✅ Minimizes cache effects

**Large Files (500-1000 MB)**:
- ✅ Tests sustained performance
- ✅ Best for thorough evaluation
- ⚠️ Takes longer (~30-60 seconds)
- ⚠️ Requires more disk space

### Block Size Effects

**Small Blocks (4 KB)**:
- ✅ Standard for databases
- ✅ Realistic for random I/O
- ✅ Shows true IOPS capability
- ⚠️ Slower for sequential

**Medium Blocks (8-32 KB)**:
- ✅ Good balance
- ✅ Common filesystem sizes
- ✅ Better sequential performance
- ✅ Still relevant for random I/O

**Large Blocks (64-128 KB+)**:
- ✅ Maximum sequential throughput
- ✅ Good for video/large files
- ⚠️ Not realistic for random I/O
- ⚠️ IOPS metrics less meaningful

---

## Workload-Specific Recommendations

### Database Testing
```bash
# 4 KB blocks, focus on random I/O
./run.sh --tests disk.rand-read,disk.rand-write --size 500 --block 4
```

**Why**: Databases primarily use 4 KB or 8 KB pages with random access patterns.

### Video Editing
```bash
# Large files, large blocks
./run.sh --tests disk.seq-read,disk.seq-write --size 1000 --block 128
```

**Why**: Video editing requires sustained sequential read/write of large files.

### Web Server
```bash
# Medium files, small blocks
./run.sh --categories disk --size 200 --block 8
```

**Why**: Web servers have mixed workloads with medium file sizes.

### General Purpose
```bash
# Default settings
./run.sh --categories disk --size 100 --block 4
```

**Why**: Balanced for most common use cases.

### SSD Performance
```bash
# Large file, medium blocks
./run.sh --categories disk --size 500 --block 16
```

**Why**: SSDs excel at both sequential and random, medium blocks show balance.

### HDD Performance
```bash
# Medium file, large blocks for sequential
./run.sh --tests disk.seq-read,disk.seq-write --size 200 --block 64
```

**Why**: HDDs perform best with sequential access and larger blocks.

---

## Understanding Results

### Sequential Tests
**File Size Impact**:
- Larger files → More accurate sustained throughput
- Smaller files → May show inflated numbers due to caching

**Block Size Impact**:
- Larger blocks → Higher MB/s throughput
- Smaller blocks → More realistic for typical usage

### Random Tests
**File Size Impact**:
- Affects test duration and accuracy
- Larger = more representative sample

**Block Size Impact**:
- 4 KB: Standard IOPS measurement
- Larger blocks: Higher throughput, lower IOPS

**IOPS Calculation**:
- IOPS = operations per second
- Each operation reads/writes one block
- Smaller blocks = higher IOPS potential

---

## Troubleshooting

### Test Too Slow
```bash
# Reduce file size
./run.sh --categories disk --size 50

# Or run specific tests only
./run.sh --tests disk.seq-write,disk.seq-read --size 50
```

### Need More Accuracy
```bash
# Increase file size
./run.sh --categories disk --size 500

# Use appropriate block size
./run.sh --categories disk --size 500 --block 4
```

### Unrealistic Results
```bash
# Ensure file size is large enough
./run.sh --categories disk --size 200

# Use realistic block size for your use case
./run.sh --categories disk --size 200 --block 4
```

### Out of Disk Space
```bash
# Use smaller file
./run.sh --categories disk --size 50

# Or specify different directory with more space
./run.sh --categories disk --dir /path/to/larger/drive --size 500
```

---

## Advanced Usage

### Compare Block Sizes
```bash
# Test with different block sizes
./run.sh --tests disk.seq-write --size 200 --block 4 > results_4kb.txt
./run.sh --tests disk.seq-write --size 200 --block 8 > results_8kb.txt
./run.sh --tests disk.seq-write --size 200 --block 16 > results_16kb.txt
./run.sh --tests disk.seq-write --size 200 --block 128 > results_128kb.txt

# Compare results
cat results_*.txt | grep "MB/s"
```

### Compare File Sizes
```bash
# Test with different file sizes
./run.sh --tests disk.seq-read --size 50 --block 4 > results_50mb.txt
./run.sh --tests disk.seq-read --size 100 --block 4 > results_100mb.txt
./run.sh --tests disk.seq-read --size 500 --block 4 > results_500mb.txt

# Compare results
cat results_*.txt | grep "MB/s"
```

### Test Multiple Drives
```bash
# Internal drive
./run.sh --categories disk --size 500 --block 4 > internal_results.txt

# External SSD
./run.sh --categories disk --dir /Volumes/ExternalSSD --size 500 --block 4 > external_ssd_results.txt

# NAS
./run.sh --categories disk --dir /Volumes/NAS --size 500 --block 4 > nas_results.txt

# Compare
diff internal_results.txt external_ssd_results.txt
```

---

## Best Practices

### 1. Match Your Workload
Choose file size and block size that match your actual use case:
- Database? Use 4-8 KB blocks
- Video? Use large files and blocks
- General? Use defaults

### 2. Test Multiple Times
```bash
# Run 3 times for consistency
./run.sh --categories disk --size 200 > run1.txt
./run.sh --categories disk --size 200 > run2.txt
./run.sh --categories disk --size 200 > run3.txt
```

### 3. Close Background Apps
- Stop Time Machine backups
- Close browsers and IDEs
- Disable antivirus scans during test

### 4. Cool Down Between Tests
- Allow disk to cool between runs
- Especially important for sustained tests
- Wait 30-60 seconds between large tests

### 5. Document Your Settings
```bash
# Save test parameters in filename
./run.sh --categories disk --size 500 --block 16 > disk_500mb_16kb_$(date +%Y%m%d).txt
```

---

## Quick Reference

### Common Configurations

| Use Case | Size | Block | Command |
|----------|------|-------|---------|
| Quick test | 50 MB | 4 KB | `--size 50 --block 4` |
| Standard test | 100 MB | 4 KB | *(default)* |
| Database | 500 MB | 4 KB | `--size 500 --block 4` |
| Video editing | 1000 MB | 128 KB | `--size 1000 --block 128` |
| SSD benchmark | 500 MB | 16 KB | `--size 500 --block 16` |
| HDD benchmark | 200 MB | 64 KB | `--size 200 --block 64` |
| Thorough test | 1000 MB | 4 KB | `--size 1000 --block 4` |

---

## Summary

✅ **Dynamic Configuration**: All disk tests support custom file size and block size  
✅ **Command-Line Control**: Easy to adjust via `--size` and `--block` parameters  
✅ **Workload Matching**: Configure tests to match your actual usage patterns  
✅ **Flexible Testing**: From quick 30-second tests to thorough 5-minute evaluations  

**Default**: `--size 100 --block 4` provides balanced, realistic testing for most users.
