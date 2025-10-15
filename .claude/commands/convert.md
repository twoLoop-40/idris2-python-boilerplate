---
description: Convert Idris2 code to target language with runtime checks
---

Convert Idris2 source code to the target language (configured in `.claude/project_config.yaml`).

## Conversion Process

1. **Read Idris2 source** from `src/` directory
2. **Compile Idris2** to verify type correctness
3. **Generate target language code** with:
   - Type signatures → Type hints/annotations
   - Dependent type constraints → Runtime assertions
   - Pattern matching → Conditional logic
   - Private/public visibility → Naming conventions
   - Docstrings explaining original Idris2 types
4. **Save to `generated/{language}/`**
5. **Auto-generate tests** in `generated/tests/`
6. **Format and lint** generated code
7. **Show conversion summary**

## Usage

```
/convert src/MyModule.idr
```

Or convert all files:
```
/convert
```

## Configuration

Edit `.claude/project_config.yaml` to customize:

```yaml
target:
  language: python  # or typescript, rust, java

generation:
  runtime_checks: true
  documentation: true
  preserve_types: true
```

## Conversion Examples

### Basic Functions
```idris
add : Nat -> Nat -> Nat
add Z y = y
add (S k) y = S (add k y)
```
↓
```python
def add(x: int, y: int) -> int:
    """Type: Nat -> Nat -> Nat"""
    assert x >= 0 and y >= 0, "add requires Nat (non-negative)"
    if x == 0:
        return y
    else:
        return 1 + add(x - 1, y)
```

### Dependent Types
```idris
head : Vect (S n) a -> a
head (x :: xs) = x
```
↓
```python
def head(vec: list) -> Any:
    """
    Type: Vect (S n) a -> a
    Precondition: len(vec) >= 1 (non-empty vector)
    """
    assert len(vec) >= 1, "head requires non-empty vector"
    return vec[0]
```

### Maybe Types
```idris
safeDiv : Int -> Int -> Maybe Int
safeDiv x Z = Nothing
safeDiv x y = Just (div x y)
```
↓
```python
def safe_div(x: int, y: int) -> Optional[int]:
    """Type: Int -> Int -> Maybe Int"""
    if y == 0:
        return None
    return x // y
```

## What Gets Generated

For each Idris2 module `src/MyModule.idr`:

1. **`generated/python/my_module.py`** - Converted code
2. **`generated/tests/test_my_module.py`** - Test suite
3. **`generated/docs/my_module.md`** - Documentation (optional)

## Verification

After conversion, the tool:
- ✅ Compiles target code
- ✅ Runs type checker
- ✅ Executes generated tests
- ✅ Compares outputs with Idris2 (if enabled)

## Troubleshooting

**"Unsupported type"**: Add mapping in `.claude/project_config.yaml`

**"Conversion failed"**: Check Idris2 compiles first:
```bash
idris2 --check src/MyModule.idr
```

**"Tests failing"**: Use `/verify` to debug differences
