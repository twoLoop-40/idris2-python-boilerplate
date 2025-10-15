# Example 2: Dependent Types

Advanced example showcasing the power of dependent types for compile-time guarantees.

## Key Features

### Safe Operations (Type-Level Constraints)

```idris
-- Only works on non-empty vectors
safeHead : Vect (S n) a -> a

-- Bounded indexing (impossible to go out of bounds)
safeIndex : Fin n -> Vect n a -> a

-- Length tracking in types
safeTake : (n : Nat) -> Vect (n + m) a -> Vect n a
```

### Matrix Operations (Dimensions in Types)

```idris
-- Matrix with compile-time dimensions
Matrix : Nat -> Nat -> Type -> Type

-- Type ensures dimensions match!
matAdd : Matrix r c Int -> Matrix r c Int -> Matrix r c Int
```

## Python Conversion

All type-level guarantees become runtime checks:

```python
def safe_head(vec: List[T]) -> T:
    """Idris2 type: Vect (S n) a -> a"""
    assert len(vec) >= 1, "requires non-empty vector"
    return vec[0]

def mat_add(mat1: Matrix, mat2: Matrix) -> Matrix:
    """Idris2 type: Matrix r c Int -> Matrix r c Int -> Matrix r c Int"""
    assert mat1.rows == mat2.rows  # Dimension check
    assert mat1.cols == mat2.cols
    # ...
```

## Generated Tests (45 total, 100% passing)

### Precondition Tests
```python
def test_safe_head_rejects_empty():
    """Type: Vect (S n) requires non-empty"""
    with pytest.raises(AssertionError):
        safe_head([])  # Type prevents this!
```

### Property-Based Tests
```python
@given(n=st.integers(0, 50), m=st.integers(0, 50))
def test_safe_take_length_property(n, m):
    """Type: Vect (n + m) → Vect n"""
    vec = list(range(n + m))
    result = safe_take(n, vec)
    assert len(result) == n  # Always true!
```

### Integration Tests
```python
def test_matches_idris2_output():
    """Verify Python matches Idris2 exactly"""
    assert safe_head([1,2,3,4,5]) == 1
    assert safe_take(3, [1,2,3,4,5]) == [1,2,3]
```

## Running This Example

### Compile and Run Idris2
```bash
idris2 -o safelist SafeList.idr
./build/exec/safelist
```

Output:
```
=== Safe List Operations ===
"Head: 1"
"Index 0: 1"
...
✅ All operations completed safely!
```

### Run Python
```bash
python safe_list.py
```

Output: (identical to Idris2!)

### Run Tests
```bash
pytest test_safe_list.py -v
```

Result: **45/45 tests passed** ✅

## What This Demonstrates

### 1. Dependent Types → Runtime Checks

| Idris2 Type Constraint | Python Runtime Check |
|------------------------|----------------------|
| `Vect (S n)` (non-empty) | `assert len(vec) >= 1` |
| `Fin n` (bounded index) | `assert 0 <= i < n` |
| `Vect (n + m)` (length guarantee) | `assert len(vec) >= n` |
| `Matrix r c` (dimensions) | `assert rows == r and cols == c` |

### 2. Compile-Time → Test-Time

Every type constraint becomes a test:
- **Preconditions** → tests that invalid inputs are rejected
- **Postconditions** → tests that outputs meet guarantees
- **Invariants** → property-based tests

### 3. Bug Prevention

These bugs are **impossible** in Idris2, and **caught by tests** in Python:
- ❌ Empty list passed to `head`
- ❌ Out-of-bounds array access
- ❌ Matrix dimension mismatch
- ❌ Taking more elements than available

## Learning Path

1. **Read the Idris2 code** - Notice how types prevent errors
2. **Compare with Python** - See how assertions preserve guarantees
3. **Study the tests** - Understand how types become test cases
4. **Experiment** - Try breaking the code and see tests catch it!

## Advanced Concepts Demonstrated

- **Vect (S n)**: Non-empty list at type level
- **Fin n**: Bounded natural numbers (indices)
- **Dependent pairs**: Values that depend on other values
- **Type-level arithmetic**: `n + m` in types
- **Phantom types**: Dimensions in Matrix type

This example shows the **full power** of type-driven development!
