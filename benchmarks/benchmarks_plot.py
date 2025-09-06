"""
Plotting utilities for benchmark results visualization.

Generates charts showing performance comparisons between algorithms.
"""

import csv
import os
import sys

def main():
    """Main plotting function with graceful matplotlib handling."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("matplotlib is not installed. Plotting is optional.")
        print("To install: pip install matplotlib")
        print("Exiting gracefully.")
        sys.exit(0)
    
    results_file = "benchmarks/results.csv"
    if not os.path.exists(results_file):
        print(f"Results file {results_file} not found.")
        print("Please run 'python benchmarks/benchmarks_run.py' first.")
        sys.exit(1)
    
    results = []
    with open(results_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for key in ['s_len', 't_len', 'alphabet_size', 'sliding_mean', 'sliding_stddev', 
                       'indexed_mean', 'indexed_stddev', 'dispatcher_mean', 'dispatcher_stddev']:
                row[key] = float(row[key])
            results.append(row)
    
    if not results:
        print("No results found in CSV file.")
        sys.exit(1)
    
    os.makedirs("benchmarks", exist_ok=True)
    
    plot_mean_times(results)
    plot_speedup_ratios(results)
    plot_scaling_analysis(results)
    
    print("Plots generated successfully:")
    print("  - benchmarks/mean_times_comparison.png")
    print("  - benchmarks/speedup_ratios.png") 
    print("  - benchmarks/scaling_analysis.png")


def plot_mean_times(results):
    """Plot mean execution times for each algorithm."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    configs = [r['config'] for r in results]
    sliding_times = [r['sliding_mean'] * 1000 for r in results]  # Convert to ms
    indexed_times = [r['indexed_mean'] * 1000 for r in results]
    dispatcher_times = [r['dispatcher_mean'] * 1000 for r in results]
    
    x = np.arange(len(configs))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    bars1 = ax.bar(x - width, sliding_times, width, label='Sliding Window', alpha=0.8)
    bars2 = ax.bar(x, indexed_times, width, label='Indexed Positions', alpha=0.8)
    bars3 = ax.bar(x + width, dispatcher_times, width, label='Dispatcher', alpha=0.8)
    
    ax.set_xlabel('Configuration')
    ax.set_ylabel('Mean Execution Time (ms)')
    ax.set_title('Algorithm Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(configs, rotation=45, ha='right')
    ax.legend()
    ax.set_yscale('log')  # Log scale for better visualization
    
    def add_value_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height:.2f}',
                       xy=(bar.get_x() + bar.get_width() / 2, height),
                       xytext=(0, 3),
                       textcoords="offset points",
                       ha='center', va='bottom',
                       fontsize=8)
    
    add_value_labels(bars1)
    add_value_labels(bars2)
    add_value_labels(bars3)
    
    plt.tight_layout()
    plt.savefig('benchmarks/mean_times_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_speedup_ratios(results):
    """Plot speedup ratios between algorithms."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    configs = [r['config'] for r in results]
    speedups = []
    
    for r in results:
        if r['indexed_mean'] > 0:
            speedup = r['sliding_mean'] / r['indexed_mean']
        else:
            speedup = 1.0
        speedups.append(speedup)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.bar(configs, speedups, alpha=0.7, color='skyblue')
    ax.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Equal Performance')
    
    ax.set_xlabel('Configuration')
    ax.set_ylabel('Speedup Ratio (Sliding / Indexed)')
    ax.set_title('Performance Speedup: Sliding Window vs Indexed Positions')
    ax.set_xticklabels(configs, rotation=45, ha='right')
    ax.legend()
    
    for bar, speedup in zip(bars, speedups):
        height = bar.get_height()
        ax.annotate(f'{speedup:.2f}x',
                   xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3),
                   textcoords="offset points",
                   ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('benchmarks/speedup_ratios.png', dpi=300, bbox_inches='tight')
    plt.close()


def plot_scaling_analysis(results):
    """Plot scaling behavior with input size."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    s_lens = sorted(set(r['s_len'] for r in results))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    for t_len in sorted(set(r['t_len'] for r in results)):
        subset = [r for r in results if r['t_len'] == t_len]
        if len(subset) < 2:
            continue
            
        subset.sort(key=lambda x: x['s_len'])
        s_lens_subset = [r['s_len'] for r in subset]
        sliding_times = [r['sliding_mean'] * 1000 for r in subset]
        indexed_times = [r['indexed_mean'] * 1000 for r in subset]
        
        ax1.plot(s_lens_subset, sliding_times, 'o-', label=f'Sliding (t_len={t_len})', alpha=0.7)
        ax1.plot(s_lens_subset, indexed_times, 's--', label=f'Indexed (t_len={t_len})', alpha=0.7)
    
    ax1.set_xlabel('String Length |s|')
    ax1.set_ylabel('Mean Time (ms)')
    ax1.set_title('Scaling with String Length')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    for s_len in [1000, 10000, 100000]:
        subset = [r for r in results if r['s_len'] == s_len]
        if len(subset) < 2:
            continue
            
        subset.sort(key=lambda x: x['t_len'])
        t_lens_subset = [r['t_len'] for r in subset]
        sliding_times = [r['sliding_mean'] * 1000 for r in subset]
        indexed_times = [r['indexed_mean'] * 1000 for r in subset]
        
        ax2.plot(t_lens_subset, sliding_times, 'o-', label=f'Sliding (s_len={s_len})', alpha=0.7)
        ax2.plot(t_lens_subset, indexed_times, 's--', label=f'Indexed (s_len={s_len})', alpha=0.7)
    
    ax2.set_xlabel('Target Length |t|')
    ax2.set_ylabel('Mean Time (ms)')
    ax2.set_title('Scaling with Target Length')
    ax2.set_yscale('log')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('benchmarks/scaling_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    main()
