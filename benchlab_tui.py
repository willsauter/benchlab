"""
BenchLab - Animated TUI Interface for Disk Benchmarking
Using Rich library for colorful and vibrant animated graphics
"""

import time
import threading
from typing import List, Optional
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich import box
from rich.align import Align
import sys

from benchmark import DiskBenchmark, BenchmarkResult


class BenchLabTUI:
    """Animated TUI for disk benchmarking"""
    
    def __init__(self, file_size_mb: int = 100, block_size_kb: int = 4, test_dir: Optional[str] = None):
        self.console = Console()
        self.benchmark = DiskBenchmark(test_dir=test_dir, file_size_mb=file_size_mb, block_size_kb=block_size_kb)
        self.results: List[BenchmarkResult] = []
        self.current_progress = 0
        self.current_test = ""
        self.is_running = False
        
    def create_header(self) -> Panel:
        """Create animated header"""
        header_text = Text()
        header_text.append("⚡ ", style="bold yellow")
        header_text.append("BENCH", style="bold cyan")
        header_text.append("LAB", style="bold magenta")
        header_text.append(" ⚡", style="bold yellow")
        header_text.append("\n")
        header_text.append("Disk Performance Benchmarking Tool", style="italic bright_white")
        
        return Panel(
            Align.center(header_text),
            box=box.DOUBLE,
            style="bold blue",
            border_style="cyan"
        )
    
    def create_config_panel(self) -> Panel:
        """Create configuration panel"""
        config_table = Table(show_header=False, box=None, padding=(0, 2))
        config_table.add_column(style="bold yellow")
        config_table.add_column(style="bright_white")
        
        config_table.add_row("📁 Test Directory:", self.benchmark.test_dir)
        config_table.add_row("📊 File Size:", f"{self.benchmark.file_size_mb} MB")
        config_table.add_row("🔲 Block Size:", f"{self.benchmark.block_size_kb} KB")
        
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
                BarColumn(complete_style="cyan", finished_style="green"),
                TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
                expand=True
            )
            task = progress_bar.add_task(self.current_test, total=100)
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
        """Create results panel with fancy table"""
        if not self.results:
            content = Align.center(
                Text("No results yet...", style="dim italic"),
                vertical="middle"
            )
        else:
            results_table = Table(
                show_header=True,
                header_style="bold magenta",
                box=box.HEAVY,
                border_style="magenta"
            )
            
            results_table.add_column("Test", style="cyan", no_wrap=True)
            results_table.add_column("Duration", style="yellow", justify="right")
            results_table.add_column("Throughput", style="green", justify="right")
            results_table.add_column("IOPS", style="blue", justify="right")
            
            for result in self.results:
                iops_str = f"{result.iops:,}" if result.iops else "N/A"
                results_table.add_row(
                    f"✓ {result.test_name}",
                    f"{result.duration:.2f}s",
                    f"{result.throughput_mbps:.2f} MB/s",
                    iops_str
                )
            
            content = results_table
        
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
        footer_text.append("BenchLab v1.0", style="bold cyan italic")
        
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
            Layout(name="config", size=7),
            Layout(name="progress", size=7),
            Layout(name="results", minimum_size=10),
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
    
    def run_benchmark(self, test_name: str, test_func):
        """Run a single benchmark test"""
        self.current_test = test_name
        self.is_running = True
        self.current_progress = 0
        
        try:
            result = test_func(progress_callback=self.progress_callback)
            self.results.append(result)
        except Exception as e:
            self.console.print(f"[bold red]Error in {test_name}: {e}[/bold red]")
        finally:
            self.is_running = False
            self.current_progress = 0
    
    def run_all_benchmarks(self):
        """Run all benchmark tests with live display"""
        layout = self.create_layout()
        
        try:
            with Live(layout, console=self.console, refresh_per_second=10, screen=True):
                self.update_layout(layout)
                time.sleep(1)
                
                # Sequential Write
                self.run_benchmark("Sequential Write 📝", self.benchmark.sequential_write)
                self.update_layout(layout)
                time.sleep(0.5)
                
                # Sequential Read
                self.run_benchmark("Sequential Read 📖", self.benchmark.sequential_read)
                self.update_layout(layout)
                time.sleep(0.5)
                
                # Random Write
                self.run_benchmark("Random Write 🎲", self.benchmark.random_write)
                self.update_layout(layout)
                time.sleep(0.5)
                
                # Random Read
                self.run_benchmark("Random Read 🎯", self.benchmark.random_read)
                self.update_layout(layout)
                
                # Show final results
                self.current_test = "✅ All tests completed!"
                self.update_layout(layout)
                time.sleep(3)
                
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Benchmark interrupted by user[/bold red]")
        finally:
            self.benchmark.cleanup()
    
    def show_welcome(self):
        """Show welcome screen with animation"""
        welcome_text = Text()
        welcome_text.append("\n\n")
        welcome_text.append("    ⚡ ", style="bold yellow")
        welcome_text.append("BENCHLAB", style="bold cyan")
        welcome_text.append(" ⚡", style="bold yellow")
        welcome_text.append("\n\n")
        welcome_text.append("  Disk Performance Benchmark Tool\n\n", style="italic bright_white")
        welcome_text.append("  Starting benchmarks...\n\n", style="dim")
        
        panel = Panel(
            Align.center(welcome_text, vertical="middle"),
            box=box.DOUBLE_EDGE,
            border_style="cyan",
            style="bold"
        )
        
        self.console.print(panel)
        time.sleep(1)
    
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
        
        # Calculate and show averages
        if self.results:
            avg_throughput = sum(r.throughput_mbps for r in self.results) / len(self.results)
            self.console.print(f"\n[bold cyan]Average Throughput:[/bold cyan] [bold yellow]{avg_throughput:.2f} MB/s[/bold yellow]")


def main():
    """Main entry point for TUI application"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BenchLab - Disk Performance Benchmark Tool")
    parser.add_argument("--size", type=int, default=100, help="Test file size in MB (default: 100)")
    parser.add_argument("--block", type=int, default=4, help="Block size in KB (default: 4)")
    parser.add_argument("--dir", type=str, default=None, help="Test directory (default: temp dir)")
    
    args = parser.parse_args()
    
    tui = BenchLabTUI(
        file_size_mb=args.size,
        block_size_kb=args.block,
        test_dir=args.dir
    )
    
    tui.show_welcome()
    tui.run_all_benchmarks()
    tui.show_summary()


if __name__ == "__main__":
    main()
