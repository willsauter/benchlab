"""
BenchLab - Comprehensive Animated TUI Interface
System-wide performance benchmarking: Disk, CPU, Memory, GPU/AI
"""

import time
from typing import List, Optional, Dict, Any
from rich.console import Console, Group
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich import box
from rich.align import Align
from rich.prompt import Prompt, Confirm, IntPrompt

from benchmark import DiskBenchmark, BenchmarkResult
from cpu_benchmark import CPUBenchmark, CPUBenchmarkResult
from memory_benchmark import MemoryBenchmark, MemoryBenchmarkResult
from gpu_benchmark import GPUBenchmark, GPUBenchmarkResult


class BenchLabTUI:
    """Comprehensive animated TUI for system benchmarking"""
    
    def __init__(self, file_size_mb: int = 100, block_size_kb: int = 4, test_dir: Optional[str] = None,
                 categories: List[str] = None):
        self.console = Console()
        
        # Initialize benchmarks
        self.disk_benchmark = DiskBenchmark(test_dir=test_dir, file_size_mb=file_size_mb, block_size_kb=block_size_kb)
        self.cpu_benchmark = CPUBenchmark()
        self.memory_benchmark = MemoryBenchmark()
        self.gpu_benchmark = GPUBenchmark()
        
        # Results storage
        self.disk_results: List[BenchmarkResult] = []
        self.cpu_results: List[CPUBenchmarkResult] = []
        self.memory_results: List[MemoryBenchmarkResult] = []
        self.gpu_results: List[GPUBenchmarkResult] = []
        
        # Progress tracking
        self.current_progress = 0
        self.current_test = ""
        self.current_category = ""
        self.is_running = False
        
        # Test categories to run
        self.categories = categories or ["disk", "cpu", "memory", "gpu"]
        self.gpu_available = self.gpu_benchmark.is_available()
        
        # Configuration (set by main)
        self.config = {
            'disk_size': file_size_mb,
            'disk_block': block_size_kb,
            'cpu_duration': 5,
            'cpu_multi_duration': 10,
            'mem_size': 100,
            'gpu_iterations': 100,
            'selected_tests': None
        }
        
    def create_header(self) -> Panel:
        """Create animated header"""
        header_text = Text()
        header_text.append("⚡ ", style="bold yellow")
        header_text.append("BENCH", style="bold cyan")
        header_text.append("LAB", style="bold magenta")
        header_text.append(" ⚡", style="bold yellow")
        header_text.append("\n")
        header_text.append("System Performance Benchmarking Suite", style="italic bright_white")
        
        return Panel(
            Align.center(header_text),
            box=box.DOUBLE,
            style="bold blue",
            border_style="cyan"
        )
    
    def create_config_panel(self) -> Panel:
        """Create configuration panel"""
        config_table = Table(show_header=False, box=None, padding=(0, 1))
        config_table.add_column(style="bold yellow", width=20)
        config_table.add_column(style="bright_white", width=30)
        
        # System info
        config_table.add_row("💾 Disk Test:", f"{self.disk_benchmark.file_size_mb} MB file")
        config_table.add_row("🔲 Block Size:", f"{self.disk_benchmark.block_size_kb} KB")
        config_table.add_row("🧠 CPU Cores:", f"{self.cpu_benchmark.cpu_count}")
        config_table.add_row("🎮 GPU:", "Metal (Apple Silicon)" if self.gpu_available else "Not Available")
        
        categories_enabled = ", ".join([c.upper() for c in self.categories])
        config_table.add_row("📊 Categories:", categories_enabled)
        
        return Panel(
            config_table,
            title="[bold green]Configuration[/bold green]",
            box=box.ROUNDED,
            border_style="green"
        )
    
    def create_progress_panel(self) -> Panel:
        """Create progress panel"""
        if not self.is_running:
            content = Align.center(
                Text("Ready to benchmark! 🚀", style="bold bright_green"),
                vertical="middle"
            )
        else:
            progress_bar = Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(complete_style="cyan", finished_style="green", width=40),
                TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
                expand=True
            )
            task_desc = f"{self.current_category} > {self.current_test}"
            task = progress_bar.add_task(task_desc, total=100)
            progress_bar.update(task, completed=self.current_progress)
            content = progress_bar
        
        return Panel(
            content,
            title="[bold cyan]Progress[/bold cyan]",
            box=box.ROUNDED,
            border_style="cyan",
            height=5
        )
    
    def create_results_panel(self) -> Panel:
        """Create comprehensive results panel"""
        if not any([self.disk_results, self.cpu_results, self.memory_results, self.gpu_results]):
            content = Align.center(
                Text("No results yet...", style="dim italic"),
                vertical="middle"
            )
        else:
            # Create tables for each category
            tables = []
            
            # Disk Results
            if self.disk_results and "disk" in self.categories:
                disk_table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED, title="💾 DISK I/O")
                disk_table.add_column("Test", style="cyan", no_wrap=True)
                disk_table.add_column("Duration", style="yellow", justify="right")
                disk_table.add_column("Throughput", style="green", justify="right")
                disk_table.add_column("IOPS", style="blue", justify="right")
                
                for result in self.disk_results:
                    iops_str = f"{result.iops:,}" if result.iops else "N/A"
                    disk_table.add_row(
                        f"✓ {result.test_name}",
                        f"{result.duration:.2f}s",
                        f"{result.throughput_mbps:.2f} MB/s",
                        iops_str
                    )
                tables.append(disk_table)
            
            # CPU Results
            if self.cpu_results and "cpu" in self.categories:
                cpu_table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED, title="🧠 CPU")
                cpu_table.add_column("Test", style="magenta", no_wrap=True)
                cpu_table.add_column("Duration", style="yellow", justify="right")
                cpu_table.add_column("Ops/sec", style="green", justify="right")
                cpu_table.add_column("Score", style="blue", justify="right")
                cpu_table.add_column("Temp", style="red", justify="right")
                
                for result in self.cpu_results:
                    temp_str = f"{result.temperature:.1f}°C" if result.temperature else "N/A"
                    cpu_table.add_row(
                        f"✓ {result.test_name}",
                        f"{result.duration:.2f}s",
                        f"{result.ops_per_second:.0f}",
                        f"{result.score:.2f}",
                        temp_str
                    )
                tables.append(cpu_table)
            
            # Memory Results
            if self.memory_results and "memory" in self.categories:
                mem_table = Table(show_header=True, header_style="bold yellow", box=box.ROUNDED, title="💿 MEMORY")
                mem_table.add_column("Test", style="yellow", no_wrap=True)
                mem_table.add_column("Duration", style="cyan", justify="right")
                mem_table.add_column("Bandwidth", style="green", justify="right")
                mem_table.add_column("Buffer", style="blue", justify="right")
                
                for result in self.memory_results:
                    mem_table.add_row(
                        f"✓ {result.test_name}",
                        f"{result.duration:.2f}s",
                        f"{result.bandwidth_gbps:.2f} GB/s",
                        result.buffer_size or "N/A"
                    )
                tables.append(mem_table)
            
            # GPU Results
            if self.gpu_results and "gpu" in self.categories:
                gpu_table = Table(show_header=True, header_style="bold green", box=box.ROUNDED, title="🎮 GPU/AI")
                gpu_table.add_column("Test", style="green", no_wrap=True)
                gpu_table.add_column("Duration", style="yellow", justify="right")
                gpu_table.add_column("Ops/sec", style="cyan", justify="right")
                gpu_table.add_column("Score", style="magenta", justify="right")
                
                for result in self.gpu_results:
                    gpu_table.add_row(
                        f"✓ {result.test_name}",
                        f"{result.duration:.2f}s",
                        f"{result.ops_per_second:.2f}",
                        f"{result.score:.2f}"
                    )
                tables.append(gpu_table)
            
            # Combine tables using Group for proper rendering
            from rich.console import Group as RenderGroup
            content = RenderGroup(*tables)
        
        return Panel(
            content,
            title="[bold magenta]Benchmark Results[/bold magenta]",
            box=box.ROUNDED,
            border_style="magenta"
        )
    
    def create_footer(self) -> Panel:
        """Create footer with controls"""
        footer_text = Text()
        footer_text.append("Press ", style="dim")
        footer_text.append("Ctrl+C", style="bold red")
        footer_text.append(" to stop | ", style="dim")
        footer_text.append("BenchLab v2.0", style="bold cyan italic")
        
        return Panel(
            Align.center(footer_text),
            box=box.ROUNDED,
            style="dim",
            border_style="blue"
        )
    
    def create_layout(self) -> Layout:
        """Create main layout"""
        layout = Layout()
        
        layout.split_column(
            Layout(name="header", size=5),
            Layout(name="config", size=9),
            Layout(name="progress", size=7),
            Layout(name="results", minimum_size=15),
            Layout(name="footer", size=3)
        )
        
        return layout
    
    def update_layout(self, layout: Layout):
        """Update layout with current data"""
        layout["header"].update(self.create_header())
        layout["config"].update(self.create_config_panel())
        layout["progress"].update(self.create_progress_panel())
        layout["results"].update(self.create_results_panel())
        layout["footer"].update(self.create_footer())
    
    def progress_callback(self, progress: float):
        """Callback for benchmark progress updates"""
        self.current_progress = progress
    
    def run_benchmark(self, category: str, test_name: str, test_func):
        """Run a single benchmark test"""
        self.current_category = category.upper()
        self.current_test = test_name
        self.is_running = True
        self.current_progress = 0
        
        try:
            result = test_func(progress_callback=self.progress_callback)
            
            # Store result in appropriate category
            if category == "DISK":
                self.disk_results.append(result)
            elif category == "CPU":
                self.cpu_results.append(result)
            elif category == "MEMORY":
                self.memory_results.append(result)
            elif category == "GPU":
                self.gpu_results.append(result)
                
        except Exception as e:
            self.console.print(f"[bold red]Error in {test_name}: {e}[/bold red]")
        finally:
            self.is_running = False
            self.current_progress = 0
    
    def should_run_test(self, test_id: str) -> bool:
        """Check if a specific test should run based on selected_tests"""
        if self.config['selected_tests'] is None:
            return True
        return test_id in self.config['selected_tests']
    
    def run_all_benchmarks(self):
        """Run all benchmark tests with live display"""
        layout = self.create_layout()
        
        # Get configuration
        disk_size = self.config['disk_size']
        disk_block = self.config['disk_block']
        cpu_dur = self.config['cpu_duration']
        cpu_multi_dur = self.config['cpu_multi_duration']
        mem_size = self.config['mem_size']
        gpu_iter = self.config['gpu_iterations']
        
        try:
            with Live(layout, console=self.console, refresh_per_second=10, screen=True):
                self.update_layout(layout)
                time.sleep(1)
                
                # === DISK TESTS ===
                if "disk" in self.categories:
                    if self.should_run_test("disk.seq-write"):
                        self.run_benchmark("DISK", "Sequential Write 📝", 
                                         lambda progress_callback: self.disk_benchmark.sequential_write(
                                             progress_callback=progress_callback,
                                             file_size_mb=disk_size,
                                             block_size_kb=disk_block))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("disk.seq-read"):
                        self.run_benchmark("DISK", "Sequential Read 📖", 
                                         lambda progress_callback: self.disk_benchmark.sequential_read(
                                             progress_callback=progress_callback,
                                             file_size_mb=disk_size,
                                             block_size_kb=disk_block))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("disk.rand-write"):
                        self.run_benchmark("DISK", "Random Write 🎲", 
                                         lambda progress_callback: self.disk_benchmark.random_write(
                                             progress_callback=progress_callback,
                                             file_size_mb=disk_size,
                                             block_size_kb=disk_block))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("disk.rand-read"):
                        self.run_benchmark("DISK", "Random Read 🎯", 
                                         lambda progress_callback: self.disk_benchmark.random_read(
                                             progress_callback=progress_callback,
                                             file_size_mb=disk_size,
                                             block_size_kb=disk_block))
                        self.update_layout(layout)
                        time.sleep(0.5)
                
                # === CPU TESTS ===
                if "cpu" in self.categories:
                    if self.should_run_test("cpu.single-int"):
                        self.run_benchmark("CPU", "Single-Core Int 🔢", 
                                         lambda progress_callback: self.cpu_benchmark.single_core_integer(duration=cpu_dur, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("cpu.single-float"):
                        self.run_benchmark("CPU", "Single-Core Float ➗", 
                                         lambda progress_callback: self.cpu_benchmark.single_core_floating_point(duration=cpu_dur, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("cpu.multi"):
                        self.run_benchmark("CPU", "Multi-Core Hash 🔐", 
                                         lambda progress_callback: self.cpu_benchmark.multi_core_hash(duration=cpu_multi_dur, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("cpu.compress"):
                        self.run_benchmark("CPU", "Compression 📦", 
                                         lambda progress_callback: self.cpu_benchmark.compression_test(duration=cpu_multi_dur, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("cpu.crypto"):
                        self.run_benchmark("CPU", "Cryptography 🔒", 
                                         lambda progress_callback: self.cpu_benchmark.crypto_test(duration=cpu_dur, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.5)
                
                # === MEMORY TESTS ===
                if "memory" in self.categories:
                    if self.should_run_test("mem.seq-read"):
                        self.run_benchmark("MEMORY", "Sequential Read 📖", 
                                         lambda progress_callback: self.memory_benchmark.sequential_read(size_mb=mem_size, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("mem.seq-write"):
                        self.run_benchmark("MEMORY", "Sequential Write 📝", 
                                         lambda progress_callback: self.memory_benchmark.sequential_write(size_mb=mem_size, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("mem.l1"):
                        self.run_benchmark("MEMORY", "L1 Cache ⚡", 
                                         lambda progress_callback: self.memory_benchmark.cache_test_l1(duration=5.0, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("mem.l2"):
                        self.run_benchmark("MEMORY", "L2 Cache 💨", 
                                         lambda progress_callback: self.memory_benchmark.cache_test_l2(duration=5.0, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("mem.l3"):
                        self.run_benchmark("MEMORY", "L3 Cache 🌊", 
                                         lambda progress_callback: self.memory_benchmark.cache_test_l3(duration=5.0, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("mem.copy"):
                        self.run_benchmark("MEMORY", "Memory Copy 📋", 
                                         lambda progress_callback: self.memory_benchmark.memory_copy(size_mb=mem_size, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("mem.random"):
                        self.run_benchmark("MEMORY", "Random Access 🎲", 
                                         lambda progress_callback: self.memory_benchmark.random_access(size_mb=mem_size, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.5)
                
                # === GPU TESTS ===
                if "gpu" in self.categories and self.gpu_available:
                    if self.should_run_test("gpu.matrix"):
                        self.run_benchmark("GPU", "Matrix Multiply 🔢", 
                                         lambda progress_callback: self.gpu_benchmark.matrix_multiply(size=2048, iterations=gpu_iter, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("gpu.conv"):
                        self.run_benchmark("GPU", "2D Convolution 🎨", 
                                         lambda progress_callback: self.gpu_benchmark.convolution_2d(iterations=gpu_iter, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("gpu.element"):
                        self.run_benchmark("GPU", "Element-wise Ops ➕", 
                                         lambda progress_callback: self.gpu_benchmark.element_wise_ops(iterations=gpu_iter, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("gpu.transformer"):
                        self.run_benchmark("GPU", "Transformer Attn 🤖", 
                                         lambda progress_callback: self.gpu_benchmark.transformer_attention(iterations=gpu_iter//2, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("gpu.memory"):
                        self.run_benchmark("GPU", "GPU Memory BW 💾", 
                                         lambda progress_callback: self.gpu_benchmark.memory_bandwidth(size_mb=500, iterations=20, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.3)
                    
                    if self.should_run_test("gpu.inference"):
                        self.run_benchmark("GPU", "AI Inference 🧠", 
                                         lambda progress_callback: self.gpu_benchmark.ai_inference_simulation(iterations=gpu_iter//2, progress_callback=progress_callback))
                        self.update_layout(layout)
                        time.sleep(0.5)
                
                # Show final results
                self.current_test = "✅ All tests completed!"
                self.update_layout(layout)
                time.sleep(3)
                
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Benchmark interrupted by user[/bold red]")
        finally:
            if "disk" in self.categories:
                self.disk_benchmark.cleanup()
    
    def show_welcome(self):
        """Show welcome screen"""
        welcome_text = Text()
        welcome_text.append("\n")
        welcome_text.append("    ", style="bold yellow")
        welcome_text.append("BENCHLAB", style="bold cyan")
        welcome_text.append(" ", style="bold yellow")
        welcome_text.append("\n", style="bold yellow")
        welcome_text.append("    System Performance Benchmarking Suite\n", style="italic bright_white")
        welcome_text.append("\n")
        
        panel = Panel(
            Align.center(welcome_text),
            box=box.DOUBLE,
            style="bold blue"
        )
        
        self.console.print(panel)
        time.sleep(1)
    
    def show_interactive_menu(self) -> bool:
        """Show interactive configuration menu. Returns True if user wants to continue."""
        self.console.clear()
        self.show_welcome()
        
        # Main menu
        self.console.print("\n[bold cyan]═══ Main Menu ═══[/bold cyan]\n")
        self.console.print("[1] Run all tests with default settings")
        self.console.print("[2] Customize test configuration")
        self.console.print("[3] Quick test (fast settings)")
        self.console.print("[4] Exit")
        
        choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4"], default="1")
        
        if choice == "4":
            self.console.print("\n[yellow]Exiting...[/yellow]")
            return False
        elif choice == "1":
            # Use defaults, all categories
            self.categories = ["disk", "cpu", "memory", "gpu"]
            self.config['selected_tests'] = None
            return True
        elif choice == "3":
            # Quick test settings
            self.categories = ["disk", "cpu", "memory"]
            self.config = {
                'disk_size': 50,
                'disk_block': 4,
                'cpu_duration': 3,
                'cpu_multi_duration': 5,
                'mem_size': 50,
                'gpu_iterations': 50,
                'selected_tests': None
            }
            self.console.print("\n[green] Quick test mode selected (faster settings)[/green]")
            time.sleep(1)
            return True
        else:
            # Customize
            return self._customize_configuration()
    
    def _customize_configuration(self) -> bool:
        """Interactive configuration customization"""
        self.console.clear()
        self.console.print("\n[bold cyan]═══ Customize Configuration ═══[/bold cyan]\n")
        
        # Step 1: Select categories
        self.console.print("[bold yellow]Step 1: Select Test Categories[/bold yellow]\n")
        self.console.print("Available categories:")
        self.console.print("  [1] Disk I/O (4 tests)")
        self.console.print("  [2] CPU (5 tests)")
        self.console.print("  [3] Memory (7 tests)")
        gpu_text = "  [4] GPU/AI (6 tests)"
        if not self.gpu_available:
            gpu_text += " [dim](not available)[/dim]"
        self.console.print(gpu_text)
        self.console.print("  [5] All categories")
        
        cat_choice = Prompt.ask("\nSelect categories (comma-separated numbers)", default="5")
        
        # Parse category selection
        cat_map = {"1": "disk", "2": "cpu", "3": "memory", "4": "gpu"}
        if cat_choice.strip() == "5":
            self.categories = ["disk", "cpu", "memory", "gpu"]
        else:
            selected = [cat_map[c.strip()] for c in cat_choice.split(",") if c.strip() in cat_map]
            self.categories = selected if selected else ["disk", "cpu", "memory", "gpu"]
        
        # Step 2: Specific tests or all in category?
        self.console.print("\n[bold yellow]Step 2: Test Selection[/bold yellow]\n")
        run_all_in_cat = Confirm.ask("Run all tests in selected categories?", default=True)
        
        if not run_all_in_cat:
            self.config['selected_tests'] = self._select_specific_tests()
        else:
            self.config['selected_tests'] = None
        
        # Step 3: Configure parameters
        self.console.print("\n[bold yellow]Step 3: Configure Parameters[/bold yellow]\n")
        configure_params = Confirm.ask("Customize test parameters?", default=False)
        
        if configure_params:
            self._configure_parameters()
        
        # Summary
        self.console.print("\n[bold green]═══ Configuration Summary ═══[/bold green]\n")
        self.console.print(f"Categories: [cyan]{', '.join(self.categories).upper()}[/cyan]")
        if self.config.get('selected_tests'):
            self.console.print(f"Tests: [cyan]{len(self.config['selected_tests'])} selected[/cyan]")
        else:
            self.console.print("Tests: [cyan]All in selected categories[/cyan]")
        self.console.print(f"Disk: [cyan]{self.config['disk_size']} MB, {self.config['disk_block']} KB blocks[/cyan]")
        self.console.print(f"CPU: [cyan]{self.config['cpu_duration']}s single, {self.config['cpu_multi_duration']}s multi[/cyan]")
        self.console.print(f"Memory: [cyan]{self.config['mem_size']} MB buffer[/cyan]")
        self.console.print(f"GPU: [cyan]{self.config['gpu_iterations']} iterations[/cyan]")
        
        self.console.print("")
        proceed = Confirm.ask("Start benchmark with these settings?", default=True)
        
        if not proceed:
            retry = Confirm.ask("Return to main menu?", default=True)
            if retry:
                return self.show_interactive_menu()
            return False
        
        return True
    
    def _select_specific_tests(self) -> List[str]:
        """Allow user to select specific tests"""
        selected = []
        
        test_catalog = {
            "disk": [
                ("disk.seq-write", "Sequential write"),
                ("disk.seq-read", "Sequential read"),
                ("disk.rand-write", "Random write"),
                ("disk.rand-read", "Random read"),
            ],
            "cpu": [
                ("cpu.single-int", "Single-core integer"),
                ("cpu.single-float", "Single-core float"),
                ("cpu.multi", "Multi-core hash"),
                ("cpu.compress", "Compression"),
                ("cpu.crypto", "Cryptography"),
            ],
            "memory": [
                ("mem.seq-read", "Sequential read"),
                ("mem.seq-write", "Sequential write"),
                ("mem.l1", "L1 cache"),
                ("mem.l2", "L2 cache"),
                ("mem.l3", "L3 cache"),
                ("mem.copy", "Memory copy"),
                ("mem.random", "Random access"),
            ],
            "gpu": [
                ("gpu.matrix", "Matrix multiply"),
                ("gpu.conv", "2D convolution"),
                ("gpu.element", "Element-wise ops"),
                ("gpu.transformer", "Transformer attention"),
                ("gpu.memory", "GPU memory bandwidth"),
                ("gpu.inference", "AI inference"),
            ]
        }
        
        for category in self.categories:
            if category == "gpu" and not self.gpu_available:
                continue
            
            self.console.print(f"\n[bold cyan]{category.upper()} Tests:[/bold cyan]")
            tests = test_catalog.get(category, [])
            for idx, (test_id, desc) in enumerate(tests, 1):
                self.console.print(f"  [{idx}] {desc}")
            
            choices = Prompt.ask(
                f"Select {category} tests (comma-separated numbers, or 'all')",
                default="all"
            )
            
            if choices.strip().lower() == "all":
                selected.extend([test_id for test_id, _ in tests])
            else:
                try:
                    indices = [int(c.strip()) - 1 for c in choices.split(",") if c.strip()]
                    selected.extend([tests[i][0] for i in indices if 0 <= i < len(tests)])
                except (ValueError, IndexError):
                    # Invalid input, select all
                    selected.extend([test_id for test_id, _ in tests])
        
        return selected if selected else None
    
    def _configure_parameters(self):
        """Configure test parameters interactively"""
        if "disk" in self.categories:
            self.console.print("\n[bold] Disk Configuration[/bold]")
            self.config['disk_size'] = IntPrompt.ask(
                "  File size (MB)",
                default=self.config['disk_size']
            )
            self.config['disk_block'] = IntPrompt.ask(
                "  Block size (KB)",
                default=self.config['disk_block']
            )
        
        if "cpu" in self.categories:
            self.console.print("\n[bold] CPU Configuration[/bold]")
            self.config['cpu_duration'] = IntPrompt.ask(
                "  Single-core test duration (seconds)",
                default=self.config['cpu_duration']
            )
            self.config['cpu_multi_duration'] = IntPrompt.ask(
                "  Multi-core test duration (seconds)",
                default=self.config['cpu_multi_duration']
            )
        
        if "memory" in self.categories:
            self.console.print("\n[bold] Memory Configuration[/bold]")
            self.config['mem_size'] = IntPrompt.ask(
                "  Buffer size (MB)",
                default=self.config['mem_size']
            )
        
        if "gpu" in self.categories and self.gpu_available:
            self.console.print("\n[bold] GPU Configuration[/bold]")
            self.config['gpu_iterations'] = IntPrompt.ask(
                "  Iteration count",
                default=self.config['gpu_iterations']
            )
    
    def show_summary(self):
        """Show final summary"""
        self.console.print("\n")
        
        summary_panel = Panel(
            self.create_results_panel(),
            title="[bold green]✅ Benchmark Complete![/bold green]",
            box=box.DOUBLE,
            border_style="green"
        )
        
        self.console.print(summary_panel)
        
        # Calculate category summaries
        if self.disk_results:
            avg_throughput = sum(r.throughput_mbps for r in self.disk_results) / len(self.disk_results)
            self.console.print(f"\n[bold cyan]💾 Disk Average:[/bold cyan] [bold yellow]{avg_throughput:.2f} MB/s[/bold yellow]")
        
        if self.cpu_results:
            avg_score = sum(r.score for r in self.cpu_results) / len(self.cpu_results)
            avg_temp = sum(r.temperature for r in self.cpu_results if r.temperature) / sum(1 for r in self.cpu_results if r.temperature) if any(r.temperature for r in self.cpu_results) else None
            self.console.print(f"[bold magenta]🧠 CPU Average Score:[/bold magenta] [bold yellow]{avg_score:.2f}[/bold yellow]", end="")
            if avg_temp:
                self.console.print(f" [bold red](Temp: {avg_temp:.1f}°C)[/bold red]")
            else:
                self.console.print()
        
        if self.memory_results:
            avg_bandwidth = sum(r.bandwidth_gbps for r in self.memory_results) / len(self.memory_results)
            self.console.print(f"[bold yellow]💿 Memory Average:[/bold yellow] [bold yellow]{avg_bandwidth:.2f} GB/s[/bold yellow]")
        
        if self.gpu_results:
            avg_score = sum(r.score for r in self.gpu_results) / len(self.gpu_results)
            self.console.print(f"[bold green]🎮 GPU Average Score:[/bold green] [bold yellow]{avg_score:.2f}[/bold yellow]")


def main():
    """Main entry point for TUI application"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="BenchLab - System Performance Benchmark Suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./run.sh                                    # Run all tests
  ./run.sh --categories disk                  # Disk tests only
  ./run.sh --categories cpu,memory            # CPU and memory tests
  ./run.sh --size 500 --block 8               # Custom disk settings
  ./run.sh --list-tests                       # List all available tests
  ./run.sh --tests disk.seq-read,cpu.multi    # Run specific tests

Test Categories:
  disk    - Disk I/O (sequential/random read/write, 4 tests)
  cpu     - CPU performance (integer/float/multi-core/compression/crypto, 5 tests)
  memory  - Memory bandwidth (sequential/cache/random/copy, 6 tests)
  gpu     - GPU/AI performance (matrix/conv/transformer/inference, 6 tests)
        """
    )
    
    # Category selection
    parser.add_argument("--categories", type=str, default="all", 
                       help="Categories to test: all, disk, cpu, memory, gpu (comma-separated)")
    
    # Individual test selection
    parser.add_argument("--tests", type=str, default=None,
                       help="Specific tests to run (e.g., disk.seq-write,cpu.single-int)")
    
    parser.add_argument("--list-tests", action="store_true",
                       help="List all available tests and exit")
    
    # Disk configuration
    parser.add_argument("--size", type=int, default=100, 
                       help="Disk test file size in MB (default: 100)")
    parser.add_argument("--block", type=int, default=4, 
                       help="Disk block size in KB (default: 4)")
    parser.add_argument("--dir", type=str, default=None, 
                       help="Disk test directory (default: system temp)")
    
    # CPU configuration
    parser.add_argument("--cpu-duration", type=int, default=5,
                       help="CPU single-core test duration in seconds (default: 5)")
    parser.add_argument("--cpu-multi-duration", type=int, default=10,
                       help="CPU multi-core test duration in seconds (default: 10)")
    
    # Memory configuration  
    parser.add_argument("--mem-size", type=int, default=100,
                       help="Memory test buffer size in MB (default: 100)")
    
    # GPU configuration
    parser.add_argument("--gpu-iterations", type=int, default=100,
                       help="GPU test iterations (default: 100)")
    
    # Interactive mode control
    parser.add_argument("--no-interactive", action="store_true",
                       help="Skip interactive menu even if no other args provided")
    
    args = parser.parse_args()
    
    # Detect if we should use interactive mode
    # Interactive if: no args except program name, or only --categories/--tests not specified
    import sys
    use_interactive = (
        len(sys.argv) == 1 or  # No arguments at all
        (not args.no_interactive and 
         args.categories == "all" and 
         args.tests is None and
         not args.list_tests and
         args.size == 100 and
         args.block == 4 and
         args.cpu_duration == 5 and
         args.cpu_multi_duration == 10 and
         args.mem_size == 100 and
         args.gpu_iterations == 100)
    )
    
    # List tests if requested
    if args.list_tests:
        console = Console()
        console.print("\n[bold cyan]Available Tests:[/bold cyan]\n")
        
        console.print("[bold magenta]💾 Disk I/O:[/bold magenta]")
        console.print("  disk.seq-write    - Sequential write")
        console.print("  disk.seq-read     - Sequential read")
        console.print("  disk.rand-write   - Random write with IOPS")
        console.print("  disk.rand-read    - Random read with IOPS")
        
        console.print("\n[bold magenta]🧠 CPU:[/bold magenta]")
        console.print("  cpu.single-int    - Single-core integer")
        console.print("  cpu.single-float  - Single-core floating point")
        console.print("  cpu.multi         - Multi-core hash")
        console.print("  cpu.compress      - Compression test")
        console.print("  cpu.crypto        - Cryptography test")
        
        console.print("\n[bold magenta]💿 Memory:[/bold magenta]")
        console.print("  mem.seq-read      - Sequential read")
        console.print("  mem.seq-write     - Sequential write")
        console.print("  mem.l1            - L1 cache test")
        console.print("  mem.l2            - L2 cache test")
        console.print("  mem.l3            - L3 cache test")
        console.print("  mem.copy          - Memory copy")
        console.print("  mem.random        - Random access")
        
        console.print("\n[bold magenta]🎮 GPU/AI:[/bold magenta]")
        console.print("  gpu.matrix        - Matrix multiply")
        console.print("  gpu.conv          - 2D convolution")
        console.print("  gpu.element       - Element-wise ops")
        console.print("  gpu.transformer   - Transformer attention")
        console.print("  gpu.memory        - GPU memory bandwidth")
        console.print("  gpu.inference     - AI inference")
        
        console.print("\n[bold yellow]Examples:[/bold yellow]")
        console.print("  --tests disk.seq-read,disk.seq-write")
        console.print("  --tests cpu.single-int,cpu.multi")
        console.print("  --categories disk,cpu")
        console.print()
        return
    
    # === INTERACTIVE MODE ===
    if use_interactive:
        # Create TUI with defaults for interactive configuration
        tui = BenchLabTUI(
            file_size_mb=args.size,
            block_size_kb=args.block,
            test_dir=args.dir,
            categories=["disk", "cpu", "memory", "gpu"]
        )
        
        # Show interactive menu and get configuration
        if not tui.show_interactive_menu():
            # User chose to exit
            return
        
        # Run benchmarks with configured settings
        tui.run_all_benchmarks()
        tui.show_summary()
        return
    
    # === CLI MODE ===
    # Parse categories or specific tests
    if args.tests:
        # Individual test selection
        selected_tests = [t.strip().lower() for t in args.tests.split(",")]
        # Determine categories from tests
        categories = []
        if any(t.startswith("disk.") for t in selected_tests):
            categories.append("disk")
        if any(t.startswith("cpu.") for t in selected_tests):
            categories.append("cpu")
        if any(t.startswith("mem.") for t in selected_tests):
            categories.append("memory")
        if any(t.startswith("gpu.") for t in selected_tests):
            categories.append("gpu")
    else:
        # Category selection
        if args.categories.lower() == "all":
            categories = ["disk", "cpu", "memory", "gpu"]
        else:
            categories = [c.strip().lower() for c in args.categories.split(",")]
        selected_tests = None
    
    # Create TUI with configuration
    tui = BenchLabTUI(
        file_size_mb=args.size,
        block_size_kb=args.block,
        test_dir=args.dir,
        categories=categories
    )
    
    # Store test configuration in TUI
    tui.config = {
        'disk_size': args.size,
        'disk_block': args.block,
        'cpu_duration': args.cpu_duration,
        'cpu_multi_duration': args.cpu_multi_duration,
        'mem_size': args.mem_size,
        'gpu_iterations': args.gpu_iterations,
        'selected_tests': selected_tests
    }
    
    # Non-interactive CLI mode - run directly
    tui.run_all_benchmarks()
    tui.show_summary()


if __name__ == "__main__":
    main()
