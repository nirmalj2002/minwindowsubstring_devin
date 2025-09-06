# Minimum Window Substring

A complete, well-tested, optimized Python solution for the Minimum Window Substring problem with multiple algorithm implementations and comprehensive benchmarking.

## Problem Statement

Given two strings `s` and `t`, find the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If no such substring exists, return an empty string `""`.

- The order of characters does not matter, but multiplicity does (e.g., `t = "AABC"` requires two A characters)
- Strings are case-sensitive and treat all characters as individual tokens (including Unicode)
- Returns the substring from `s` with minimum length that contains all characters from `t`
- If multiple windows have equal minimal length, returns any one of them

### Examples

```python
s = "ADOBECODEBANC", t = "ABC"  # -> "BANC"
s = "a", t = "aa"               # -> ""
```

## Algorithms

This implementation provides two algorithms with an intelligent dispatcher:

### 1. Primary: Optimized Sliding Window

The standard two-pointer sliding window approach with character-frequency counters and a formed counter to track when the window satisfies the target string.

- **Time Complexity**: O(|s| + |t|)
- **Space Complexity**: O(U) where U is the size of the character set present in t/window
- **Best for**: Most general cases, especially when |t| is not extremely small compared to |s|

### 2. Alternative: Indexed Positions Technique

Builds an index map for characters in `s` (list of positions per character). For cases where |t| is small compared to |s|, this method can be faster by generating candidate windows using position merging.

- **Time Complexity**: O(|s| + k * log n) where k is the number of required characters
- **Space Complexity**: O(|s|) for position indices
- **Best for**: Very small |t| (≤ 10) with large |s| (> 100k) and large alphabet size

### Dispatcher Logic

The dispatcher automatically chooses the best algorithm:

- **Default**: Uses sliding window method (optimal for most cases)
- **Fallback**: Uses indexed positions when `len(t) <= 10`, `len(s) > 100,000`, and `len(set(s)) > 1000`

The heuristic is conservative and can be adjusted by modifying the threshold constants in the `min_window()` function. The sliding window approach is generally more efficient due to its linear time complexity and better cache locality.

## Installation and Setup

```bash
pip install -r requirements.txt
```

## Usage

```python
from minimum_window_substring import min_window

result = min_window("ADOBECODEBANC", "ABC")
print(result)  # "BANC"
```

## Testing

Run all tests:
```bash
pytest -q
```

Run tests with coverage:
```bash
coverage run --source=minimum_window_substring -m pytest && coverage report -m
```

The test suite includes:
- Basic examples and edge cases
- Empty string handling
- Unicode character support
- Case sensitivity verification
- Randomized consistency testing between algorithms
- Performance tests for large inputs
- Brute force validation for correctness

## Benchmarking

Run performance benchmarks:
```bash
python -m benchmarks.benchmarks_run
```

This generates deterministic benchmarks across various input sizes and saves results to `benchmarks/results.csv`.

Generate visualization plots:
```bash
python -m benchmarks.benchmarks_plot
```

### Benchmark Output

The benchmarks produce:
- **benchmarks/results.csv**: Raw numerical data
- **benchmarks/mean_times_comparison.png**: Bar chart comparing algorithm performance
- **benchmarks/speedup_ratios.png**: Speedup ratios between algorithms
- **benchmarks/scaling_analysis.png**: Scaling behavior with input size

The plotting script gracefully handles missing matplotlib by printing a message and exiting with code 0, ensuring tests don't fail if matplotlib is unavailable.

## API Reference

### Main Function

```python
def min_window(s: str, t: str) -> str
```

Finds the minimum window substring using the optimal algorithm based on input characteristics.

### Internal Helpers

```python
def _sliding_window(s: str, t: str) -> str
def _indexed_positions_window(s: str, t: str) -> str
```

These internal functions are exposed for testing and can be imported directly for algorithm-specific usage.

## Performance Characteristics

- **Sliding Window**: Excellent for general use, linear time complexity
- **Indexed Positions**: Can be faster for very specific input patterns (small target, large source)
- **Memory Usage**: Both algorithms use reasonable memory proportional to character set size
- **Large Inputs**: Tested with strings up to 100k+ characters

## Edge Cases Handled

- Empty strings (`s == ""` or `t == ""`)
- Impossible cases (`len(t) > len(s)`)
- Missing characters in source string
- Unicode and special characters
- Multiple valid windows of same length
- Case sensitivity

## File Structure

```
├── minimum_window_substring.py    # Main implementation
├── test_minimum_window_substring.py    # Comprehensive test suite
├── benchmarks/
│   ├── benchmarks_run.py         # Benchmark execution script
│   ├── benchmarks_plot.py        # Visualization generation
│   └── results.csv               # Generated benchmark data
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

## Dependencies

- **pytest**: Testing framework
- **coverage**: Code coverage analysis
- **matplotlib**: Optional, for generating plots (gracefully handled if missing)

## Contributing

The implementation follows Python best practices:
- Type hints for better code clarity
- Comprehensive docstrings
- Modular design with testable components
- Performance-conscious implementation avoiding unnecessary allocations
- Deterministic testing with fixed random seeds
