# Idris2 to Python Code Generation System

## Project Vision

A revolutionary AI-assisted code generation system that uses **dependent types** to eliminate the infinite debugging loop common in AI code generation.

## Core Concept

```
Natural Language → AI → Idris2 (Dependent Types) → Python (Runtime Checks) + Auto-generated Tests
                   ↑                           ↓
                   └──── Compile Errors ───────┘
```

### Why This Approach?

**Problem with Traditional AI Code Generation:**
- Ambiguous natural language specifications
- No compile-time verification
- Infinite debugging loops (AI fixes bug A → creates bug B → fixes B → recreates A)
- Missing edge cases

**Solution: Idris2 as Intermediate Representation:**
1. **Precise Specifications**: Dependent types express exact requirements
2. **Compile-Time Verification**: Type checker catches errors before Python generation
3. **Automatic Test Generation**: Type signatures generate comprehensive test cases
4. **Bug Class Elimination**: Types prevent entire categories of bugs (null references, array bounds, etc.)

## Architecture

### Workflow

```
1. Natural Language Requirement
   ↓
2. AI generates Idris2 type signature (with dependent types)
   ↓
3. Human expert reviews/refines types ← Critical quality gate
   ↓
4. AI implements Idris2 function
   ↓
5. Idris2 compiler verification
   ↓ (if errors, back to step 4)
6. Automated Python conversion
   - Type constraints → Runtime assertions
   - Pattern matching → Conditional logic
   - Dependent types → Precondition/postcondition checks
   ↓
7. Automated test generation from type specifications
   ↓
8. Execute tests
   ↓
9. Production-ready Python code
```

### Component Responsibilities

#### 1. Idris2 Layer (Specification & Implementation)
- **Purpose**: Formal specification with executable implementation
- **Benefits**:
  - Declarative and concise
  - Type-level guarantees
  - Pattern matching for exhaustive case handling
  - Compiler-verified correctness

#### 2. Python Layer (Runtime Implementation)
- **Purpose**: Practical execution environment
- **Generated Elements**:
  - Type hints (best effort)
  - Runtime assertions (from dependent type constraints)
  - Docstrings (from type signatures)
  - Error messages (from type preconditions)

#### 3. Test Layer (Verification)
- **Auto-generated from**:
  - Type signatures → property-based tests
  - Preconditions → boundary tests
  - Pattern matching → branch coverage tests
  - Dependent types → invariant tests

## Example: Simple Function

### Idris2 Specification
```idris
private helperFunction : Int -> Int
helperFunction x = x + 1

public export apiFunction : Int -> Int
apiFunction x = helperFunction x * 2
```

### Generated Python
```python
def _helper_function(x: int) -> int:
    """Private helper function from Idris2.

    Type: Int -> Int
    """
    return x + 1

def api_function(x: int) -> int:
    """Public API function from Idris2.

    Type: Int -> Int
    Implementation: (helperFunction x) * 2
    """
    return _helper_function(x) * 2
```

### Generated Tests
```python
def test_helper_function_positive():
    assert _helper_function(5) == 6

def test_api_function_matches_idris():
    # Verified against compiled Idris2 output
    assert api_function(5) == 12
```

## Example: Dependent Types

### Idris2 with Dependent Types
```idris
-- Vector with length in type
data Vect : Nat -> Type -> Type where
  Nil  : Vect Z a
  (::) : a -> Vect n a -> Vect (S n) a

-- Safe head: compiler guarantees non-empty
head : Vect (S n) a -> a
head (x :: xs) = x

-- Type-safe append: lengths add up
append : Vect n a -> Vect m a -> Vect (n + m) a
append [] ys = ys
append (x :: xs) ys = x :: append xs ys
```

### Generated Python with Runtime Checks
```python
from typing import TypeVar, Generic, List
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Vect(Generic[T]):
    """Vector with runtime length tracking.

    Idris2 dependent type: Vect : Nat -> Type -> Type
    Runtime invariant: len(data) == length
    """
    length: int
    data: List[T]

    def __post_init__(self):
        assert len(self.data) == self.length, \
            f"Invariant violated: len(data)={len(self.data)} != length={self.length}"

def head(vec: Vect[T]) -> T:
    """Safe head operation.

    Idris2 type: Vect (S n) a -> a
    Precondition: vec.length >= 1 (enforced by dependent type)
    """
    assert vec.length >= 1, \
        "Precondition violation: head requires non-empty vector"
    return vec.data[0]

def append(v1: Vect[T], v2: Vect[T]) -> Vect[T]:
    """Type-safe append.

    Idris2 type: Vect n a -> Vect m a -> Vect (n + m) a
    Postcondition: result.length == v1.length + v2.length
    """
    result = Vect(
        length=v1.length + v2.length,
        data=v1.data + v2.data
    )
    assert result.length == v1.length + v2.length, \
        "Postcondition violation: length arithmetic"
    return result
```

