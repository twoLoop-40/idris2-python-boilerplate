"""
AUTO-GENERATED from src/SafeList.idr
Generated: 2025-10-15
DO NOT EDIT - Modify the Idris2 source instead
To regenerate: /convert src/SafeList.idr

This module demonstrates dependent types converted to runtime checks.
Original Idris2 guarantees are preserved as assertions.
"""

from typing import List, TypeVar, Tuple, Callable, Optional, Any
from dataclasses import dataclass

T = TypeVar('T')
A = TypeVar('A')
B = TypeVar('B')


# ============================================================================
# Basic Safe Operations
# ============================================================================

def safe_head(vec: List[T]) -> T:
    """Safe head: only works on non-empty lists

    Idris2 type: Vect (S n) a -> a
    Precondition: len(vec) >= 1 (non-empty vector)

    The type `Vect (S n)` in Idris2 means "vector with at least 1 element".
    The compiler prevents calling this on empty vectors.
    """
    assert len(vec) >= 1, "safe_head requires non-empty vector (len >= 1)"
    return vec[0]


def safe_tail(vec: List[T]) -> List[T]:
    """Safe tail: only works on non-empty lists

    Idris2 type: Vect (S n) a -> Vect n a
    Precondition: len(vec) >= 1
    Postcondition: len(result) == len(vec) - 1
    """
    assert len(vec) >= 1, "safe_tail requires non-empty vector"
    return vec[1:]


def safe_index(index: int, vec: List[T]) -> T:
    """Safe indexing using bounded indices

    Idris2 type: Fin n -> Vect n a -> a

    Fin n represents natural numbers strictly less than n.
    This makes out-of-bounds access impossible at compile time.
    At runtime, we check: 0 <= index < len(vec)
    """
    assert isinstance(index, int), f"Index must be int, got {type(index)}"
    assert 0 <= index < len(vec), \
        f"Index out of bounds: {index} not in range [0, {len(vec)})"
    return vec[index]


def safe_take(n: int, vec: List[T]) -> List[T]:
    """Take exactly n elements from a vector

    Idris2 type: (n : Nat) -> Vect (n + m) a -> Vect n a
    Precondition: len(vec) >= n (vector has at least n elements)
    Postcondition: len(result) == n
    """
    assert isinstance(n, int) and n >= 0, f"n must be non-negative int, got {n}"
    assert len(vec) >= n, \
        f"Vector too short: len={len(vec)}, need at least {n}"

    result = vec[:n]
    assert len(result) == n, "Postcondition: result length must equal n"
    return result


def safe_drop(n: int, vec: List[T]) -> List[T]:
    """Drop exactly n elements from a vector

    Idris2 type: (n : Nat) -> Vect (n + m) a -> Vect m a
    Precondition: len(vec) >= n
    Postcondition: len(result) == len(vec) - n
    """
    assert isinstance(n, int) and n >= 0, f"n must be non-negative int, got {n}"
    assert len(vec) >= n, \
        f"Cannot drop {n} elements from vector of length {len(vec)}"

    result = vec[n:]
    assert len(result) == len(vec) - n, "Postcondition: length arithmetic"
    return result


def zip_vect(vec1: List[A], vec2: List[B]) -> List[Tuple[A, B]]:
    """Zip two vectors of the same length

    Idris2 type: Vect n a -> Vect n b -> Vect n (a, b)
    Precondition: len(vec1) == len(vec2) (same length required)
    Postcondition: len(result) == len(vec1)

    The type enforces that both inputs have exactly the same length.
    """
    assert len(vec1) == len(vec2), \
        f"Vectors must have same length: {len(vec1)} != {len(vec2)}"

    result = list(zip(vec1, vec2))
    assert len(result) == len(vec1), "Postcondition: preserve length"
    return result


def safe_replicate(n: int, value: T) -> List[T]:
    """Replicate a value n times

    Idris2 type: (n : Nat) -> a -> Vect n a
    Postcondition: len(result) == n (exactly n copies)
    """
    assert isinstance(n, int) and n >= 0, f"n must be non-negative int, got {n}"

    result = [value] * n
    assert len(result) == n, "Postcondition: result has exactly n elements"
    return result


# ============================================================================
# Matrix Operations with Dependent Types
# ============================================================================

@dataclass
class Matrix:
    """Matrix with runtime dimension tracking

    Idris2 type: Matrix rows cols a

    In Idris2, dimensions are part of the type:
        Matrix 2 3 Int  -- 2×3 matrix of integers

    At runtime, we track dimensions and enforce them with assertions.
    """
    rows: int
    cols: int
    data: List[List[Any]]

    def __post_init__(self):
        """Verify matrix invariants"""
        assert self.rows >= 0, f"rows must be non-negative, got {self.rows}"
        assert self.cols >= 0, f"cols must be non-negative, got {self.cols}"
        assert len(self.data) == self.rows, \
            f"Data has {len(self.data)} rows, expected {self.rows}"
        for i, row in enumerate(self.data):
            assert len(row) == self.cols, \
                f"Row {i} has {len(row)} cols, expected {self.cols}"


def zero_matrix(rows: int, cols: int) -> Matrix:
    """Create a zero matrix

    Idris2 type: (rows : Nat) -> (cols : Nat) -> Matrix rows cols Int
    Postcondition: result.rows == rows and result.cols == cols
    """
    assert rows >= 0 and cols >= 0, "Dimensions must be non-negative"

    data = [[0] * cols for _ in range(rows)]
    return Matrix(rows, cols, data)


