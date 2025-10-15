# Contributing to Idris2 Type-Driven Code Generation

Thank you for your interest in contributing! This project aims to make type-driven development accessible and practical.

## 🎯 Ways to Contribute

### 1. Add Examples

We especially need examples demonstrating:
- Web API validation with dependent types
- Parser combinators
- State machines with type-safe transitions
- Business rule engines
- Data transformation pipelines
- Financial calculations with precision types

**Example structure:**
```
examples/XX_your_example/
├── README.md              # What it demonstrates
├── YourModule.idr         # Idris2 source
├── your_module.py         # Generated Python
└── test_your_module.py    # Tests
```

### 2. Improve Documentation

- Tutorials for beginners
- Best practices guide
- Pattern library (common dependent type patterns)
- Video walkthroughs
- Blog posts

### 3. Add Target Language Support

Currently supported: Python

We'd love support for:
- **TypeScript** (with io-ts for runtime types)
- **Rust** (with const generics and newtype pattern)
- **Java** (with contracts and annotations)

### 4. Tooling Improvements

- Better conversion rules
- Enhanced test generation
- IDE integration (VS Code extension)
- CLI tool for conversion

## 📝 Contribution Process

### For Examples

1. **Fork the repository**
   ```bash
   git clone https://github.com/twoLoop-40/idris2-python-boilerplate.git
   cd idris2-python-boilerplate
   ```

2. **Create your example**
   ```bash
   mkdir -p examples/XX_your_example
   # Add your Idris2 code
   # Generate Python and tests
   ```

3. **Verify it works**
   ```bash
   # Test Idris2
   idris2 --check examples/XX_your_example/YourModule.idr
   idris2 -o yourmodule examples/XX_your_example/YourModule.idr
   ./build/exec/yourmodule

   # Test Python
   python examples/XX_your_example/your_module.py
   pytest examples/XX_your_example/test_your_module.py -v
   ```

4. **Write a README**
   - Explain what the example demonstrates
   - Show the key Idris2 types
   - Highlight the generated Python code
   - List all tests and what they verify

5. **Submit a pull request**
   ```bash
   git checkout -b add-example-your-topic
   git add examples/XX_your_example/
   git commit -m "Add example: Your Topic

   Demonstrates:
   - Key concept 1
   - Key concept 2
   - Key concept 3

   Includes:
   - Idris2 source with dependent types
   - Generated Python with runtime checks
   - N auto-generated tests (all passing)
   "
   git push origin add-example-your-topic
   ```

### For Code Changes

1. **Discuss first** - Open an issue to discuss your proposed changes
2. **Follow existing patterns** - Look at current code structure
3. **Add tests** - All code changes should include tests
4. **Update documentation** - Keep docs in sync with code

### For Documentation

1. **Check for accuracy** - Verify all code examples work
2. **Be beginner-friendly** - Explain concepts clearly
3. **Use examples** - Show, don't just tell
4. **Keep it concise** - Respect reader's time

## ✅ Code Quality Standards

### Idris2 Code

```idris
-- ✅ Good: Clear types, documented
||| Safe head function - only works on non-empty vectors
||| Type guarantees: Vector has at least 1 element
safeHead : Vect (S n) a -> a
safeHead (x :: xs) = x

-- ❌ Bad: No documentation, unclear purpose
f : Vect n a -> a
f (x :: _) = x
```

### Python Code

```python
# ✅ Good: Clear assertions, documented
def safe_head(vec: List[T]) -> T:
    """Safe head operation.

    Idris2 type: Vect (S n) a -> a
    Precondition: len(vec) >= 1 (non-empty vector)
    """
    assert len(vec) >= 1, "safe_head requires non-empty vector"
    return vec[0]

# ❌ Bad: Magic numbers, unclear assertions
def f(v):
    assert len(v) > 0
    return v[0]
```

### Tests

```python
# ✅ Good: Clear test names, explain what's being verified
def test_safe_head_rejects_empty():
    """Type constraint: Vect (S n) requires non-empty"""
    with pytest.raises(AssertionError, match="non-empty"):
        safe_head([])

# ❌ Bad: Unclear what's being tested
def test1():
    with pytest.raises(AssertionError):
        safe_head([])
```

## 🐛 Reporting Issues

### Bug Reports

Include:
- **Environment**: OS, Idris2 version, Python version
- **Steps to reproduce**: Minimal example
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Idris2 code**: If applicable
- **Error message**: Full traceback

Example:
```markdown
**Environment:**
- macOS 14.0
- Idris2 0.7.0
- Python 3.11

**Steps:**
1. Create file with...
2. Run conversion...
3. Execute tests...

**Expected:** All tests pass
**Actual:** Test X fails with...

**Idris2 code:**
```idris
safeHead : Vect (S n) a -> a
...
```

**Error:**
```
AssertionError: ...
```
```

### Feature Requests

Include:
- **Use case**: What problem does this solve?
- **Proposed solution**: How would it work?
- **Alternatives**: What else have you considered?
- **Examples**: Show what it would look like

## 💬 Communication

- **Issues**: Bug reports, feature requests
- **Discussions**: Questions, ideas, show & tell
- **Pull Requests**: Code contributions

### Be Respectful

- Assume good intentions
- Be patient with newcomers
- Give constructive feedback
- Celebrate contributions

## 🎓 Learning Resources

Before contributing, you might want to:

1. **Try the examples** - Understand the workflow
2. **Read the documentation** - Especially `.claude/project_spec.md`
3. **Learn Idris2** - https://idris2.readthedocs.io/en/latest/tutorial/
4. **Understand dependent types** - The key concept

## 📋 Checklist for Pull Requests

- [ ] Code follows existing style
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] README updated (if needed)
- [ ] Commit messages are descriptive
- [ ] No merge conflicts

## 🙏 Recognition

All contributors will be:
- Listed in the project's contributors
- Mentioned in release notes (for significant contributions)
- Part of a growing community!

## 📞 Questions?

- Open a [Discussion](https://github.com/twoLoop-40/idris2-python-boilerplate/discussions)
- Tag us on social media
- Join our community chat (if we set one up!)

---

**Thank you for making type-driven development better!** 🎉