### Generated Tests from Dependent Types
```python
import pytest
from hypothesis import given, strategies as st

def test_head_precondition_empty_rejected():
    """Generated from type: Vect (S n) a -> a
    Tests that empty vectors are rejected."""
    empty = Vect(0, [])
    with pytest.raises(AssertionError, match="non-empty"):
        head(empty)

def test_head_returns_first_element():
    """Generated from type and implementation."""
    vec = Vect(3, [1, 2, 3])
    assert head(vec) == 1

def test_append_length_invariant():
    """Generated from dependent type: Vect (n + m)
    Tests the fundamental type-level property."""
    v1 = Vect(2, [1, 2])
    v2 = Vect(3, [3, 4, 5])
    result = append(v1, v2)
    assert result.length == 5  # 2 + 3

@given(
    n=st.integers(0, 10),
    m=st.integers(0, 10)
)
def test_append_property_based(n, m):
    """Property-based test generated from dependent type.
    Verifies type invariant holds for all valid inputs."""
    v1 = Vect(n, list(range(n)))
    v2 = Vect(m, list(range(m)))
    result = append(v1, v2)
    assert result.length == n + m
    assert len(result.data) == n + m
```

## Project Structure

```
ProgrammingWithIdris2/
├── .claude/
│   ├── project_spec.md          # This file
│   ├── commands/
│   │   ├── idris2-to-python.md  # Slash command for conversion
│   │   └── gen-tests.md         # Slash command for test generation
│   └── examples/                # Reference examples
├── idris2/
│   ├── func.idr                 # Idris2 source files
│   └── ...                      # More Idris2 modules
├── idris2_to_python/
│   ├── func.py                  # Generated Python
│   ├── test_func.py             # Generated tests
│   └── ...
├── build/                       # Idris2 compilation artifacts
└── docs/
    └── conversion_guide.md      # Idris2 → Python patterns
```

## Code Conversion Patterns

### Pattern 1: Simple Functions
```idris
f : Int -> Int
f x = x + 1
```
↓
```python
def f(x: int) -> int:
    return x + 1
```

### Pattern 2: Pattern Matching
```idris
isZero : Nat -> Bool
isZero Z = True
isZero (S k) = False
```
↓
```python
def is_zero(n: int) -> bool:
    assert n >= 0, "is_zero requires Nat (n >= 0)"
    return n == 0
```

### Pattern 3: Maybe/Option Types
```idris
safeDivide : Int -> Int -> Maybe Int
safeDivide x 0 = Nothing
safeDivide x y = Just (div x y)
```
↓
```python
from typing import Optional

def safe_divide(x: int, y: int) -> Optional[int]:
    if y == 0:
        return None
    return x // y
```

### Pattern 4: Dependent Types → Runtime Checks
```idris
-- Type guarantees length >= n
take : (n : Nat) -> Vect (n + m) a -> Vect n a
```
↓
```python
def take(n: int, vec: Vect[T]) -> Vect[T]:
    """
    Idris2: take : (n : Nat) -> Vect (n + m) a -> Vect n a
    Precondition: vec.length >= n (from type (n + m))
    Postcondition: result.length == n
    """
    assert vec.length >= n, \
        f"Precondition: vec.length ({vec.length}) must be >= n ({n})"
    result = Vect(n, vec.data[:n])
    assert result.length == n, "Postcondition: result length"
    return result
```

## Human Expert Role

The human expert with dependent types knowledge is crucial for:

1. **Type Refinement**: Converting imprecise natural language to precise dependent types
2. **Invariant Identification**: Recognizing which properties should be type-level guarantees
3. **Proof Guidance**: Helping AI satisfy type checker requirements
4. **Quality Gate**: Ensuring type specifications truly capture requirements

### Example Expert Intervention

**Initial AI attempt:**
```idris
processUser : User -> String
processUser u = "Hello " ++ u.name
```

**Expert refinement:**
```idris
-- What if user is invalid? Make it explicit!
data ValidUser : Type where
  MkValid : (u : User) -> {auto prf : u.age >= 18} -> ValidUser

processUser : ValidUser -> String
processUser (MkValid u) = "Hello " ++ u.name

validateUser : User -> Maybe ValidUser
validateUser u =
  if u.age >= 18
    then Just (MkValid u)
    else Nothing
```

Now the types guarantee:
- `processUser` only receives valid users
- Validation is explicit and checked
- Python version has clear preconditions

## Benefits Summary

### For AI Code Generation
- ✅ Clear, unambiguous specifications (dependent types)
- ✅ Immediate feedback on errors (compiler)
- ✅ Reduced debugging loops (type-driven)
- ✅ Automatic edge case discovery (type exhaustiveness)

### For Python Code Quality
- ✅ Comprehensive runtime checks (from type constraints)
- ✅ Clear error messages (from precondition violations)
- ✅ Self-documenting (types as documentation)
- ✅ Test coverage (auto-generated from types)

### For Development Process
- ✅ Faster iteration (fewer bugs reach runtime)
- ✅ Higher confidence (type-checked specifications)
- ✅ Better maintainability (declarative Idris2 source)
- ✅ Easier refactoring (compiler guides changes)

## Next Steps

1. **Expand examples**: More complex dependent type patterns
2. **Build converter**: Automated Idris2 → Python translation
3. **Test generator**: Type signature → test suite
4. **VS Code integration**: Seamless workflow in Claude Code
5. **Documentation**: Comprehensive pattern library

## References

- Idris2 Documentation: https://idris2.readthedocs.io/
- Dependent Types Explanation: Types that depend on values
- Property-Based Testing: Hypothesis for Python
