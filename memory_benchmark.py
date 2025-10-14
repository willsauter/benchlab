"""
Memory Performance Benchmarking Module
Provides memory bandwidth and cache hierarchy testing
"""

import time
import array
import random
from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class MemoryBenchmarkResult:
    """Results from a memory benchmark test"""
    test_name: str
    duration: float
    bytes_transferred: int
    bandwidth_gbps: float
    score: float
    buffer_size: Optional[str] = None


class MemoryBenchmark:
    """Memory performance benchmarking tool"""
    
    def __init__(self):
        """Initialize memory benchmark"""
        pass
    
    def sequential_read(self, size_mb: int = 100, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test sequential memory read bandwidth"""
        size = size_mb * 1024 * 1024
        
        # Create test array
        test_array = array.array('d', [float(i) for i in range(size // 8)])
        
        iterations = 10
        start_time = time.time()
        
        for iteration in range(iterations):
            # Sequential read
            total = 0.0
            for i in range(len(test_array)):
                total += test_array[i]
            
            if progress_callback:
                progress = ((iteration + 1) / iterations) * 100
                progress_callback(progress)
        
        duration = time.time() - start_time
        bytes_transferred = size * iterations
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / duration
        score = bandwidth_gbps
        
        return MemoryBenchmarkResult(
            test_name="Sequential Read",
            duration=duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size=f"{size_mb} MB"
        )
    
    def sequential_write(self, size_mb: int = 100, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test sequential memory write bandwidth"""
        size = size_mb * 1024 * 1024
        
        iterations = 10
        start_time = time.time()
        
        for iteration in range(iterations):
            # Sequential write
            test_array = array.array('d', [0.0] * (size // 8))
            for i in range(len(test_array)):
                test_array[i] = float(i)
            
            if progress_callback:
                progress = ((iteration + 1) / iterations) * 100
                progress_callback(progress)
        
        duration = time.time() - start_time
        bytes_transferred = size * iterations
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / duration
        score = bandwidth_gbps
        
        return MemoryBenchmarkResult(
            test_name="Sequential Write",
            duration=duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size=f"{size_mb} MB"
        )
    
    def random_access(self, size_mb: int = 100, num_accesses: int = 1000000, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test random memory access patterns"""
        size = size_mb * 1024 * 1024
        
        # Create test array
        test_array = array.array('d', [float(i) for i in range(size // 8)])
        array_len = len(test_array)
        
        # Pre-generate random indices
        indices = [random.randint(0, array_len - 1) for _ in range(num_accesses)]
        
        start_time = time.time()
        
        # Random access
        total = 0.0
        for i, idx in enumerate(indices):
            total += test_array[idx]
            
            if progress_callback and i % 10000 == 0:
                progress = (i / num_accesses) * 100
                progress_callback(progress)
        
        duration = time.time() - start_time
        bytes_transferred = num_accesses * 8  # 8 bytes per double
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / duration
        score = bandwidth_gbps * 10  # Scale up since random is typically slower
        
        return MemoryBenchmarkResult(
            test_name="Random Access",
            duration=duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size=f"{size_mb} MB"
        )
    
    def cache_test_l1(self, duration: float = 5.0, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test L1 cache performance (small array fits in L1)"""
        # L1 cache is typically 32-64KB, use 16KB to be safe
        size = 16 * 1024
        test_array = array.array('d', [float(i) for i in range(size // 8)])
        
        start_time = time.time()
        end_time = start_time + duration
        iterations = 0
        
        while time.time() < end_time:
            total = 0.0
            for i in range(len(test_array)):
                total += test_array[i]
            iterations += 1
            
            if progress_callback and iterations % 100 == 0:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        bytes_transferred = size * iterations
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / actual_duration
        score = bandwidth_gbps
        
        return MemoryBenchmarkResult(
            test_name="L1 Cache",
            duration=actual_duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size="16 KB"
        )
    
    def cache_test_l2(self, duration: float = 5.0, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test L2 cache performance (array fits in L2)"""
        # L2 cache is typically 256KB-1MB, use 256KB
        size = 256 * 1024
        test_array = array.array('d', [float(i) for i in range(size // 8)])
        
        start_time = time.time()
        end_time = start_time + duration
        iterations = 0
        
        while time.time() < end_time:
            total = 0.0
            for i in range(len(test_array)):
                total += test_array[i]
            iterations += 1
            
            if progress_callback and iterations % 10 == 0:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        bytes_transferred = size * iterations
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / actual_duration
        score = bandwidth_gbps
        
        return MemoryBenchmarkResult(
            test_name="L2 Cache",
            duration=actual_duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size="256 KB"
        )
    
    def cache_test_l3(self, duration: float = 5.0, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test L3 cache performance (array fits in L3)"""
        # L3 cache is typically 8-32MB, use 8MB
        size = 8 * 1024 * 1024
        test_array = array.array('d', [float(i) for i in range(size // 8)])
        
        start_time = time.time()
        end_time = start_time + duration
        iterations = 0
        
        while time.time() < end_time:
            total = 0.0
            for i in range(len(test_array)):
                total += test_array[i]
            iterations += 1
            
            if progress_callback:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        bytes_transferred = size * iterations
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / actual_duration
        score = bandwidth_gbps
        
        return MemoryBenchmarkResult(
            test_name="L3 Cache",
            duration=actual_duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size="8 MB"
        )
    
    def memory_copy(self, size_mb: int = 100, progress_callback: Optional[Callable] = None) -> MemoryBenchmarkResult:
        """Test memory copy bandwidth"""
        size = size_mb * 1024 * 1024
        
        # Create source array
        source = array.array('d', [float(i) for i in range(size // 8)])
        
        iterations = 10
        start_time = time.time()
        
        for iteration in range(iterations):
            # Copy array
            destination = array.array('d', source)
            
            if progress_callback:
                progress = ((iteration + 1) / iterations) * 100
                progress_callback(progress)
        
        duration = time.time() - start_time
        # Copy involves read + write
        bytes_transferred = size * iterations * 2
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / duration
        score = bandwidth_gbps
        
        return MemoryBenchmarkResult(
            test_name="Memory Copy",
            duration=duration,
            bytes_transferred=bytes_transferred,
            bandwidth_gbps=bandwidth_gbps,
            score=score,
            buffer_size=f"{size_mb} MB"
        )
