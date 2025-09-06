"""
Benchmark suite for minimum window substring algorithms.

Measures performance across different input sizes and characteristics.
"""

import time
import random
import csv
import os
import statistics
from typing import List, Tuple, Dict, Any
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from minimum_window_substring import min_window, _sliding_window, _indexed_positions_window


def generate_test_data(s_len: int, t_len: int, alphabet_size: int = 26) -> Tuple[str, str]:
    """Generate deterministic test data for benchmarking."""
    alphabet = 'abcdefghijklmnopqrstuvwxyz'[:alphabet_size]
    
    s_parts = []
    for _ in range(s_len // 10):
        s_parts.append(''.join(random.choices(alphabet, k=10)))
    
    remaining = s_len - len(''.join(s_parts))
    if remaining > 0:
        s_parts.append(''.join(random.choices(alphabet, k=remaining)))
    
    s = ''.join(s_parts)
    
    t_chars = random.choices(alphabet[:min(alphabet_size, len(set(s)))], k=t_len)
    t = ''.join(t_chars)
    
    return s, t


def benchmark_algorithm(func, s: str, t: str, num_runs: int = 5) -> Dict[str, float]:
    """Benchmark a single algorithm with multiple runs."""
    times = []
    
    for _ in range(num_runs):
        start_time = time.perf_counter()
        result = func(s, t)
        end_time = time.perf_counter()
        times.append(end_time - start_time)
    
    return {
        'mean': statistics.mean(times),
        'stddev': statistics.stdev(times) if len(times) > 1 else 0.0,
        'min': min(times),
        'max': max(times),
        'result_length': len(result) if result else 0
    }


def run_benchmarks() -> List[Dict[str, Any]]:
    """Run comprehensive benchmarks and return results."""
    random.seed(42)  # Deterministic results
    
    configs = [
        (1000, 5, 10, "small_s_tiny_t"),
        (1000, 50, 10, "small_s_small_t"),
        (10000, 10, 26, "medium_s_tiny_t"),
        (10000, 100, 26, "medium_s_medium_t"),
        (100000, 10, 26, "large_s_tiny_t"),
        (100000, 100, 26, "large_s_medium_t"),
        (100000, 1000, 26, "large_s_large_t"),
        (10000, 5, 1000, "medium_s_tiny_t_large_alphabet"),
    ]
    
    results = []
    
    print("Running benchmarks...")
    print("=" * 80)
    
    for s_len, t_len, alphabet_size, description in configs:
        print(f"\nConfiguration: {description}")
        print(f"  s_len={s_len}, t_len={t_len}, alphabet_size={alphabet_size}")
        
        s, t = generate_test_data(s_len, t_len, alphabet_size)
        
        sliding_stats = benchmark_algorithm(_sliding_window, s, t)
        
        indexed_stats = benchmark_algorithm(_indexed_positions_window, s, t)
        
        dispatcher_stats = benchmark_algorithm(min_window, s, t)
        
        result = {
            'config': description,
            's_len': s_len,
            't_len': t_len,
            'alphabet_size': alphabet_size,
            'sliding_mean': sliding_stats['mean'],
            'sliding_stddev': sliding_stats['stddev'],
            'indexed_mean': indexed_stats['mean'],
            'indexed_stddev': indexed_stats['stddev'],
            'dispatcher_mean': dispatcher_stats['mean'],
            'dispatcher_stddev': dispatcher_stats['stddev'],
            'result_length': sliding_stats['result_length']
        }
        results.append(result)
        
        print(f"  Sliding Window:    {sliding_stats['mean']:.6f}s ± {sliding_stats['stddev']:.6f}s")
        print(f"  Indexed Positions: {indexed_stats['mean']:.6f}s ± {indexed_stats['stddev']:.6f}s")
        print(f"  Dispatcher:        {dispatcher_stats['mean']:.6f}s ± {dispatcher_stats['stddev']:.6f}s")
        
        if indexed_stats['mean'] > 0:
            speedup = sliding_stats['mean'] / indexed_stats['mean']
            print(f"  Speedup (sliding/indexed): {speedup:.2f}x")
    
    return results


def save_results(results: List[Dict[str, Any]], filename: str = "benchmarks/results.csv"):
    """Save benchmark results to CSV file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w', newline='') as csvfile:
        if results:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    print(f"\nResults saved to {filename}")


def print_summary_table(results: List[Dict[str, Any]]):
    """Print a formatted summary table."""
    print("\n" + "=" * 80)
    print("BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"{'Configuration':<25} {'Sliding (ms)':<12} {'Indexed (ms)':<12} {'Dispatcher (ms)':<15} {'Speedup':<8}")
    print("-" * 80)
    
    for result in results:
        sliding_ms = result['sliding_mean'] * 1000
        indexed_ms = result['indexed_mean'] * 1000
        dispatcher_ms = result['dispatcher_mean'] * 1000
        speedup = sliding_ms / indexed_ms if indexed_ms > 0 else float('inf')
        
        print(f"{result['config']:<25} {sliding_ms:<12.3f} {indexed_ms:<12.3f} {dispatcher_ms:<15.3f} {speedup:<8.2f}")


if __name__ == "__main__":
    print("Minimum Window Substring Benchmarks")
    print("=" * 40)
    
    results = run_benchmarks()
    save_results(results)
    print_summary_table(results)
    
    print(f"\nBenchmark completed. Results saved to benchmarks/results.csv")
    print("Run 'python benchmarks/benchmarks_plot.py' to generate visualizations.")