def mat_add(mat1: Matrix, mat2: Matrix) -> Matrix:
    """Matrix addition: dimensions must match

    Idris2 type: Matrix r c Int -> Matrix r c Int -> Matrix r c Int
    Precondition: mat1.rows == mat2.rows and mat1.cols == mat2.cols
    Postcondition: result has same dimensions

    The compiler ensures both matrices have the same size.
    """
    assert mat1.rows == mat2.rows, \
        f"Row mismatch: {mat1.rows} != {mat2.rows}"
    assert mat1.cols == mat2.cols, \
        f"Column mismatch: {mat1.cols} != {mat2.cols}"

    result_data = [
        [mat1.data[i][j] + mat2.data[i][j] for j in range(mat1.cols)]
        for i in range(mat1.rows)
    ]

    return Matrix(mat1.rows, mat1.cols, result_data)


def mat_index(i: int, j: int, mat: Matrix) -> Any:
    """Get element at position (i, j)

    Idris2 type: Fin r -> Fin c -> Matrix r c a -> a

    Fin types guarantee indices are in bounds at compile time!
    At runtime: 0 <= i < mat.rows and 0 <= j < mat.cols
    """
    assert 0 <= i < mat.rows, \
        f"Row index {i} out of bounds [0, {mat.rows})"
    assert 0 <= j < mat.cols, \
        f"Column index {j} out of bounds [0, {mat.cols})"

    return mat.data[i][j]


# ============================================================================
# Vector Operations
# ============================================================================

def map_vect(f: Callable[[A], B], vec: List[A]) -> List[B]:
    """Map over a vector - length is preserved

    Idris2 type: (a -> b) -> Vect n a -> Vect n b
    Postcondition: len(result) == len(vec)
    """
    result = [f(x) for x in vec]
    assert len(result) == len(vec), "Postcondition: preserve length"
    return result


def sum_vect(vec: List) -> Any:
    """Sum all elements in a vector

    Idris2 type: Num a => Vect n a -> a
    """
    return sum(vec)


# ============================================================================
# Validation with Dependent Types
# ============================================================================

@dataclass
class NonEmpty:
    """A non-empty list - type guarantees at least one element

    Idris2 type: NonEmpty : Type -> Type

    This type makes it impossible to represent an empty list.
    """
    head: Any
    tail: List[Any]

    def to_list(self) -> List[Any]:
        """Convert to regular list"""
        return [self.head] + self.tail

    def __len__(self) -> int:
        return 1 + len(self.tail)


def vect_to_non_empty(vec: List[T]) -> NonEmpty:
    """Convert non-empty vector to NonEmpty

    Idris2 type: Vect (S n) a -> NonEmpty a
    Precondition: len(vec) >= 1

    Both Vect (S n) and NonEmpty guarantee non-emptiness!
    """
    assert len(vec) >= 1, "vect_to_non_empty requires non-empty vector"
    return NonEmpty(head=vec[0], tail=vec[1:])


def safe_minimum(vec: List) -> Any:
    """Safe minimum - only works on non-empty vectors

    Idris2 type: Ord a => Vect (S n) a -> a
    Precondition: len(vec) >= 1

    Type guarantees we never call min() on empty list!
    """
    assert len(vec) >= 1, "safe_minimum requires non-empty vector"
    return min(vec)


def safe_maximum(vec: List) -> Any:
    """Safe maximum - only works on non-empty vectors

    Idris2 type: Ord a => Vect (S n) a -> a
    Precondition: len(vec) >= 1
    """
    assert len(vec) >= 1, "safe_maximum requires non-empty vector"
    return max(vec)


# ============================================================================
# Main Example (matching Idris2 output)
# ============================================================================

def main():
    """Demonstrate all safe operations"""
    print("=== Safe List Operations ===")

    # Safe head examples
    vec1 = [1, 2, 3, 4, 5]
    print(f'"Head: {safe_head(vec1)}"')

    # Safe indexing (bounded by length)
    print(f'"Index 0: {safe_index(0, vec1)}"')
    print(f'"Index 2: {safe_index(2, vec1)}"')

    # Take/drop
    print(f'"Take 3: {safe_take(3, vec1)}"')
    print(f'"Drop 2: {safe_drop(2, vec1)}"')

    # Zip
    vec2 = ['a', 'b', 'c', 'd', 'e']
    print(f'"Zipped: {zip_vect(vec1, vec2)}"')

    print("\n=== Matrix Operations ===")

    # Matrix operations
    mat1 = Matrix(2, 3, [[1, 2, 3], [4, 5, 6]])
    mat2 = Matrix(2, 3, [[7, 8, 9], [10, 11, 12]])
    result = mat_add(mat1, mat2)
    print(f'"Matrix Add: {result.data}"')

    # Matrix indexing
    print(f'"Element at (0,1): {mat_index(0, 1, mat1)}"')
    print(f'"Element at (1,2): {mat_index(1, 2, mat1)}"')

    print("\n=== Safe Min/Max ===")

    # Safe minimum/maximum
    nums = [42, 17, 93, 5]
    print(f'"Minimum: {safe_minimum(nums)}"')
    print(f'"Maximum: {safe_maximum(nums)}"')

    print("\n✅ All operations completed safely!")


if __name__ == "__main__":
    main()
