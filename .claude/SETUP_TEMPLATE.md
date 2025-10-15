# Idris2 Type-Driven Development Setup Template

This is a reusable template for setting up any Idris2 project with AI-assisted code generation.

## Quick Setup for New Project

1. **Copy `.claude/` directory** to your new project root
2. **Run setup script**:
   ```bash
   bash .claude/setup_project.sh
   ```
3. **Configure** `.claude/project_config.yaml`
4. **Start coding** with type-driven AI assistance!

## Template Structure

```
your-project/
├── .claude/
│   ├── project_spec.md          # Core methodology (customize for your domain)
│   ├── project_config.yaml      # Project-specific settings
│   ├── setup_project.sh         # Initialization script
│   └── commands/
│       ├── convert.md           # Idris2 → target language
│       ├── gen-tests.md         # Auto-generate tests
│       └── verify.md            # Verify conversion
├── src/                         # Idris2 source files (.idr)
├── generated/                   # Generated target language code
│   ├── python/                  # Python output
│   ├── tests/                   # Generated tests
│   └── docs/                    # Generated documentation
├── build/                       # Idris2 compilation artifacts
└── README.md                    # Project documentation
```

## Folder Naming Convention

- `src/` - All Idris2 source code (`.idr` files)
- `generated/` - All AI-generated code from Idris2
  - `generated/python/` - Python conversions
  - `generated/tests/` - Test suites
  - `generated/docs/` - Auto-generated documentation
- `build/` - Idris2 compiler output (gitignore this)

## Customization Points

### 1. Target Language
Default: Python, but can generate any language:
- Python (default)
- TypeScript (with io-ts for runtime types)
- Rust (with dependent types → const generics)
- Java (with contracts)

Edit `.claude/project_config.yaml`:
```yaml
target_language: python  # or typescript, rust, java
```

### 2. Project Domain
Specify your domain in `.claude/project_spec.md` to give context to AI:
```markdown
## Domain: Web Backend Development
## Domain: Data Science
## Domain: Systems Programming
## Domain: Financial Computing
```

### 3. Verification Strategy
Choose verification level:
```yaml
verification:
  compile_idris: true          # Always compile before converting
  run_tests: true              # Auto-run generated tests
  compare_outputs: true        # Compare Idris vs target outputs
  property_based: true         # Generate property-based tests
```

## Usage with Claude Code

Once set up, use in any Idris2 project:

```bash
# Convert a specific file
/convert src/MyModule.idr

# Generate tests for all modules
/gen-tests

# Verify conversion correctness
/verify src/MyModule.idr
```

## Available Commands

### `/convert [file]`
Convert Idris2 to target language with runtime checks

### `/gen-tests [file]`
Generate comprehensive test suite from type signatures

### `/verify [file]`
Verify target code matches Idris2 behavior

### `/new-module <name>`
Create new Idris2 module with template

### `/refine-types <file>`
AI suggests dependent type improvements

## Philosophy

This template embodies **Type-Driven AI Development**:

1. **Specifications First**: Write precise types in Idris2
2. **Compiler as Guard**: Types checked before code generation
3. **Automated Translation**: Types → runtime checks + tests
4. **Human in the Loop**: Expert refines types, AI generates code

## Example Workflow

```
# 1. Create new module
/new-module UserValidation

# 2. AI generates Idris2 type signature from natural language
You: "Validate user email and age >= 18"
AI: Creates src/UserValidation.idr with dependent types

# 3. You refine the types
# Edit src/UserValidation.idr to add precise constraints

# 4. Convert to target language
/convert src/UserValidation.idr

# 5. Tests auto-generated and run
✅ All type constraints verified
```

## Benefits

- ✅ Reusable across all Idris2 projects
- ✅ Consistent workflow and structure
- ✅ Language-agnostic (configure target)
- ✅ Production-ready from day 1
- ✅ Type safety → runtime safety

## Advanced Features

### Custom Conversion Rules

Add project-specific patterns in `.claude/conversion_rules.yaml`:

```yaml
# Map Idris2 types to domain types
type_mappings:
  UserId:
    python: "UUID"
    typescript: "string"

  EmailAddress:
    python: "pydantic.EmailStr"
    typescript: "string & { __brand: 'Email' }"

# Custom runtime checks
runtime_checks:
  EmailAddress:
    python: "validate_email(value)"
    typescript: "isEmail(value)"
```

### Property Extraction

Configure which properties to extract as tests:

```yaml
property_extraction:
  - preconditions: true      # Function preconditions → test
  - postconditions: true     # Return constraints → test
  - invariants: true         # Type invariants → property test
  - totality: true           # Termination → test with timeout
```

## Migration from Existing Project

If you have an existing Idris2 project:

1. Copy `.claude/` into your project
2. Move `.idr` files to `src/`
3. Run `bash .claude/setup_project.sh`
4. Update `.claude/project_config.yaml`
5. Start using `/convert` commands

## Best Practices

### 1. Small, Focused Modules
```idris
-- Good: One responsibility
module UserValidation where

-- Avoid: Kitchen sink module
module Everything where
```

### 2. Explicit Dependent Types
```idris
-- Good: Constraints in type
take : (n : Nat) -> Vect (n + m) a -> Vect n a

-- Avoid: Runtime checks only
take : Nat -> List a -> List a
```

### 3. Document Type Decisions
```idris
||| We use Vect instead of List because:
||| 1. Length is statically known
||| 2. Out-of-bounds errors impossible
||| 3. Converts to clear Python assertions
safeIndex : Fin n -> Vect n a -> a
```

### 4. Test Idris2 First
```bash
# Always verify Idris2 works before converting
idris2 --check src/MyModule.idr
./build/exec/my_program

# Then convert
/convert src/MyModule.idr
```

## Troubleshooting

### "Conversion failed: Type too complex"
- Simplify dependent types
- Split into smaller functions
- Check `.claude/conversion_rules.yaml` for missing mappings

### "Tests failing after conversion"
- Run `/verify` to compare Idris2 vs target output
- Check runtime assertions match type constraints
- Review generated test cases

### "AI generates incorrect Idris2"
- Provide more context in natural language
- Show example type signatures
- Manually refine and let AI learn

## Next Steps

1. Read [full specification](.claude/project_spec.md)
2. Try example conversion: `/convert src/func.idr`
3. Customize for your domain
4. Share your patterns with community!

---

**Template Version**: 1.0
**Last Updated**: 2025-10-15
**License**: MIT - Use freely in any project
