---
description: Generate tests from Idris2 type signatures
---

Generate comprehensive test suite from Idris2 type signatures:

1. Analyze type signatures for:
   - Preconditions (dependent type constraints)
   - Postconditions (return type guarantees)
   - Edge cases (pattern matching branches)
   - Invariants (type-level properties)

2. Generate test categories:
   - **Precondition tests**: Verify runtime assertions trigger correctly
   - **Happy path tests**: Normal operation with valid inputs
   - **Edge case tests**: Boundary values (0, empty, max)
   - **Property-based tests**: Type invariants hold for all inputs
   - **Integration tests**: Verify matches compiled Idris2 output

3. Use pytest and hypothesis for property-based testing

4. Include test documentation explaining which type constraint each test verifies

If no file specified, generate tests for all Python files in `idris2_to_python/`.
