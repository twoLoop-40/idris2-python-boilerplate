# Type-Driven AI Code Generation Template

> Eliminate infinite debugging loops with dependent types

## Overview

This is a **reusable template** for AI-assisted code generation using Idris2's dependent type system as an intermediate representation.

**The Problem:**
```
Natural Language → AI → Code → Bug → Fix → New Bug → Fix → ... ∞
```

**Our Solution:**
```
Natural Language → AI → Idris2 (Dependent Types) → Target Language + Tests
                   ↑                             ↓
                   └───────── Compiler ──────────┘
```

## Key Innovation

**Use dependent types as a specification language for AI code generation.**

### Why This Works

1. **Precise Specifications**: No ambiguity in types
2. **Compiler Verification**: Catch errors before code generation
3. **Automatic Tests**: Types generate comprehensive test suites
4. **Bug Prevention**: Impossible to express certain bug classes
5. **Language Agnostic**: Convert to any target language

## Quick Start

### 1. Setup New Project

```bash
# Copy this template to your project
cp -r .claude /path/to/your/project/

# Run setup
cd /path/to/your/project
bash .claude/setup_project.sh
```

### 2. Configure

Edit `.claude/project_config.yaml`:

```yaml
project:
  name: "YourProject"

target:
  language: "python"  # or typescript, rust, java

directories:
  source: "src"       # Your Idris2 files
  generated: "generated"
```

### 3. Write Idris2 Code

```idris
-- src/Example.idr
module Example

||| Safe head: type guarantees non-empty
head : Vect (S n) a -> a
head (x :: xs) = x
```

### 4. Convert (in Claude Code)

```
/convert src/Example.idr
```

### 5. Get Generated Code + Tests

```python
# generated/python/example.py
def head(vec: list) -> Any:
    """Type: Vect (S n) a -> a
    Precondition: len(vec) >= 1"""
    assert len(vec) >= 1, "head requires non-empty vector"
    return vec[0]

# generated/tests/test_example.py
def test_head_rejects_empty():
    with pytest.raises(AssertionError):
        head([])  # Type said this is impossible!
```

## Project Structure

```
your-project/
├── .claude/
│   ├── project_spec.md          # Methodology & patterns
│   ├── project_config.yaml      # Your configuration
│   ├── SETUP_TEMPLATE.md        # Setup guide
│   ├── setup_project.sh         # Auto-setup script
│   └── commands/
│       ├── convert.md           # Conversion command
│       ├── gen-tests.md         # Test generation
│       └── verify.md            # Verification
├── src/                         # Idris2 source (.idr)
├── generated/
│   ├── python/                  # Generated Python
│   ├── tests/                   # Generated tests
│   └── docs/                    # Generated docs
└── build/                       # Idris2 build output
```

## Available Commands

Use in Claude Code or command line:

### `/convert [file]`
Convert Idris2 to target language
```
/convert src/MyModule.idr
```

### `/gen-tests [file]`
Generate tests from type signatures
```
/gen-tests src/MyModule.idr
```

### `/verify [file]`
Verify generated code matches Idris2
```
/verify src/MyModule.idr
```

## Workflow

```
1. Requirements (natural language)
   ↓
2. Idris2 Types (AI generates, you refine)
   ↓
3. Compiler Verification (types checked)
   ↓
4. Code Generation (target language + tests)
   ↓
5. Verification (behavior matches)
   ↓
6. Production Ready!
```

## Example: Type-Driven Development

### Requirement
"Validate user email and ensure age >= 18"

### Step 1: AI Generates Idris2 Types
```idris
data ValidUser : Type where
  MkValid : (email : String)
         -> (age : Nat)
         -> {auto prf : age >= 18}
         -> ValidUser

validateUser : String -> Nat -> Maybe ValidUser
validateUser email age =
  if age >= 18 && validEmail email
    then Just (MkValid email age)
    else Nothing
```

### Step 2: You Refine (if needed)
```idris
-- Add email format validation
data Email : Type where
  MkEmail : (addr : String) -> {auto prf : '@' `elem` addr} -> Email

-- More precise validation
data ValidUser : Type where
  MkValid : (email : Email)
         -> (age : Nat)
         -> {auto prf : age >= 18}
         -> ValidUser
```

### Step 3: Convert to Python
```python
@dataclass
class ValidUser:
    """Valid user with compile-time guarantees (now runtime checks)"""
    email: str
    age: int

    def __post_init__(self):
        assert '@' in self.email, "Invalid email format"
        assert self.age >= 18, f"Age must be >= 18, got {self.age}"

def validate_user(email: str, age: int) -> Optional[ValidUser]:
    """Type: String -> Nat -> Maybe ValidUser"""
    try:
        return ValidUser(email, age)
    except AssertionError:
        return None
```

