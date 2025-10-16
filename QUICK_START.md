# 🚀 Quick Start Guide

## Run BenchLab

```bash
./run.sh
```

## Menu Options

### Fast Tests
- **[1] Quick** - 2-3 minutes, fast validation
- **[2] Standard** - 8-12 minutes, balanced (default)

### Deep Tests  
- **[3] Thorough** - 20-30 minutes, comprehensive
- **[4] Stress** - 45-60 minutes, maximum load

### Custom
- **[5] Custom** - Build your own configuration
- **[6] Load Saved** - Use previously saved settings

### Workload Profiles
- **[7] Database** - Random I/O testing (15-20 min)
- **[8] Video** - Sequential I/O testing (10-15 min)

## CLI Mode (Skip Menu)

```bash
# Specific categories
./run.sh --categories disk
./run.sh --categories cpu,memory

# Custom settings
./run.sh --size 500 --cpu-duration 10

# Specific tests
./run.sh --tests disk.seq-read,cpu.multi

# Quick override
./run.sh --categories all
```

## Save Your Config

1. Choose option [5] Custom Configuration
2. Configure your settings
3. Answer "yes" to save
4. Name your config
5. Load it later with option [6]

## Presets Summary

| Mode | Best For |
|------|----------|
| Quick | Smoke tests, quick checks |
| Standard | Regular benchmarks |
| Thorough | Before/after comparisons |
| Stress | Stability, thermal testing |
| Database | Database server simulation |
| Video | Video editing simulation |

## Files

- Configs saved to: `~/.benchlab/config.json`
- Accuracy info: `TEST_ACCURACY.md`
- Full docs: `INTERACTIVE_MODE.md`, `NEW_FEATURES.md`
