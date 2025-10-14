"""
CPU Performance Benchmarking Module
Provides single-core, multi-core, and various computational tests
"""

import time
import math
import hashlib
import multiprocessing
import platform
import subprocess
from dataclasses import dataclass
from typing import Callable, Optional, List


@dataclass
class CPUBenchmarkResult:
    """Results from a CPU benchmark test"""
    test_name: str
    duration: float
    operations: int
    ops_per_second: float
    score: float
    cores_used: int = 1
    temperature: Optional[float] = None


class CPUBenchmark:
    """CPU performance benchmarking tool"""
    
    def __init__(self):
        """Initialize CPU benchmark"""
        self.cpu_count = multiprocessing.cpu_count()
        self.platform = platform.system()
        
    def _get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature (macOS specific)"""
        try:
            if self.platform == "Darwin":  # macOS
                result = subprocess.run(
                    ["sudo", "powermetrics", "--samplers", "smc", "-i1", "-n1"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                # Parse output for CPU die temperature
                for line in result.stdout.split('\n'):
                    if 'CPU die temperature' in line:
                        temp_str = line.split(':')[1].strip().split()[0]
                        return float(temp_str)
            return None
        except Exception:
            return None
    
    def single_core_integer(self, duration: float = 5.0, progress_callback: Optional[Callable] = None) -> CPUBenchmarkResult:
        """Test single-core integer performance"""
        start_temp = self._get_cpu_temperature()
        operations = 0
        start_time = time.time()
        end_time = start_time + duration
        
        # Prime number calculation (CPU intensive)
        n = 2
        while time.time() < end_time:
            # Check if n is prime
            is_prime = True
            if n > 2:
                for i in range(2, int(math.sqrt(n)) + 1):
                    if n % i == 0:
                        is_prime = False
                        break
            if is_prime:
                operations += 1
            n += 1
            
            if progress_callback and operations % 100 == 0:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        ops_per_second = operations / actual_duration
        score = ops_per_second / 1000  # Normalize score
        end_temp = self._get_cpu_temperature()
        
        return CPUBenchmarkResult(
            test_name="Single-Core Integer",
            duration=actual_duration,
            operations=operations,
            ops_per_second=ops_per_second,
            score=score,
            cores_used=1,
            temperature=end_temp
        )
    
    def single_core_floating_point(self, duration: float = 5.0, progress_callback: Optional[Callable] = None) -> CPUBenchmarkResult:
        """Test single-core floating point performance"""
        start_temp = self._get_cpu_temperature()
        operations = 0
        start_time = time.time()
        end_time = start_time + duration
        
        # Floating point operations
        x = 1.0
        while time.time() < end_time:
            x = math.sqrt(x + 1.0)
            x = math.sin(x) * math.cos(x)
            x = math.exp(x / 100.0)
            x = math.log(abs(x) + 1.0)
            operations += 4
            
            if progress_callback and operations % 1000 == 0:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        ops_per_second = operations / actual_duration
        score = ops_per_second / 100000  # Normalize score
        end_temp = self._get_cpu_temperature()
        
        return CPUBenchmarkResult(
            test_name="Single-Core Float",
            duration=actual_duration,
            operations=operations,
            ops_per_second=ops_per_second,
            score=score,
            cores_used=1,
            temperature=end_temp
        )
    
    def _worker_hash(self, iterations: int) -> int:
        """Worker function for multi-core hash test"""
        operations = 0
        data = b"BenchLab benchmark data"
        for i in range(iterations):
            h = hashlib.sha256(data + str(i).encode())
            h.digest()
            operations += 1
        return operations
    
    def multi_core_hash(self, duration: float = 10.0, progress_callback: Optional[Callable] = None) -> CPUBenchmarkResult:
        """Test multi-core performance with hashing"""
        start_temp = self._get_cpu_temperature()
        start_time = time.time()
        
        # Calculate iterations per worker
        iterations_per_worker = 10000
        
        # Create worker pool
        with multiprocessing.Pool(self.cpu_count) as pool:
            results = []
            workers_started = 0
            total_workers = int((duration / 2) * self.cpu_count)  # Estimate
            
            for _ in range(total_workers):
                result = pool.apply_async(self._worker_hash, (iterations_per_worker,))
                results.append(result)
                workers_started += 1
                
                if progress_callback:
                    elapsed = time.time() - start_time
                    if elapsed < duration:
                        progress = (elapsed / duration) * 100
                        progress_callback(min(progress, 100))
                    else:
                        break
                
                # Stop spawning if duration exceeded
                if time.time() - start_time > duration:
                    break
            
            # Collect results
            total_operations = sum(r.get() for r in results if r.ready())
        
        actual_duration = time.time() - start_time
        ops_per_second = total_operations / actual_duration
        score = ops_per_second / 10000  # Normalize score
        end_temp = self._get_cpu_temperature()
        
        return CPUBenchmarkResult(
            test_name="Multi-Core Hash",
            duration=actual_duration,
            operations=total_operations,
            ops_per_second=ops_per_second,
            score=score,
            cores_used=self.cpu_count,
            temperature=end_temp
        )
    
    def _worker_compress(self, data: bytes) -> int:
        """Worker function for compression test"""
        import zlib
        compressed = zlib.compress(data, level=6)
        return len(compressed)
    
    def compression_test(self, duration: float = 10.0, progress_callback: Optional[Callable] = None) -> CPUBenchmarkResult:
        """Test CPU with compression workload"""
        import zlib
        start_temp = self._get_cpu_temperature()
        start_time = time.time()
        end_time = start_time + duration
        
        # Generate test data
        test_data = b"BenchLab " * 1000  # 9KB of data
        operations = 0
        bytes_compressed = 0
        
        while time.time() < end_time:
            compressed = zlib.compress(test_data, level=6)
            bytes_compressed += len(test_data)
            operations += 1
            
            if progress_callback and operations % 10 == 0:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        ops_per_second = operations / actual_duration
        mbps = (bytes_compressed / (1024 * 1024)) / actual_duration
        score = mbps / 10  # Normalize score
        end_temp = self._get_cpu_temperature()
        
        return CPUBenchmarkResult(
            test_name="Compression",
            duration=actual_duration,
            operations=operations,
            ops_per_second=ops_per_second,
            score=score,
            cores_used=1,
            temperature=end_temp
        )
    
    def crypto_test(self, duration: float = 5.0, progress_callback: Optional[Callable] = None) -> CPUBenchmarkResult:
        """Test CPU with cryptographic operations"""
        start_temp = self._get_cpu_temperature()
        start_time = time.time()
        end_time = start_time + duration
        
        operations = 0
        data = b"BenchLab benchmark data for cryptographic testing"
        
        while time.time() < end_time:
            # Multiple hash algorithms
            hashlib.sha256(data).digest()
            hashlib.sha512(data).digest()
            hashlib.md5(data).digest()
            operations += 3
            
            if progress_callback and operations % 100 == 0:
                progress = ((time.time() - start_time) / duration) * 100
                progress_callback(min(progress, 100))
        
        actual_duration = time.time() - start_time
        ops_per_second = operations / actual_duration
        score = ops_per_second / 10000  # Normalize score
        end_temp = self._get_cpu_temperature()
        
        return CPUBenchmarkResult(
            test_name="Cryptography",
            duration=actual_duration,
            operations=operations,
            ops_per_second=ops_per_second,
            score=score,
            cores_used=1,
            temperature=end_temp
        )
