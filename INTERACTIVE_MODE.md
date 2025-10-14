# 🎛️ Interactive Menu System Guide

## Overview

BenchLab v2.0 now features a comprehensive interactive menu system that appears automatically when you run the program without command-line arguments. This makes it easy to configure and customize your benchmark tests without memorizing CLI options.

---

## When Interactive Mode Activates

### Automatic Activation
Interactive mode **automatically starts** when you run:
```bash
./run.sh
# or
python benchlab.py
```

### Manual Override
**Skip interactive mode** by providing any configuration argument:
```bash
./run.sh --categories disk        # CLI mode
./run.sh --size 500                # CLI mode
./run.sh --no-interactive          # Force CLI mode with defaults
```

---

## Main Menu

When you start BenchLab without arguments, you'll see:

```
╔════════════════════════════════════╗
║      ⚡ BENCHLAB ⚡                ║
║  System Performance Benchmark Suite ║
╚════════════════════════════════════╝

═══ Main Menu ═══

[1] Run all tests with default settings
[2] Customize test configuration
[3] Quick test (fast settings)
[4] Exit

Select option [1/2/3/4] (1):
```

### Menu Options

#### [1] Run All Tests (Default)
- **What it does**: Runs all tests in all categories with default settings
- **Categories**: Disk, CPU, Memory, GPU
- **Duration**: ~8-12 minutes
- **Settings**:
  - Disk: 100 MB file, 4 KB blocks
  - CPU: 5s single-core, 10s multi-core
  - Memory: 100 MB buffer
  - GPU: 100 iterations

**When to use**: Standard comprehensive system benchmark

#### [2] Customize Configuration
- **What it does**: Opens the configuration wizard
- **Features**: 
  - Select specific categories
  - Choose individual tests
  - Configure all parameters
  - Review summary before starting
- **Control**: Full customization of everything

**When to use**: When you need specific tests or custom settings

#### [3] Quick Test
- **What it does**: Runs a fast benchmark with reduced settings
- **Categories**: Disk, CPU, Memory (skips GPU)
- **Duration**: ~2-3 minutes
- **Settings**:
  - Disk: 50 MB file, 4 KB blocks
  - CPU: 3s single-core, 5s multi-core
  - Memory: 50 MB buffer

**When to use**: Quick system check or validation

#### [4] Exit
- **What it does**: Exits the program without running any tests

---

## Customization Wizard (Option 2)

### Step 1: Select Test Categories

```
═══ Customize Configuration ═══

Step 1: Select Test Categories

Available categories:
  [1] 💾 Disk I/O (4 tests)
  [2] 🧠 CPU (5 tests)
  [3] 💿 Memory (7 tests)
  [4] 🎮 GPU/AI (6 tests)
  [5] All categories

Select categories (comma-separated numbers) [5]:
```

**Options**:
- **Single category**: Type `1`, `2`, `3`, or `4`
- **Multiple categories**: Type `1,2,3` or `1,4`
- **All categories**: Type `5` or press Enter
- **Note**: GPU shown as unavailable if no compatible GPU

**Examples**:
```
5          → All categories
1          → Disk only
2,3        → CPU and Memory
1,2,4      → Disk, CPU, and GPU
```

### Step 2: Test Selection

```
Step 2: Test Selection

Run all tests in selected categories? [Y/n]:
```

#### Option A: Run All Tests in Categories (Default)
- Press Enter or type `y`
- Runs every test in the selected categories
- Simple and comprehensive

#### Option B: Select Specific Tests
- Type `n`
- Opens test selection menu for each category
- Choose exactly which tests to run

**Example - Selecting Specific Tests**:
```
DISK Tests:
  [1] Sequential write
  [2] Sequential read
  [3] Random write
  [4] Random read

Select disk tests (comma-separated numbers, or 'all') [all]: 1,2

CPU Tests:
  [1] Single-core integer
  [2] Single-core float
  [3] Multi-core hash
  [4] Compression
  [5] Cryptography

Select cpu tests (comma-separated numbers, or 'all') [all]: 1,3
```

**Selection Options**:
- `all` or press Enter → All tests in category
- `1,2` → Tests 1 and 2 only
- `1,3,5` → Tests 1, 3, and 5

### Step 3: Configure Parameters

```
Step 3: Configure Parameters

Customize test parameters? [y/N]:
```

#### Option A: Use Default Parameters
- Press Enter or type `n`
- Uses standard settings (recommended)

#### Option B: Customize Parameters
- Type `y`
- Configure settings for each selected category

