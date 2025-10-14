"""
Disk Performance Benchmarking Module
Provides sequential and random read/write performance testing
"""

import os
import time
import random
import tempfile
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class BenchmarkResult:
    """Results from a benchmark test"""
    test_name: str
    duration: float
    bytes_transferred: int
    throughput_mbps: float
    iops: Optional[int] = None


class DiskBenchmark:
    """Disk performance benchmarking tool"""
    
    def __init__(self, test_dir: Optional[str] = None, file_size_mb: int = 100, block_size_kb: int = 4):
        """
        Initialize disk benchmark
        
        Args:
            test_dir: Directory to run tests in (uses temp dir if None)
            file_size_mb: Size of test file in MB
            block_size_kb: Block size for I/O operations in KB
        """
        self.test_dir = test_dir or tempfile.gettempdir()
        self.file_size_mb = file_size_mb
        self.block_size_kb = block_size_kb
        self.block_size = block_size_kb * 1024
        self.file_size = file_size_mb * 1024 * 1024
        self.test_file = os.path.join(self.test_dir, f"benchmark_test_{os.getpid()}.tmp")
        
    def _generate_random_data(self, size: int) -> bytes:
        """Generate random data for writing"""
        return os.urandom(size)
    
    def sequential_write(self, progress_callback: Optional[Callable] = None) -> BenchmarkResult:
        """Test sequential write performance"""
        data = self._generate_random_data(self.block_size)
        blocks = self.file_size // self.block_size
        
        start_time = time.time()
        with open(self.test_file, 'wb') as f:
            for i in range(blocks):
                f.write(data)
                if progress_callback:
                    progress_callback((i + 1) / blocks * 100)
        
        # Ensure data is written to disk
        os.sync()
        
        duration = time.time() - start_time
        throughput_mbps = (self.file_size / (1024 * 1024)) / duration
        
        return BenchmarkResult(
            test_name="Sequential Write",
            duration=duration,
            bytes_transferred=self.file_size,
            throughput_mbps=throughput_mbps
        )
    
    def sequential_read(self, progress_callback: Optional[Callable] = None) -> BenchmarkResult:
        """Test sequential read performance"""
        if not os.path.exists(self.test_file):
            raise FileNotFoundError("Test file not found. Run sequential_write first.")
        
        blocks = self.file_size // self.block_size
        bytes_read = 0
        
        start_time = time.time()
        with open(self.test_file, 'rb') as f:
            for i in range(blocks):
                data = f.read(self.block_size)
                bytes_read += len(data)
                if progress_callback:
                    progress_callback((i + 1) / blocks * 100)
        
        duration = time.time() - start_time
        throughput_mbps = (bytes_read / (1024 * 1024)) / duration
        
        return BenchmarkResult(
            test_name="Sequential Read",
            duration=duration,
            bytes_transferred=bytes_read,
            throughput_mbps=throughput_mbps
        )
    
    def random_write(self, num_operations: int = 1000, progress_callback: Optional[Callable] = None) -> BenchmarkResult:
        """Test random write performance"""
        data = self._generate_random_data(self.block_size)
        
        # Create file if it doesn't exist
        if not os.path.exists(self.test_file):
            with open(self.test_file, 'wb') as f:
                f.write(b'\0' * self.file_size)
        
        max_position = self.file_size - self.block_size
        
        start_time = time.time()
        with open(self.test_file, 'r+b') as f:
            for i in range(num_operations):
                position = random.randint(0, max_position)
                f.seek(position)
                f.write(data)
                if progress_callback:
                    progress_callback((i + 1) / num_operations * 100)
        
        os.sync()
        
        duration = time.time() - start_time
        bytes_transferred = num_operations * self.block_size
        throughput_mbps = (bytes_transferred / (1024 * 1024)) / duration
        iops = int(num_operations / duration)
        
        return BenchmarkResult(
            test_name="Random Write",
            duration=duration,
            bytes_transferred=bytes_transferred,
            throughput_mbps=throughput_mbps,
            iops=iops
        )
    
    def random_read(self, num_operations: int = 1000, progress_callback: Optional[Callable] = None) -> BenchmarkResult:
        """Test random read performance"""
        if not os.path.exists(self.test_file):
            raise FileNotFoundError("Test file not found. Run sequential_write first.")
        
        max_position = self.file_size - self.block_size
        bytes_read = 0
        
        start_time = time.time()
        with open(self.test_file, 'rb') as f:
            for i in range(num_operations):
                position = random.randint(0, max_position)
                f.seek(position)
                data = f.read(self.block_size)
                bytes_read += len(data)
                if progress_callback:
                    progress_callback((i + 1) / num_operations * 100)
        
        duration = time.time() - start_time
        throughput_mbps = (bytes_read / (1024 * 1024)) / duration
        iops = int(num_operations / duration)
        
        return BenchmarkResult(
            test_name="Random Read",
            duration=duration,
            bytes_transferred=bytes_read,
            throughput_mbps=throughput_mbps,
            iops=iops
        )
    
    def cleanup(self):
        """Remove test file"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
