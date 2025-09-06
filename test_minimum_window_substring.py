"""
Comprehensive test suite for minimum window substring implementation.
"""

import pytest
import random
import string
from collections import Counter
from minimum_window_substring import (
    min_window, 
    _sliding_window, 
    _indexed_positions_window
)


class TestMinimumWindowSubstring:
    """Test cases for minimum window substring algorithms."""
    
    def test_basic_examples(self):
        """Test the provided examples."""
        assert min_window("ADOBECODEBANC", "ABC") == "BANC"
        assert min_window("a", "aa") == ""
    
    def test_empty_inputs(self):
        """Test edge cases with empty strings."""
        assert min_window("", "") == ""
        assert min_window("", "a") == ""
        assert min_window("a", "") == ""
        assert min_window("", "abc") == ""
    
    def test_impossible_cases(self):
        """Test cases where no valid window exists."""
        assert min_window("a", "aa") == ""
        assert min_window("abc", "def") == ""
        assert min_window("short", "verylongstring") == ""
    
    def test_single_character(self):
        """Test single character cases."""
        assert min_window("a", "a") == "a"
        assert min_window("aaa", "a") == "a"
        assert min_window("abc", "c") == "c"
    
    def test_repeated_characters(self):
        """Test cases with repeated characters in target."""
        assert min_window("ADOBECODEBANC", "AABC") == "ADOBECODEBA"
        assert min_window("aaab", "aab") == "aab"
        assert min_window("aabbcc", "abc") == "abbc"
    
    def test_unicode_characters(self):
        """Test with unicode characters."""
        assert min_window("αβγδεζ", "αγε") == "αβγδε"
        assert min_window("🚀🌟⭐🌙", "🌟🌙") == "🌟⭐🌙"
        assert min_window("café", "fé") == "fé"
    
    def test_case_sensitivity(self):
        """Test case sensitivity."""
        assert min_window("AaBbCc", "abc") == "aBbCc"
        assert min_window("AaBbCc", "ABC") == "AaBbC"
    
    def test_whole_string_required(self):
        """Test cases where entire string is the minimum window."""
        assert min_window("abc", "abc") == "abc"
        assert min_window("abcdef", "fed") == "def"
    
    def test_multiple_valid_windows(self):
        """Test cases with multiple valid windows of same length."""
        result = min_window("abab", "ab")
        assert result in ["ab", "ba"]  # Both are valid minimal windows
        assert len(result) == 2
    
    def test_internal_helpers_consistency(self):
        """Test that both internal algorithms produce consistent results."""
        test_cases = [
            ("ADOBECODEBANC", "ABC"),
            ("abcdef", "cf"),
            ("aabbcc", "abc"),
            ("", ""),
            ("a", "aa"),
            ("hello", "ell"),
        ]
        
        for s, t in test_cases:
            sliding_result = _sliding_window(s, t)
            indexed_result = _indexed_positions_window(s, t)
            
            if sliding_result == "":
                assert indexed_result == "", f"Inconsistent results for ({s}, {t})"
            else:
                assert len(sliding_result) == len(indexed_result), \
                    f"Different window lengths for ({s}, {t}): {len(sliding_result)} vs {len(indexed_result)}"
                
                assert _is_valid_window(s, t, sliding_result)
                assert _is_valid_window(s, t, indexed_result)
    
    def test_randomized_consistency(self):
        """Test consistency with randomized small inputs."""
        random.seed(42)  # Deterministic testing
        
        for _ in range(50):
            s_len = random.randint(1, 20)
            t_len = random.randint(1, min(5, s_len))
            
            alphabet = string.ascii_lowercase[:random.randint(2, 5)]
            s = ''.join(random.choices(alphabet, k=s_len))
            t = ''.join(random.choices(alphabet, k=t_len))
            
            sliding_result = _sliding_window(s, t)
            indexed_result = _indexed_positions_window(s, t)
            brute_force_result = _brute_force_window(s, t)
            
            if brute_force_result == "":
                assert sliding_result == ""
                assert indexed_result == ""
            else:
                assert len(sliding_result) == len(brute_force_result)
                assert len(indexed_result) == len(brute_force_result)
                assert _is_valid_window(s, t, sliding_result)
                assert _is_valid_window(s, t, indexed_result)
    
    @pytest.mark.slow
    def test_performance_large_input(self):
        """Test performance with large inputs."""
        import time
        
        s = "a" * 50000 + "b" * 50000 + "c" * 1000
        t = "abc"
        
        start_time = time.time()
        result = min_window(s, t)
        end_time = time.time()
        
        assert end_time - start_time < 1.0
        assert len(result) >= 3  # At minimum must contain a, b, c
        assert "a" in result and "b" in result and "c" in result
    
    def test_dispatcher_logic(self):
        """Test that dispatcher chooses appropriate algorithm."""
        large_s = "a" * 100000 + "b" + "c"
        small_t = "abc"
        
        result = min_window(large_s, small_t)
        assert result == "abc"


def _is_valid_window(s: str, t: str, window: str) -> bool:
    """Check if a window contains all required characters from t."""
    if not window:
        return not t or not any(char in s for char in set(t))
    
    if window not in s:
        return False
    
    t_count = Counter(t)
    window_count = Counter(window)
    
    for char, count in t_count.items():
        if window_count[char] < count:
            return False
    
    return True


def _brute_force_window(s: str, t: str) -> str:
    """Brute force O(n^3) solution for testing correctness."""
    if not s or not t or len(t) > len(s):
        return ""
    
    if not t:
        return ""
    
    t_count = Counter(t)
    min_len = float('inf')
    min_window = ""
    
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            window = s[i:j]
            window_count = Counter(window)
            
            valid = True
            for char, count in t_count.items():
                if window_count[char] < count:
                    valid = False
                    break
            
            if valid and len(window) < min_len:
                min_len = len(window)
                min_window = window
    
    return min_window


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