**Example Configuration**:
```
💾 Disk Configuration
  File size (MB) [100]: 500
  Block size (KB) [4]: 16

🧠 CPU Configuration
  Single-core test duration (seconds) [5]: 10
  Multi-core test duration (seconds) [10]: 20

💿 Memory Configuration
  Buffer size (MB) [100]: 200

🎮 GPU Configuration
  Iteration count [100]: 150
```

**Tips**:
- Press Enter to keep default shown in brackets
- Type new value to override
- All values are validated

### Configuration Summary

After configuration, you'll see a summary:

```
═══ Configuration Summary ═══

Categories: DISK, CPU
Tests: All in selected categories
Disk: 500 MB, 16 KB blocks
CPU: 10s single, 20s multi
Memory: 200 MB buffer
GPU: 150 iterations

Start benchmark with these settings? [Y/n]:
```

**Options**:
- `y` or Enter → Start benchmark
- `n` → Return to main menu or exit

---

## Usage Scenarios

### Scenario 1: First-Time User
```
1. Run: ./run.sh
2. See main menu
3. Press Enter (option 1)
4. Complete benchmark runs
```

**Result**: Full system benchmark with defaults

### Scenario 2: Quick System Check
```
1. Run: ./run.sh
2. See main menu
3. Type: 3
4. Quick test runs (~2 minutes)
```

**Result**: Fast validation of system performance

### Scenario 3: Custom Disk Test
```
1. Run: ./run.sh
2. Type: 2 (Customize)
3. Categories: 1 (Disk only)
4. All tests: y
5. Customize params: y
6. File size: 1000
7. Block size: 128
8. Confirm: y
```

**Result**: Large file sequential disk test

### Scenario 4: CPU Stress Test
```
1. Run: ./run.sh
2. Type: 2 (Customize)
3. Categories: 2 (CPU only)
4. All tests: n
5. Select: 3,4,5 (Multi-core tests)
6. Customize params: y
7. Multi-core duration: 30
8. Confirm: y
```

**Result**: Extended CPU stress test

### Scenario 5: Memory Hierarchy Analysis
```
1. Run: ./run.sh
2. Type: 2 (Customize)
3. Categories: 3 (Memory only)
4. All tests: n
5. Select: 3,4,5 (Cache tests)
6. Customize params: n
7. Confirm: y
```

**Result**: L1, L2, L3 cache benchmark

### Scenario 6: AI/ML Performance
```
1. Run: ./run.sh
2. Type: 2 (Customize)
3. Categories: 4 (GPU only)
4. All tests: n
5. Select: 1,4,6 (Matrix, Transformer, Inference)
6. Customize params: y
7. Iterations: 200
8. Confirm: y
```

**Result**: AI workload simulation

---

## Navigation Tips

### Quick Actions
- **Just press Enter**: Accept defaults and continue
- **Type number + Enter**: Select that option
- **Type 'n' + Enter**: Decline or go back
- **Ctrl+C**: Exit immediately (emergency stop)

### Smart Defaults
- All prompts show recommended defaults in `[brackets]`
- Pressing Enter always selects the safe/common choice
- You can customize only what you need

### Recovery Options
- If you make a mistake during configuration, you can:
  - Say 'no' at the final confirmation
  - Choose to return to main menu
  - Exit and restart

---

## Switching Between Modes

### Force Interactive Mode
```bash
# Even with arguments, use interactive menu (not currently supported)
# Just run without arguments:
./run.sh
```

### Force CLI Mode
```bash
# Skip interactive menu with any argument
./run.sh --categories all
./run.sh --no-interactive
./run.sh --size 100
```

### Quick CLI Examples (Skip Menu)
```bash
# Disk test
./run.sh --categories disk --size 500

# CPU test
./run.sh --categories cpu --cpu-duration 10

# Specific tests
./run.sh --tests disk.seq-read,cpu.multi

# All with custom settings
./run.sh --size 200 --cpu-duration 5
```

---

## Interactive vs CLI Comparison

| Feature | Interactive Mode | CLI Mode |
|---------|-----------------|----------|
| **Activation** | No arguments | Any argument |
| **Configuration** | Step-by-step wizard | Command-line flags |
| **Test Selection** | Visual menu | `--tests` flag |
| **Category Selection** | Numbered choices | `--categories` flag |
| **Parameters** | Interactive prompts | `--size`, `--cpu-duration`, etc. |
| **Preview** | Configuration summary | None (direct execution) |
| **Best For** | First-time users, exploration | Scripts, automation, repeated tests |
| **Speed** | Slower (interactive) | Faster (direct) |
| **Flexibility** | Very high | Very high |