### Step 4: Auto-Generated Tests
```python
def test_validate_user_underage():
    """From type constraint: age >= 18"""
    assert validate_user("test@example.com", 17) is None

def test_validate_user_invalid_email():
    """From type constraint: '@' in email"""
    assert validate_user("invalid-email", 25) is None

def test_validate_user_valid():
    """Happy path"""
    user = validate_user("test@example.com", 25)
    assert user is not None
    assert user.email == "test@example.com"
    assert user.age == 25

@given(
    email=st.emails(),
    age=st.integers(min_value=18, max_value=120)
)
def test_validate_user_property(email, age):
    """Property: valid inputs always succeed"""
    user = validate_user(email, age)
    assert user is not None
```

## Benefits

### For AI Code Generation
- ✅ Clear, unambiguous specifications
- ✅ Immediate compiler feedback
- ✅ Reduced debugging cycles
- ✅ Automatic edge case discovery

### For Code Quality
- ✅ Comprehensive runtime checks
- ✅ Self-documenting code
- ✅ High test coverage
- ✅ Provable correctness properties

### For Development
- ✅ Faster iteration
- ✅ Higher confidence
- ✅ Easier refactoring
- ✅ Better maintainability

## Target Languages

Currently supported conversions:

| Target | Status | Type Features |
|--------|--------|---------------|
| Python | ✅ Stable | Runtime assertions, type hints |
| TypeScript | 🚧 Beta | io-ts runtime types |
| Rust | 🚧 Beta | Const generics, newtype pattern |
| Java | 📋 Planned | Contracts, annotations |

Configure in `.claude/project_config.yaml`:
```yaml
target:
  language: "python"
  additional:
    - "typescript"  # Generate both!
```

## Customization

### Type Mappings
```yaml
# .claude/project_config.yaml
type_mappings:
  UserId:
    python: "uuid.UUID"
    typescript: "string"

domain_types:
  EmailAddress:
    python: "pydantic.EmailStr"
    validation: "validate_email"
```

### Conversion Rules
```yaml
conversion:
  naming:
    case_style: "snake_case"  # or camelCase
  pattern_matching:
    style: "match-case"  # Python 3.10+
```

### Test Generation
```yaml
testing:
  framework: "pytest"
  property_based:
    enabled: true
    max_examples: 100
```

## Real-World Examples

See `examples/` directory for:
- Web API validation
- Matrix operations with dimensions
- Safe array indexing
- Parser combinators
- State machines

## Philosophy: Human-AI-Compiler Triangle

```
      Human Expert
    (Domain Knowledge)
           ↓
     Idris2 Types
    (Specification)
       ↙       ↘
  Compiler    AI
  (Verify)    (Implement)
       ↘       ↙
  Target Code + Tests
```

- **Human**: Translates requirements → precise types
- **Compiler**: Verifies correctness before generation
- **AI**: Generates implementation + comprehensive tests

## Use Cases

### ✅ Great For
- Business logic with complex validation
- Data transformation pipelines
- APIs with strict contracts
- Safety-critical code
- Refactoring legacy systems

### ⚠️ Not Ideal For
- Prototype/throwaway code
- Simple CRUD operations
- UI/presentation layer
- Performance-critical hot paths (without optimization)

## Learn More

- [Full Specification](.claude/project_spec.md)
- [Setup Guide](.claude/SETUP_TEMPLATE.md)
- [Quick Start](QUICKSTART.md)
- [Idris2 Documentation](https://idris2.readthedocs.io/)

## Community & Support

- **Issues**: Report bugs and request features
- **Discussions**: Share patterns and examples
- **Contributing**: PRs welcome!

## Roadmap

- [x] Python code generation
- [x] Property-based test generation
- [x] Runtime assertion generation
- [ ] TypeScript support
- [ ] Rust support
- [ ] Formal proof preservation
- [ ] IDE integration
- [ ] Cloud deployment templates

## FAQ

**Q: Why Idris2 and not Coq/Lean/Agda?**
A: Idris2 is practical, compiles to executables, and has great ergonomics.

**Q: Do I need to know dependent types?**
A: Basic understanding helps, but AI can generate types from descriptions.

**Q: Performance overhead from assertions?**
A: Minimal. Disable in production with `python -O` if needed.

**Q: Can I use existing Idris2 libraries?**
A: Yes! Import and use any Idris2 package.

## License

MIT - Use freely in any project, commercial or open source.

## Credits

Built on the shoulders of giants:
- Idris2 and the dependent types community
- Claude Code and AI-assisted development
- Property-based testing (QuickCheck, Hypothesis)

---

**Status**: Production-ready template
**Version**: 1.0
**Last Updated**: 2025-10-15

⭐ Star this repo to use as a template for your projects!
