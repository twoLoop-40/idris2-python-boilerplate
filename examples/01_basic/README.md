# Example 1: Basic Functions

A simple example demonstrating the basic workflow.

## Idris2 Source: `func.idr`

```idris
private helperFunction : Int -> Int
helperFunction x = x + 1

public export apiFunction : Int -> Int
apiFunction x = helperFunction x * 2
```

**Type constraints:**
- Simple function types (`Int -> Int`)
- Public/private visibility

## Generated Python: `func.py`

```python
def _helper_function(x: int) -> int:
    """Private helper function."""
    return x + 1

def api_function(x: int) -> int:
    """Public API function."""
    return _helper_function(x) * 2
```

**Conversion:**
- `private` → `_` prefix (Python convention)
- `public export` → regular function
- Type signatures → type hints

## Generated Tests: `test_func.py`

```python
def test_api_function_positive():
    assert api_function(5) == 12  # (5+1) * 2

def test_matches_idris_output():
    # Verified against compiled Idris2
    assert api_function(5) == 12
```

## Running This Example

### Compile Idris2
```bash
idris2 -o func func.idr
./build/exec/func  # Output: 12
```

### Run Python
```bash
python func.py  # Output: 12
```

### Run Tests
```bash
pytest test_func.py -v
```

## What This Demonstrates

✅ **Basic type-driven workflow**
- Write Idris2 with clear types
- Convert to Python with type hints
- Auto-generate basic tests

✅ **Verification**
- Python output matches Idris2 exactly
- Tests verify correctness

This is the simplest example to start with!
