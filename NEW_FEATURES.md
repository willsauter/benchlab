# 🎉 New Features v2.0

## 🎛️ Colorful Interactive Menu

**New Control Center** with 9 options:
- ⚡ Quick Test (2-3 min)
- 📊 Standard Test (8-12 min) - Default
- 🔍 Thorough Test (20-30 min)
- 🔥 Stress Test (45-60 min)
- 🎨 Custom Configuration
- 💾 Load Saved Config
- 🗄️ Database Profile (15-20 min)
- 🎬 Video Profile (10-15 min)
- ❌ Exit

## ⏱️ Test Duration Presets

**6 Built-in Presets:**

| Preset | Disk | CPU Single/Multi | Memory | GPU | Duration |
|--------|------|------------------|--------|-----|----------|
| **Quick** | 50 MB | 3s / 5s | 50 MB | 50 | 2-3 min |
| **Standard** | 100 MB | 5s / 10s | 100 MB | 100 | 8-12 min |
| **Thorough** | 500 MB | 15s / 30s | 200 MB | 200 | 20-30 min |
| **Stress** | 1000 MB | 30s / 60s | 500 MB | 500 | 45-60 min |
| **Database** | 500 MB | 10s / 20s | 200 MB | 100 | 15-20 min |
| **Video** | 1000 MB | 10s / 20s | 500 MB | 200 | 10-15 min |

## 💾 Save/Load Configurations

**Save custom configs:**
- Create custom configuration in wizard
- Option to save before running
- Stored in `~/.benchlab/config.json`
- Reusable across sessions

**Load saved configs:**
- Option [6] in main menu
- Shows list of saved configurations
- One-click to apply saved settings

## 🔥 Stress Test Profiles

**Stress Test Mode:**
- 1000 MB disk files
- 30s single-core, 60s multi-core CPU tests
- 500 MB memory buffers
- 500 GPU iterations
- Tests thermal throttling and sustained performance
- Warning prompt before starting

**Workload Profiles:**
- **Database**: Random I/O (disk) + All memory tests (15-20 min)
  - 2 disk tests (random read/write, 4KB blocks)
  - 7 memory tests (sequential, cache, random, copy)
- **Video**: Sequential I/O (disk) + Multi-core CPU + GPU compute (10-15 min)
  - 2 disk tests (sequential read/write, 128KB blocks)
  - 2 CPU tests (multi-core hash, compression)
  - 3 GPU tests (matrix multiply, convolution, memory bandwidth)

## 🎨 Enhanced Custom Wizard

**New Step 0:** Choose starting preset
- Table view of all presets
- Start from any preset, then customize
- Makes configuration faster

**Save Option:** Before running tests
- Prompt to save configuration
- Named configurations for reuse
- Easy workflow for repeated tests

## 📊 Test Accuracy Documentation

See `TEST_ACCURACY.md` for:
- Accuracy percentages per test type
- Methodology explanations
- Variance information
- Best practices for accurate results
- Comparison to other tools

## Quick Start

```bash
# Interactive menu
./run.sh

# Quick test
./run.sh  # Select option 1

# Stress test
./run.sh  # Select option 4

# Custom with save
./run.sh  # Select option 5, configure, save

# Load saved
./run.sh  # Select option 6, choose config
```

## Configuration File Location

`~/.benchlab/config.json`

Example structure:
```json
{
  "my_config": {
    "config": {
      "disk_size": 500,
      "cpu_duration": 10,
      ...
    },
    "categories": ["disk", "cpu"]
  }
}
```

## What Changed

**Before:** 4 menu options (All/Customize/Quick/Exit)  
**After:** 9 menu options with presets, profiles, and save/load

**Before:** Manual parameter entry only  
**After:** Preset-based + manual customization

**Before:** No config persistence  
**After:** Save/load configurations

**Before:** One "quick" mode  
**After:** 6 different preset profiles
