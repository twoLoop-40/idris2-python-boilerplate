# Examples

These examples demonstrate the type-driven AI code generation workflow.

## 📚 Example Index

### [01_basic](01_basic/) - Basic Functions
**Difficulty:** ⭐ Beginner
**Concepts:** Simple types, public/private, basic conversion

Learn the fundamental workflow:
- Write Idris2 with clear types
- Convert to Python with type hints
- Auto-generate tests

**Best for:** Getting started, understanding the basics

---

### [02_dependent_types](02_dependent_types/) - Dependent Types
**Difficulty:** ⭐⭐⭐ Advanced
**Concepts:** Vect, Fin, type-level arithmetic, dependent types

See the full power:
- Compile-time guarantees → runtime checks
- Type constraints → comprehensive tests
- Matrix operations with dimension tracking

**Best for:** Understanding how dependent types work

---

## 🎯 Learning Path

### Beginner
1. Start with `01_basic/` - understand the workflow
2. Run both Idris2 and Python versions
3. Compare outputs

### Intermediate
1. Study `02_dependent_types/SafeList.idr`
2. Notice how types prevent bugs
3. Read the generated tests
4. Try breaking the code!

### Advanced
1. Create your own example
2. Use dependent types for your domain
3. Generate code and tests
4. Share your patterns!

## 🚀 Running Examples

Each example directory is self-contained:

```bash
cd examples/01_basic/

# Compile Idris2
idris2 -o func func.idr
./build/exec/func

# Run Python
python func.py

# Run tests
pytest test_func.py -v
```

## 📖 What You'll Learn

### From `01_basic/`
- ✅ Basic type-driven workflow
- ✅ Idris2 → Python conversion
- ✅ Simple test generation

### From `02_dependent_types/`
- ✅ Dependent types (Vect, Fin)
- ✅ Type-level constraints
- ✅ Comprehensive test generation
- ✅ Property-based testing
- ✅ Runtime assertion generation

## 💡 Example Template

Want to add your own example? Use this structure:

```
examples/03_your_example/
├── README.md           # Explain what it demonstrates
├── YourModule.idr      # Idris2 source
├── your_module.py      # Generated Python
└── test_your_module.py # Generated tests
```

## 🎓 Additional Resources

- [Idris2 Tutorial](https://idris2.readthedocs.io/en/latest/tutorial/)
- [Dependent Types Explained](https://idris2.readthedocs.io/en/latest/tutorial/typesfuns.html)
- [Main Project README](../README.md)

## 🤝 Contributing Examples

Have a great example? Submit a PR with:
1. Your Idris2 code
2. Generated Python code
3. Tests
4. README explaining the concept

We especially want examples for:
- Web API validation
- Business logic with complex rules
- Data transformation pipelines
- Parser combinators
- State machines
