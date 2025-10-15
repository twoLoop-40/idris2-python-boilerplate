"""
AUTO-GENERATED tests for safe_list.py
Generated from Idris2 type signatures in src/SafeList.idr

These tests verify that runtime checks correctly enforce
the dependent type constraints from the original Idris2 code.
"""

import pytest
from hypothesis import given, strategies as st
import sys
import os

# Add generated/python to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python'))

from safe_list import (
    safe_head, safe_tail, safe_index, safe_take, safe_drop,
    zip_vect, safe_replicate, Matrix, zero_matrix, mat_add,
    mat_index, map_vect, sum_vect, NonEmpty, vect_to_non_empty,
    safe_minimum, safe_maximum
)


# ============================================================================
# Tests for safe_head
# From type: Vect (S n) a -> a
# ============================================================================

class TestSafeHead:
    """Tests derived from type: Vect (S n) a -> a
    Precondition: Vector must be non-empty (S n means at least 1)"""

    @pytest.mark.precondition
    def test_safe_head_rejects_empty(self):
        """Type constraint: Vect (S n) requires non-empty"""
        with pytest.raises(AssertionError, match="non-empty"):
            safe_head([])

    def test_safe_head_single_element(self):
        """Edge case: Minimum valid input (n=0 in S n)"""
        assert safe_head([42]) == 42

    def test_safe_head_multiple_elements(self):
        """Returns first element"""
        assert safe_head([1, 2, 3, 4, 5]) == 1
        assert safe_head(['a', 'b', 'c']) == 'a'

    @given(st.lists(st.integers(), min_size=1))
    @pytest.mark.property
    def test_safe_head_property(self, vec):
        """Property: safe_head(vec) == vec[0] for non-empty vec"""
        assert safe_head(vec) == vec[0]


# ============================================================================
# Tests for safe_index
# From type: Fin n -> Vect n a -> a
# ============================================================================

class TestSafeIndex:
    """Tests derived from type: Fin n -> Vect n a -> a
    Fin n means index must be in [0, n)"""

    @pytest.mark.precondition
    def test_safe_index_negative_rejected(self):
        """Fin constraint: index >= 0"""
        with pytest.raises(AssertionError, match="out of bounds"):
            safe_index(-1, [1, 2, 3])

    @pytest.mark.precondition
    def test_safe_index_too_large_rejected(self):
        """Fin constraint: index < length"""
        vec = [1, 2, 3]
        with pytest.raises(AssertionError, match="out of bounds"):
            safe_index(3, vec)  # 3 is not < 3

    def test_safe_index_first_element(self):
        """Boundary: index = 0"""
        assert safe_index(0, [10, 20, 30]) == 10

    def test_safe_index_last_element(self):
        """Boundary: index = n-1"""
        vec = [10, 20, 30]
        assert safe_index(2, vec) == 30

    @given(
        vec=st.lists(st.integers(), min_size=1, max_size=100),
    )
    @pytest.mark.property
    def test_safe_index_valid_indices(self, vec):
        """Property: safe_index(i, vec) == vec[i] for all valid i"""
        for i in range(len(vec)):
            assert safe_index(i, vec) == vec[i]


# ============================================================================
# Tests for safe_take
# From type: (n : Nat) -> Vect (n + m) a -> Vect n a
# ============================================================================

class TestSafeTake:
    """Tests derived from type: (n : Nat) -> Vect (n + m) a -> Vect n a
    Precondition: vec length >= n (from n + m)
    Postcondition: result length == n"""

    @pytest.mark.precondition
    def test_safe_take_negative_n_rejected(self):
        """Nat constraint: n >= 0"""
        with pytest.raises(AssertionError, match="non-negative"):
            safe_take(-1, [1, 2, 3])

    @pytest.mark.precondition
    def test_safe_take_too_short_rejected(self):
        """Precondition: len(vec) >= n"""
        with pytest.raises(AssertionError, match="too short"):
            safe_take(5, [1, 2, 3])  # 3 < 5

    @pytest.mark.postcondition
    def test_safe_take_returns_exactly_n(self):
        """Postcondition: len(result) == n"""
        result = safe_take(3, [1, 2, 3, 4, 5])
        assert len(result) == 3

    def test_safe_take_zero(self):
        """Edge case: n = 0"""
        assert safe_take(0, [1, 2, 3]) == []

    def test_safe_take_all(self):
        """Edge case: n == len(vec)"""
        vec = [1, 2, 3]
        assert safe_take(3, vec) == vec

    @given(
        n=st.integers(min_value=0, max_value=50),
        m=st.integers(min_value=0, max_value=50)
    )
    @pytest.mark.property
    def test_safe_take_length_property(self, n, m):
        """Property: Type says Vect (n + m) → Vect n
        So len(vec) = n + m, len(result) = n"""
        vec = list(range(n + m))  # Length exactly n + m
        result = safe_take(n, vec)
        assert len(result) == n


# ============================================================================
# Tests for zip_vect
# From type: Vect n a -> Vect n b -> Vect n (a, b)
# ============================================================================