---

## Configuration Presets

### Default Preset (Option 1)
```yaml
Categories: All (Disk, CPU, Memory, GPU)
Tests: All tests in each category
Disk: 100 MB, 4 KB blocks
CPU: 5s single, 10s multi
Memory: 100 MB buffer
GPU: 100 iterations
Duration: ~8-12 minutes
```

### Quick Preset (Option 3)
```yaml
Categories: Disk, CPU, Memory
Tests: All tests in each category
Disk: 50 MB, 4 KB blocks
CPU: 3s single, 5s multi
Memory: 50 MB buffer
GPU: Skipped
Duration: ~2-3 minutes
```

### Custom Preset (Option 2)
```yaml
Categories: Your choice
Tests: Your choice
Disk: Your settings
CPU: Your settings
Memory: Your settings
GPU: Your settings
Duration: Varies
```

---

## Common Interactive Workflows

### Workflow 1: Compare Before/After Upgrade
**Before upgrade:**
```
1. Run: ./run.sh
2. Option: 1 (All tests)
3. Save results to file (Ctrl+C after, then rerun with > before_upgrade.txt)
```

**After upgrade:**
```
1. Run: ./run.sh
2. Option: 1 (Same settings)
3. Save results (> after_upgrade.txt)
4. Compare files
```

### Workflow 2: Troubleshoot Slow Performance
```
1. Run: ./run.sh
2. Option: 2 (Customize)
3. Select all categories
4. Run all tests
5. Identify which category is slow
6. Run again with only that category
7. Customize settings for deeper investigation
```

### Workflow 3: Workload-Specific Testing
**For video editing:**
```
1. Run: ./run.sh
2. Option: 2
3. Categories: 1 (Disk)
4. Tests: 1,2 (Sequential only)
5. Customize: y
6. File size: 1000 MB
7. Block size: 128 KB
```

**For database:**
```
1. Run: ./run.sh
2. Option: 2
3. Categories: 1,3 (Disk and Memory)
4. Disk tests: 3,4 (Random only)
5. Memory tests: all
6. Disk: 500 MB, 4 KB blocks
```

---

## Tips for Best Results

### 1. Start Simple
- Use Option 1 (default) first
- Get baseline results
- Then customize for specific needs

### 2. Use Quick Test for Validation
- Option 3 is great for:
  - Before/after quick comparisons
  - System health checks
  - Rapid iterations

### 3. Customize Strategically
- Only configure what you need
- Keep other parameters at defaults
- Easier to compare results later

### 4. Document Your Choices
- Note which options you selected
- Save configuration summary
- Reproduce tests easily

### 5. Close Background Apps
- Before selecting any option
- Especially for CPU and memory tests
- More accurate results

---

## Troubleshooting

### Menu Not Appearing
**Problem**: Command runs directly without menu

**Solution**: 
```bash
# Make sure you're not passing any arguments
./run.sh
# Not: ./run.sh --anything
```

### Can't Type in Menu
**Problem**: Input not being captured

**Solution**:
```bash
# Make sure you're running in a proper terminal
# Not redirecting input
# Try running Python directly:
python benchlab.py
```

### Want to Skip Menu Every Time
**Solution**:
```bash
# Add to alias or script:
alias benchlab='./run.sh --no-interactive'
# Or just use CLI flags always
```

### Menu Too Slow
**Problem**: Interactive mode takes too long

**Solution**:
```bash
# Use CLI mode instead:
./run.sh --categories all
# Or use Quick Test (Option 3)
```

---

## Advanced Usage

### Scripting Around Interactive Mode
```bash
#!/bin/bash
# Automated test with menu choices

# Option 1: Run all defaults
echo "1" | ./run.sh > results.txt

# Option 3: Quick test
echo "3" | ./run.sh > quick_results.txt
```

### Combine with Other Tools
```bash
# Run interactive, then process results
./run.sh | tee results.txt | grep "Average"

# Or use CLI mode for better control
./run.sh --categories disk --size 500 | tee disk_results.txt
```

---

## Summary

✅ **Automatic Activation**: Just run `./run.sh`  
✅ **Three Quick Options**: All tests, Customize, or Quick test  
✅ **Step-by-Step Configuration**: Easy-to-follow wizard  
✅ **Smart Defaults**: Press Enter for recommended settings  
✅ **Full Control**: Configure every parameter  
✅ **Preview Summary**: Review before running  
✅ **CLI Override**: Use flags to skip menu  

**Interactive mode makes BenchLab accessible to everyone, from first-time users to advanced testers!**
