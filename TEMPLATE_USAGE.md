# How to Use This Template for New Projects

This directory is a **reusable template** for type-driven AI code generation with Idris2.

## Copy to New Project

### Option 1: Copy Entire Template

```bash
# Copy this entire directory as a starting point
cp -r /Users/joonho/Idris2Projects/ProgrammingWithIdris2 ~/my-new-project
cd ~/my-new-project

# Clean up existing files
rm -rf build/ generated/python/* generated/tests/* src/func.idr

# Initialize
bash .claude/setup_project.sh
```

### Option 2: Copy Just .claude/ Configuration

```bash
# In your existing Idris2 project
cd /path/to/your/existing/project

# Copy configuration
cp -r /Users/joonho/Idris2Projects/ProgrammingWithIdris2/.claude .

# Run setup
bash .claude/setup_project.sh
```

## Configure for Your Project

### 1. Edit `.claude/project_config.yaml`

```yaml
project:
  name: "YourProjectName"  # ← Change this
  description: "Your project description"

directories:
  source: "src"              # Where your .idr files are
  generated: "generated"     # Where to put generated code

target:
  language: "python"         # or typescript, rust, etc.
```

### 2. Customize Type Mappings (Optional)

Add your domain-specific types:

```yaml
domain_types:
  # Example: User ID type
  UserId:
    python: "uuid.UUID"
    typescript: "string"
    validation: "validate_uuid"

  # Example: Email validation
  EmailAddress:
    python: "pydantic.EmailStr"
    validation: "validate_email_format"
```

### 3. Update README.md

Replace project-specific content:
- Project name and description
- Your use case examples
- Your team/organization info

## Using in Claude Code

Once set up, Claude Code will automatically:

1. **Read `.claude/project_spec.md`** for methodology
2. **Use `.claude/project_config.yaml`** for settings
3. **Provide slash commands**:
   - `/convert` - Convert Idris2 to target language
   - `/gen-tests` - Generate tests from types
   - `/verify` - Verify correctness

## Typical Workflow

### Starting a New Feature

```
# 1. In Claude Code, describe your requirement
"I need a function to validate user passwords with minimum length 8,
must have uppercase, lowercase, and number"

# 2. AI generates Idris2 types
-- Generated in src/Password.idr
data PasswordRequirement = ...
validatePassword : String -> Maybe ValidPassword

# 3. Review and refine the types (you decide!)
-- Add more constraints if needed

# 4. Convert to Python
/convert src/Password.idr

# 5. Tests auto-generated and run
✅ All preconditions tested
✅ Edge cases covered
✅ Property-based tests generated
```

## Folder Structure Reference

```
your-project/
├── .claude/                     ← Configuration & templates
│   ├── project_spec.md          ← Core methodology (customize)
│   ├── project_config.yaml      ← Your settings
│   ├── SETUP_TEMPLATE.md        ← Setup instructions
│   ├── setup_project.sh         ← Auto-setup script
│   └── commands/
│       ├── convert.md           ← /convert command
│       ├── gen-tests.md         ← /gen-tests command
│       └── verify.md            ← /verify command
├── src/                         ← Your Idris2 code (.idr files)
├── generated/
│   ├── python/                  ← Generated Python code
│   ├── tests/                   ← Generated test suites
│   └── docs/                    ← Generated documentation
├── build/                       ← Idris2 compiler output (gitignored)
├── README.md                    ← Project documentation
├── QUICKSTART.md                ← Quick reference (auto-generated)
└── requirements.txt             ← Python dependencies (auto-generated)
```

## Customization Examples

### Example 1: Web API Project

```yaml
# .claude/project_config.yaml
project:
  name: "MyWebAPI"

domain_types:
  UserId:
    python: "uuid.UUID"

  EmailAddress:
    python: "pydantic.EmailStr"

  Timestamp:
    python: "datetime.datetime"
    validation: "isinstance(value, datetime)"

testing:
  generate:
    integration_tests: true  # Test actual HTTP endpoints
```