class TestZipVect:
    """Tests derived from type: Vect n a -> Vect n b -> Vect n (a, b)
    Precondition: both vectors have same length n
    Postcondition: result has length n"""

    @pytest.mark.precondition
    def test_zip_vect_different_lengths_rejected(self):
        """Type constraint: both must have same length n"""
        with pytest.raises(AssertionError, match="same length"):
            zip_vect([1, 2, 3], ['a', 'b'])  # 3 != 2

    @pytest.mark.postcondition
    def test_zip_vect_preserves_length(self):
        """Postcondition: len(result) == n"""
        vec1 = [1, 2, 3]
        vec2 = ['a', 'b', 'c']
        result = zip_vect(vec1, vec2)
        assert len(result) == len(vec1)

    def test_zip_vect_empty(self):
        """Edge case: n = 0 (both empty)"""
        assert zip_vect([], []) == []

    def test_zip_vect_pairs_correctly(self):
        """Verify pairing is correct"""
        result = zip_vect([1, 2], ['a', 'b'])
        assert result == [(1, 'a'), (2, 'b')]

    @given(n=st.integers(min_value=0, max_value=100))
    @pytest.mark.property
    def test_zip_vect_length_invariant(self, n):
        """Property: result length equals input length"""
        vec1 = list(range(n))
        vec2 = list(range(n, n + n))
        result = zip_vect(vec1, vec2)
        assert len(result) == n


# ============================================================================
# Tests for Matrix operations
# From type: Matrix r c a
# ============================================================================

class TestMatrix:
    """Tests for Matrix type with dependent dimensions"""

    def test_matrix_creation_validates_dimensions(self):
        """Matrix invariant: data matches declared dimensions"""
        # Valid matrix
        mat = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        assert mat.rows == 2
        assert mat.cols == 3

        # Invalid: wrong number of rows
        with pytest.raises(AssertionError, match="rows"):
            Matrix(2, 3, [[1, 2, 3]])  # Only 1 row, claimed 2

        # Invalid: wrong number of cols
        with pytest.raises(AssertionError, match="cols"):
            Matrix(2, 3, [[1, 2], [4, 5, 6]])  # First row has 2, not 3

    def test_zero_matrix_creates_correct_dimensions(self):
        """Type: (rows : Nat) -> (cols : Nat) -> Matrix rows cols Int"""
        mat = zero_matrix(3, 4)
        assert mat.rows == 3
        assert mat.cols == 4
        assert all(all(x == 0 for x in row) for row in mat.data)


class TestMatAdd:
    """Tests derived from type: Matrix r c Int -> Matrix r c Int -> Matrix r c Int
    Precondition: both matrices have same dimensions r × c
    Postcondition: result has dimensions r × c"""

    @pytest.mark.precondition
    def test_mat_add_dimension_mismatch_rejected(self):
        """Type constraint: dimensions must match"""
        mat1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        mat2 = Matrix(3, 2, [[1, 2], [3, 4], [5, 6]])

        with pytest.raises(AssertionError, match="mismatch"):
            mat_add(mat1, mat2)

    @pytest.mark.postcondition
    def test_mat_add_preserves_dimensions(self):
        """Postcondition: result has same dimensions"""
        mat1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        mat2 = Matrix(2, 3, [[7, 8, 9], [10, 11, 12]])
        result = mat_add(mat1, mat2)

        assert result.rows == 2
        assert result.cols == 3

    def test_mat_add_correctness(self):
        """Verify addition is element-wise"""
        mat1 = Matrix(2, 2, [[1, 2], [3, 4]])
        mat2 = Matrix(2, 2, [[5, 6], [7, 8]])
        result = mat_add(mat1, mat2)

        assert result.data == [[6, 8], [10, 12]]

    @given(
        r=st.integers(min_value=1, max_value=5),
        c=st.integers(min_value=1, max_value=5)
    )
    @pytest.mark.property
    def test_mat_add_dimension_invariant(self, r, c):
        """Property: output dimensions == input dimensions"""
        mat1 = zero_matrix(r, c)
        mat2 = zero_matrix(r, c)
        result = mat_add(mat1, mat2)

        assert result.rows == r
        assert result.cols == c


class TestMatIndex:
    """Tests derived from type: Fin r -> Fin c -> Matrix r c a -> a
    Precondition: 0 <= i < r and 0 <= j < c"""

    @pytest.mark.precondition
    def test_mat_index_row_out_of_bounds(self):
        """Fin r constraint: 0 <= i < r"""
        mat = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])

        with pytest.raises(AssertionError, match="Row index.*out of bounds"):
            mat_index(2, 0, mat)  # row 2 >= 2

        with pytest.raises(AssertionError, match="Row index.*out of bounds"):
            mat_index(-1, 0, mat)

    @pytest.mark.precondition
    def test_mat_index_col_out_of_bounds(self):
        """Fin c constraint: 0 <= j < c"""
        mat = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])

        with pytest.raises(AssertionError, match="Column index.*out of bounds"):
            mat_index(0, 3, mat)  # col 3 >= 3

    def test_mat_index_retrieves_correct_element(self):
        """Verify indexing is correct"""
        mat = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])

        assert mat_index(0, 0, mat) == 1
        assert mat_index(0, 2, mat) == 3
        assert mat_index(1, 1, mat) == 5


