---
description: Verify target code matches Idris2 behavior
---

Verify that the generated code correctly implements the Idris2 specification by comparing behavior.

## Verification Process

1. **Compile Idris2 code**
   - Build executable from source
   - Verify type checking passes

2. **Run Idris2 with test inputs**
   - Execute compiled program
   - Record outputs

3. **Run target language equivalent**
   - Execute converted code
   - Record outputs

4. **Compare behaviors**
   - Output values must match
   - Error conditions must correspond
   - Type violations → runtime assertion errors

5. **Verify type constraints**
   - Preconditions enforced
   - Postconditions hold
   - Invariants maintained

6. **Generate report**
   - ✅ Matching behaviors
   - ⚠️ Discrepancies found
   - 📊 Coverage analysis

## Usage

```
/verify src/MyModule.idr
```

Or verify all converted modules:
```
/verify
```

## What Gets Checked

### 1. Value Equivalence
Same inputs → same outputs

**Example:**
```
Idris2:  apiFunction 5  →  12
Python:  api_function(5)  →  12  ✅
```

### 2. Error Handling
Type errors → runtime errors

**Example:**
```idris
head : Vect (S n) a -> a  -- Non-empty required
```

```
Idris2:  head []  →  Type error (won't compile)
Python:  head([])  →  AssertionError  ✅
```

### 3. Property Preservation
Type-level properties hold at runtime

**Example:**
```idris
append : Vect n a -> Vect m a -> Vect (n + m) a
```

Verify: `len(result) == len(v1) + len(v2)` always holds

### 4. Totality
Functions terminate (if marked total)

## Test Cases Generated

The verification tool automatically creates:

1. **Happy path tests** - Valid inputs
2. **Boundary tests** - Edge cases (0, empty, max)
3. **Error tests** - Invalid inputs that should fail
4. **Property tests** - Random inputs checking invariants

## Configuration

In `.claude/project_config.yaml`:

```yaml
verification:
  compile_before_convert: true
  compare_outputs: true
  auto_run_tests: true
  verify_assertions: true
```

## Example Output

```
🔍 Verifying: src/Example.idr → generated/python/example.py

Compiling Idris2...
  ✅ Type check passed
  ✅ Compilation successful

Running comparison tests...
  ✅ add(5, 3) → 8 (matches)
  ✅ mult(4, 7) → 28 (matches)
  ✅ safe_div(10, 2) → Just 5 (matches)
  ✅ safe_div(10, 0) → Nothing (matches)

Verifying type constraints...
  ✅ Nat constraint enforced (negative rejected)
  ✅ Division by zero handled correctly
  ✅ Non-empty vector constraint enforced

Running property-based tests...
  ✅ 100/100 random tests passed

Coverage: 98%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ Verification passed!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Common Issues

### Values Don't Match

**Cause**: Conversion bug or semantic difference

**Solution**:
1. Check conversion rules in `.claude/project_config.yaml`
2. Review type mappings
3. Manually inspect generated code

### Type Constraint Not Enforced

**Cause**: Missing runtime assertion

**Solution**:
1. Check `generation.runtime_checks: true`
2. Verify type mapping includes runtime check
3. Add custom assertion in conversion rules

### Tests Timeout

**Cause**: Non-terminating function

**Solution**:
1. Check Idris2 totality
2. Add `total` annotation if possible
3. Adjust timeout in test configuration

## Advanced: Custom Verification

Add custom verification rules in `.claude/project_config.yaml`:

```yaml
verification:
  custom_properties:
    - name: "idempotence"
      check: "f(f(x)) == f(x)"

    - name: "commutativity"
      check: "f(x, y) == f(y, x)"
```

## Integration with CI/CD

```bash
# In your CI pipeline
bash .claude/setup_project.sh
/verify  # Or: python -m claude_verify
pytest generated/tests/ --cov --cov-fail-under=90
```
