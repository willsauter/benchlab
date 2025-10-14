# 🚀 BenchLab Quick Start

## First Time Setup

```bash
./setup.sh
```

That's it! This creates the virtual environment and installs dependencies.

## Running BenchLab

### Option 1: Quick Run (Recommended)
```bash
./run.sh
```

### Option 2: Demo Mode (Faster)
```bash
./demo.sh
```

### Option 3: Custom Parameters
```bash
./run.sh --size 500 --block 8 --dir /tmp/test
```

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--size` | File size in MB | 100 |
| `--block` | Block size in KB | 4 |
| `--dir` | Test directory | system temp |

## Examples

**Test your home directory:**
```bash
./run.sh --dir ~/
```

**Quick test with small file:**
```bash
./run.sh --size 50
```

**Large test with bigger blocks:**
```bash
./run.sh --size 1000 --block 16
```

**Test external drive:**
```bash
./run.sh --dir /Volumes/ExternalDrive
```

## What You'll See

1. **Welcome Screen** - Animated header
2. **Configuration** - Your test settings
3. **Progress** - Live progress bars for each test
4. **Results** - Table with MB/s and IOPS metrics
5. **Summary** - Average throughput

## Understanding Results

### Good Performance
- **Sequential**: 200+ MB/s (HDD), 500+ MB/s (SSD)
- **Random**: 50+ MB/s (HDD), 200+ MB/s (SSD)
- **IOPS**: 100+ (HDD), 10,000+ (SSD)

### Tests Run
1. ✅ Sequential Write
2. ✅ Sequential Read
3. ✅ Random Write (with IOPS)
4. ✅ Random Read (with IOPS)

## Troubleshooting

**Virtual environment not found?**
```bash
./setup.sh
```

**Permission denied?**
```bash
chmod +x setup.sh run.sh demo.sh
```

**Want to test specific disk?**
```bash
./run.sh --dir /path/to/disk
```

## Tips for Best Results

1. 🚫 Close other applications
2. 📁 Ensure enough disk space (file_size × 2)
3. 🔄 Run multiple times for consistency
4. 💾 Test the actual disk you care about
5. ⚡ SSDs will show much higher IOPS than HDDs

## Need Help?

See `README.md` for full documentation  
See `OVERVIEW.md` for technical details

---

**Ready to benchmark?** Run `./run.sh` now! ⚡