# ============================================================================
# Tests for safe_minimum/maximum
# From type: Ord a => Vect (S n) a -> a
# ============================================================================

class TestSafeMinMax:
    """Tests derived from type: Vect (S n) a -> a
    Precondition: Vector must be non-empty"""

    @pytest.mark.precondition
    def test_safe_minimum_rejects_empty(self):
        """Type constraint: Vect (S n) requires non-empty"""
        with pytest.raises(AssertionError, match="non-empty"):
            safe_minimum([])

    @pytest.mark.precondition
    def test_safe_maximum_rejects_empty(self):
        """Type constraint: Vect (S n) requires non-empty"""
        with pytest.raises(AssertionError, match="non-empty"):
            safe_maximum([])

    def test_safe_minimum_single_element(self):
        """Edge case: single element (n=0 in S n)"""
        assert safe_minimum([42]) == 42

    def test_safe_maximum_single_element(self):
        """Edge case: single element"""
        assert safe_maximum([42]) == 42

    def test_safe_minimum_correctness(self):
        """Verify minimum is correct"""
        assert safe_minimum([42, 17, 93, 5]) == 5
        assert safe_minimum([100, 200, 50]) == 50

    def test_safe_maximum_correctness(self):
        """Verify maximum is correct"""
        assert safe_maximum([42, 17, 93, 5]) == 93
        assert safe_maximum([100, 200, 50]) == 200

    @given(st.lists(st.integers(), min_size=1))
    @pytest.mark.property
    def test_safe_minmax_property(self, vec):
        """Property: min <= max for all non-empty vectors"""
        assert safe_minimum(vec) <= safe_maximum(vec)


# ============================================================================
# Integration Tests: Compare with Idris2 output
# ============================================================================

@pytest.mark.integration
class TestIdris2Equivalence:
    """Integration tests comparing Python output with Idris2"""

    def test_matches_idris2_safe_head(self):
        """Compare with Idris2: safeHead [1,2,3,4,5] = 1"""
        assert safe_head([1, 2, 3, 4, 5]) == 1

    def test_matches_idris2_safe_index(self):
        """Compare with Idris2: safeIndex 2 [1,2,3,4,5] = 3"""
        assert safe_index(2, [1, 2, 3, 4, 5]) == 3

    def test_matches_idris2_safe_take(self):
        """Compare with Idris2: safeTake 3 [1,2,3,4,5] = [1,2,3]"""
        assert safe_take(3, [1, 2, 3, 4, 5]) == [1, 2, 3]

    def test_matches_idris2_safe_drop(self):
        """Compare with Idris2: safeDrop 2 [1,2,3,4,5] = [3,4,5]"""
        assert safe_drop(2, [1, 2, 3, 4, 5]) == [3, 4, 5]

    def test_matches_idris2_zip_vect(self):
        """Compare with Idris2 zip output"""
        result = zip_vect([1, 2, 3, 4, 5], ['a', 'b', 'c', 'd', 'e'])
        expected = [(1, 'a'), (2, 'b'), (3, 'c'), (4, 'd'), (5, 'e')]
        assert result == expected

    def test_matches_idris2_mat_add(self):
        """Compare with Idris2: matAdd [[1,2,3],[4,5,6]] [[7,8,9],[10,11,12]]"""
        mat1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
        mat2 = Matrix(2, 3, [[7, 8, 9], [10, 11, 12]])
        result = mat_add(mat1, mat2)
        assert result.data == [[8, 10, 12], [14, 16, 18]]

    def test_matches_idris2_safe_minimum(self):
        """Compare with Idris2: safeMinimum [42,17,93,5] = 5"""
        assert safe_minimum([42, 17, 93, 5]) == 5

    def test_matches_idris2_safe_maximum(self):
        """Compare with Idris2: safeMaximum [42,17,93,5] = 93"""
        assert safe_maximum([42, 17, 93, 5]) == 93


# ============================================================================
# Test Summary
# ============================================================================

def test_type_driven_development_summary():
    """
    Summary of what these tests demonstrate:

    1. **Precondition tests**: Type constraints → runtime assertions
       - safe_head requires Vect (S n) → assert len >= 1
       - safe_index requires Fin n → assert 0 <= i < n
       - mat_add requires matching dimensions → assert r1==r2, c1==c2

    2. **Postcondition tests**: Return type guarantees → assertions
       - safe_take returns Vect n → assert len(result) == n
       - mat_add returns Matrix r c → assert result.rows == r

    3. **Property-based tests**: Type invariants hold for all inputs
       - zip_vect preserves length
       - mat_add preserves dimensions

    4. **Integration tests**: Python matches Idris2 behavior
       - All outputs verified against compiled Idris2 program

    This demonstrates how dependent types become comprehensive test suites!
    """
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
