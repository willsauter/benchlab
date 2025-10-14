"""
GPU/AI Performance Benchmarking Module
Provides GPU compute and AI inference testing for Apple Silicon
"""

import time
import platform
from dataclasses import dataclass
from typing import Callable, Optional
import sys


@dataclass
class GPUBenchmarkResult:
    """Results from a GPU benchmark test"""
    test_name: str
    duration: float
    operations: int
    ops_per_second: float
    score: float
    gpu_type: Optional[str] = None


class GPUBenchmark:
    """GPU performance benchmarking tool"""
    
    def __init__(self):
        """Initialize GPU benchmark"""
        self.platform = platform.system()
        self.has_metal = False
        self.has_torch = False
        self.metal_device = None
        
        # Check for Metal support (Apple Silicon)
        if self.platform == "Darwin":
            try:
                import torch
                self.has_torch = True
                if torch.backends.mps.is_available():
                    self.has_metal = True
                    self.metal_device = torch.device("mps")
            except ImportError:
                pass
    
    def is_available(self) -> bool:
        """Check if GPU benchmarking is available"""
        return self.has_metal and self.has_torch
    
    def matrix_multiply(self, size: int = 2048, iterations: int = 100, progress_callback: Optional[Callable] = None) -> GPUBenchmarkResult:
        """Test GPU matrix multiplication performance"""
        if not self.is_available():
            raise RuntimeError("GPU/Metal not available. Install PyTorch with Metal support.")
        
        import torch
        
        # Create matrices on GPU
        a = torch.randn(size, size, device=self.metal_device)
        b = torch.randn(size, size, device=self.metal_device)
        
        # Warmup
        for _ in range(5):
            c = torch.matmul(a, b)
        
        # Benchmark
        start_time = time.time()
        
        for i in range(iterations):
            c = torch.matmul(a, b)
            
            if progress_callback:
                progress = ((i + 1) / iterations) * 100
                progress_callback(progress)
        
        # Ensure completion
        torch.mps.synchronize()
        
        duration = time.time() - start_time
        # FLOPs for matrix multiply: 2 * size^3 per operation
        flops = 2 * (size ** 3) * iterations
        gflops = (flops / duration) / 1e9
        score = gflops / 100  # Normalize
        
        return GPUBenchmarkResult(
            test_name="Matrix Multiply",
            duration=duration,
            operations=iterations,
            ops_per_second=iterations / duration,
            score=score,
            gpu_type="Apple Silicon Metal"
        )
    
    def convolution_2d(self, iterations: int = 100, progress_callback: Optional[Callable] = None) -> GPUBenchmarkResult:
        """Test GPU 2D convolution performance (common in AI)"""
        if not self.is_available():
            raise RuntimeError("GPU/Metal not available. Install PyTorch with Metal support.")
        
        import torch
        import torch.nn as nn
        
        # Create a typical convolution layer
        conv = nn.Conv2d(64, 128, kernel_size=3, padding=1).to(self.metal_device)
        
        # Create input tensor (batch_size=16, channels=64, height=224, width=224)
        x = torch.randn(16, 64, 224, 224, device=self.metal_device)
        
        # Warmup
        for _ in range(5):
            y = conv(x)
        
        # Benchmark
        start_time = time.time()
        
        for i in range(iterations):
            y = conv(x)
            
            if progress_callback:
                progress = ((i + 1) / iterations) * 100
                progress_callback(progress)
        
        torch.mps.synchronize()
        
        duration = time.time() - start_time
        ops_per_second = iterations / duration
        score = ops_per_second
        
        return GPUBenchmarkResult(
            test_name="2D Convolution",
            duration=duration,
            operations=iterations,
            ops_per_second=ops_per_second,
            score=score,
            gpu_type="Apple Silicon Metal"
        )
    
    def element_wise_ops(self, size: int = 10000000, iterations: int = 100, progress_callback: Optional[Callable] = None) -> GPUBenchmarkResult:
        """Test GPU element-wise operations"""
        if not self.is_available():
            raise RuntimeError("GPU/Metal not available. Install PyTorch with Metal support.")
        
        import torch
        
        # Create tensors
        a = torch.randn(size, device=self.metal_device)
        b = torch.randn(size, device=self.metal_device)
        
        # Warmup
        for _ in range(5):
            c = a * b + torch.sin(a) * torch.cos(b)
        
        # Benchmark
        start_time = time.time()
        
        for i in range(iterations):
            c = a * b + torch.sin(a) * torch.cos(b)
            
            if progress_callback:
                progress = ((i + 1) / iterations) * 100
                progress_callback(progress)
        
        torch.mps.synchronize()
        
        duration = time.time() - start_time
        ops_per_second = iterations / duration
        score = ops_per_second * 10  # Normalize
        
        return GPUBenchmarkResult(
            test_name="Element-wise Ops",
            duration=duration,
            operations=iterations,
            ops_per_second=ops_per_second,
            score=score,
            gpu_type="Apple Silicon Metal"
        )
    
    def transformer_attention(self, iterations: int = 50, progress_callback: Optional[Callable] = None) -> GPUBenchmarkResult:
        """Test transformer attention mechanism (key AI workload)"""
        if not self.is_available():
            raise RuntimeError("GPU/Metal not available. Install PyTorch with Metal support.")
        
        import torch
        import torch.nn as nn
        
        # Create multi-head attention layer
        embed_dim = 512
        num_heads = 8
        attention = nn.MultiheadAttention(embed_dim, num_heads).to(self.metal_device)
        
        # Create input (sequence_length=128, batch_size=32, embed_dim=512)
        seq_len, batch_size = 128, 32
        query = torch.randn(seq_len, batch_size, embed_dim, device=self.metal_device)
        key = torch.randn(seq_len, batch_size, embed_dim, device=self.metal_device)
        value = torch.randn(seq_len, batch_size, embed_dim, device=self.metal_device)
        
        # Warmup
        for _ in range(5):
            output, _ = attention(query, key, value)
        
        # Benchmark
        start_time = time.time()
        
        for i in range(iterations):
            output, _ = attention(query, key, value)
            
            if progress_callback:
                progress = ((i + 1) / iterations) * 100
                progress_callback(progress)
        
        torch.mps.synchronize()
        
        duration = time.time() - start_time
        ops_per_second = iterations / duration
        score = ops_per_second * 20  # Normalize
        
        return GPUBenchmarkResult(
            test_name="Transformer Attention",
            duration=duration,
            operations=iterations,
            ops_per_second=ops_per_second,
            score=score,
            gpu_type="Apple Silicon Metal"
        )
    
    def memory_bandwidth(self, size_mb: int = 500, iterations: int = 20, progress_callback: Optional[Callable] = None) -> GPUBenchmarkResult:
        """Test GPU memory bandwidth"""
        if not self.is_available():
            raise RuntimeError("GPU/Metal not available. Install PyTorch with Metal support.")
        
        import torch
        
        size = size_mb * 1024 * 1024 // 4  # 4 bytes per float32
        
        # Create large tensor
        data = torch.randn(size, device=self.metal_device)
        
        # Warmup
        for _ in range(3):
            result = data * 2.0
        
        # Benchmark
        start_time = time.time()
        
        for i in range(iterations):
            # Read and write to memory
            result = data * 2.0 + 1.0
            
            if progress_callback:
                progress = ((i + 1) / iterations) * 100
                progress_callback(progress)
        
        torch.mps.synchronize()
        
        duration = time.time() - start_time
        # Each iteration reads and writes the data
        bytes_transferred = size_mb * 1024 * 1024 * iterations * 2
        bandwidth_gbps = (bytes_transferred / (1024 ** 3)) / duration
        score = bandwidth_gbps
        
        return GPUBenchmarkResult(
            test_name="GPU Memory Bandwidth",
            duration=duration,
            operations=iterations,
            ops_per_second=iterations / duration,
            score=score,
            gpu_type="Apple Silicon Metal"
        )
    
    def ai_inference_simulation(self, iterations: int = 50, progress_callback: Optional[Callable] = None) -> GPUBenchmarkResult:
        """Simulate AI inference workload"""
        if not self.is_available():
            raise RuntimeError("GPU/Metal not available. Install PyTorch with Metal support.")
        
        import torch
        import torch.nn as nn
        
        # Create a small neural network (similar to MobileNet)
        class SimpleNet(nn.Module):
            def __init__(self):
                super(SimpleNet, self).__init__()
                self.conv1 = nn.Conv2d(3, 32, 3, padding=1)
                self.conv2 = nn.Conv2d(32, 64, 3, padding=1)
                self.conv3 = nn.Conv2d(64, 128, 3, padding=1)
                self.pool = nn.MaxPool2d(2, 2)
                self.fc = nn.Linear(128 * 28 * 28, 10)
                self.relu = nn.ReLU()
            
            def forward(self, x):
                x = self.relu(self.conv1(x))
                x = self.pool(x)
                x = self.relu(self.conv2(x))
                x = self.pool(x)
                x = self.relu(self.conv3(x))
                x = self.pool(x)
                x = x.view(-1, 128 * 28 * 28)
                x = self.fc(x)
                return x
        
        model = SimpleNet().to(self.metal_device)
        model.eval()
        
        # Create input (batch_size=1, channels=3, height=224, width=224)
        x = torch.randn(1, 3, 224, 224, device=self.metal_device)
        
        # Warmup
        with torch.no_grad():
            for _ in range(5):
                output = model(x)
        
        # Benchmark
        start_time = time.time()
        
        with torch.no_grad():
            for i in range(iterations):
                output = model(x)
                
                if progress_callback:
                    progress = ((i + 1) / iterations) * 100
                    progress_callback(progress)
        
        torch.mps.synchronize()
        
        duration = time.time() - start_time
        inferences_per_second = iterations / duration
        score = inferences_per_second * 50  # Normalize
        
        return GPUBenchmarkResult(
            test_name="AI Inference",
            duration=duration,
            operations=iterations,
            ops_per_second=inferences_per_second,
            score=score,
            gpu_type="Apple Silicon Metal"
        )