### Example 2: Data Pipeline

```yaml
project:
  name: "DataPipeline"

target:
  language: "python"
  additional:
    - "typescript"  # Generate both for frontend/backend

type_mappings:
  DataFrame:
    python: "pandas.DataFrame"

  Matrix:
    python: "numpy.ndarray"

verification:
  compare_outputs: true  # Ensure Idris2 and Python give same results
```

### Example 3: Systems Programming

```yaml
project:
  name: "SystemsTools"

target:
  language: "rust"  # Target Rust instead of Python

type_mappings:
  Vect:
    rust: "Vec<T>"
    runtime_check: "assert_eq!(vec.len(), expected_len)"

  Fin:
    rust: "RangedInt<0, N>"  # Using const generics
```

## Best Practices for Using This Template

### 1. ✅ DO: Keep .claude/ Updated

When you discover new patterns or type mappings, add them to:
- `.claude/project_config.yaml` - Type mappings
- `.claude/project_spec.md` - Methodology notes

### 2. ✅ DO: Test Idris2 First

Always verify your Idris2 code compiles before converting:

```bash
idris2 --check src/YourModule.idr
```

### 3. ✅ DO: Review Generated Code

AI-generated code should be reviewed, especially:
- Runtime assertions match your intent
- Edge cases are handled
- Error messages are clear

### 4. ✅ DO: Commit .claude/ to Git

Your team should share the same configuration:

```bash
git add .claude/
git commit -m "Add type-driven development configuration"
```

### 5. ❌ DON'T: Modify Generated Code Directly

If you need changes:
1. Modify the Idris2 source
2. Re-run `/convert`

**Why?** Your changes will be lost on next conversion.

### 6. ❌ DON'T: Ignore Type Errors

If Idris2 won't compile:
- Fix the types (don't hack around it)
- The type error is protecting you from bugs!

## Sharing This Template

### Make It Your Own

1. Fork/copy this template
2. Customize for your domain
3. Add your own conversion patterns
4. Share with your team!

### Contributing Back

Found useful patterns? Share them!
- Type mapping recipes
- Conversion rules
- Domain-specific examples

## Troubleshooting

### "Command /convert not found"

**Solution:** Claude Code reads `.claude/commands/` automatically.
Restart Claude Code or check that files are in the right place.

### "Setup script fails"

**Solution:** Check dependencies:
```bash
which idris2   # Should show path to Idris2
which python3  # Should show Python 3.11+
```

### "Generated code doesn't match Idris2"

**Solution:** Run verification:
```bash
/verify src/YourModule.idr
```

This compares Idris2 vs generated output and shows differences.

## Examples and Demos

See the `examples/` directory (if included) for:
- Simple functions → Python
- Dependent types (Vect, Fin) → Runtime checks
- Web API validation → Pydantic models
- Business logic → Property-based tests

## Getting Help

1. **Check documentation:**
   - [README.md](README.md) - Overview
   - [.claude/project_spec.md](.claude/project_spec.md) - Full spec
   - [QUICKSTART.md](QUICKSTART.md) - Quick reference

2. **In Claude Code:**
   - Ask: "How do I convert Vect types to Python?"
   - Claude reads `.claude/project_spec.md` for context

3. **Community:**
   - Share your patterns
   - Learn from others
   - Contribute improvements

## Next Steps

1. ✅ Copy this template to your project
2. ✅ Run `bash .claude/setup_project.sh`
3. ✅ Customize `.claude/project_config.yaml`
4. ✅ Write your first Idris2 module
5. ✅ Try `/convert` in Claude Code
6. ✅ Review generated code and tests
7. ✅ Iterate and improve!

---

**Template maintained at:** `/Users/joonho/Idris2Projects/ProgrammingWithIdris2`

**License:** MIT - Use freely in any project

**Version:** 1.0
