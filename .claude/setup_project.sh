#!/bin/bash
# Idris2 Type-Driven Development Project Setup
# Run this script to initialize a new project with the template

set -e  # Exit on error

echo "🚀 Setting up Idris2 Type-Driven Development Project..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get project root (parent of .claude directory)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}Project root: $PROJECT_ROOT${NC}"

# Check if Idris2 is installed
echo -e "\n${BLUE}Checking dependencies...${NC}"
if ! command -v idris2 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Idris2 not found. Install with:${NC}"
    echo "  macOS:  brew install idris2"
    echo "  Linux:  See https://idris2.readthedocs.io/"
    exit 1
else
    echo -e "${GREEN}✓ Idris2 found: $(idris2 --version | head -1)${NC}"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  Python 3 not found${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
fi

# Create directory structure
echo -e "\n${BLUE}Creating directory structure...${NC}"

mkdir -p src
mkdir -p generated/python
mkdir -p generated/tests
mkdir -p generated/docs
mkdir -p build

echo -e "${GREEN}✓ Directories created${NC}"

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo -e "\n${BLUE}Creating .gitignore...${NC}"
    cat > .gitignore << 'EOF'
# Idris2 build artifacts
build/
*.ttc
*.ttm
*.ibc

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.pytest_cache/
.coverage
htmlcov/

# Generated code (optional - you might want to commit this)
# generated/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Claude Code cache
.claude/cache/
.claude/conversion.log

# OS
.DS_Store
Thumbs.db
EOF
    echo -e "${GREEN}✓ .gitignore created${NC}"
else
    echo -e "${YELLOW}ℹ️  .gitignore already exists${NC}"
fi

# Create example Idris2 file if src is empty
if [ -z "$(ls -A src 2>/dev/null)" ]; then
    echo -e "\n${BLUE}Creating example Idris2 module...${NC}"
    cat > src/Example.idr << 'EOF'
module Example

-- Simple example functions to demonstrate type-driven development

||| Add two natural numbers
||| Type ensures non-negative inputs and output
add : Nat -> Nat -> Nat
add Z y = y
add (S k) y = S (add k y)

||| Multiply two natural numbers
mult : Nat -> Nat -> Nat
mult Z y = Z
mult (S k) y = add y (mult k y)

||| Safe division returning Maybe
||| Type makes division by zero explicit
safeDiv : Nat -> Nat -> Maybe Nat
safeDiv x Z = Nothing
safeDiv x (S k) = Just (div x (S k))

||| Example with dependent types
||| Takes exactly n elements from a vector
take : (n : Nat) -> Vect (n + m) a -> Vect n a
take Z xs = []
take (S k) (x :: xs) = x :: take k xs

||| Main function for testing
main : IO ()
main = do
  printLn (add 5 3)
  printLn (mult 4 7)
  printLn (safeDiv 10 2)
  printLn (safeDiv 10 0)
EOF
    echo -e "${GREEN}✓ Example module created: src/Example.idr${NC}"
fi

# Create Python requirements.txt
echo -e "\n${BLUE}Creating Python requirements.txt...${NC}"
cat > requirements.txt << 'EOF'
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
hypothesis>=6.82.0

# Type checking
mypy>=1.5.0

# Code formatting
black>=23.7.0
ruff>=0.0.284

# Optional: for domain types
# pydantic>=2.1.0
EOF
echo -e "${GREEN}✓ requirements.txt created${NC}"

# Install Python dependencies
echo -e "\n${BLUE}Installing Python dependencies...${NC}"
if python3 -m pip install -q -r requirements.txt; then
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  Failed to install Python dependencies. Run manually:${NC}"
    echo "  python3 -m pip install -r requirements.txt"
fi

# Create pytest configuration
echo -e "\n${BLUE}Creating pytest.ini...${NC}"
cat > pytest.ini << 'EOF'
[pytest]
testpaths = generated/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Verbose output
addopts =
    -v
    --tb=short
    --strict-markers
    --cov=generated/python
    --cov-report=term-missing
    --cov-report=html

# Markers for different test types
markers =
    precondition: Tests for type preconditions
    postcondition: Tests for type postconditions
    property: Property-based tests
    integration: Integration tests comparing with Idris2
EOF
echo -e "${GREEN}✓ pytest.ini created${NC}"

# Create mypy configuration
echo -e "\n${BLUE}Creating mypy.ini...${NC}"
cat > mypy.ini << 'EOF'
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
strict_optional = True

[mypy-generated.python.*]
# Generated code - less strict
disallow_untyped_defs = False
EOF
echo -e "${GREEN}✓ mypy.ini created${NC}"

# Compile example Idris2 code
if [ -f "src/Example.idr" ]; then
    echo -e "\n${BLUE}Compiling example Idris2 code...${NC}"
    if idris2 --check src/Example.idr; then
        echo -e "${GREEN}✓ Example compiled successfully${NC}"
    else
        echo -e "${YELLOW}⚠️  Example compilation failed (this is normal for first run)${NC}"
    fi
fi

# Create quick reference card
echo -e "\n${BLUE}Creating quick reference...${NC}"
cat > QUICKSTART.md << 'EOF'
# Quick Start Guide

## 🚀 First Steps

1. **Write Idris2 code** in `src/`
   ```bash
   # Edit or create new .idr files
   vim src/MyModule.idr
   ```

2. **Convert to Python** (in Claude Code)
   ```
   /convert src/MyModule.idr
   ```

3. **Run tests**
   ```bash
   pytest generated/tests/
   ```

## 📝 Common Commands (in Claude Code)

- `/convert src/Example.idr` - Convert Idris2 to Python
- `/gen-tests` - Generate tests from types
- `/verify src/Example.idr` - Verify conversion correctness

## 🔧 Manual Tools

```bash
# Compile Idris2
idris2 --check src/MyModule.idr

# Run Idris2 program
idris2 -o myprogram src/MyModule.idr
./build/exec/myprogram

# Format Python
black generated/python/

# Type check Python
mypy generated/python/

# Run tests
pytest generated/tests/ -v
```

## 📚 Workflow

```
Natural Language
    ↓
Write Idris2 types (src/)
    ↓
Compile & verify types
    ↓
Convert to Python (generated/python/)
    ↓
Auto-generate tests (generated/tests/)
    ↓
Run & verify
```

## 🎯 Tips

1. **Start with types**: Define precise types before implementation
2. **Use dependent types**: Leverage Vect, Fin, etc. for guarantees
3. **Test Idris2 first**: Always verify Idris2 works before converting
4. **Review generated code**: Check that assertions match your intent

## 📖 Documentation

- Full spec: `.claude/project_spec.md`
- Configuration: `.claude/project_config.yaml`
- Template guide: `.claude/SETUP_TEMPLATE.md`

## 🆘 Troubleshooting

**Idris2 won't compile:**
- Check syntax with `idris2 --check src/YourFile.idr`
- Look for type errors

**Python conversion failed:**
- Review type complexity
- Check `.claude/project_config.yaml` for type mappings

**Tests failing:**
- Run `/verify` to compare Idris2 vs Python output
- Check that runtime assertions match type constraints
EOF
echo -e "${GREEN}✓ Quick reference created: QUICKSTART.md${NC}"

# Final summary
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ Setup complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${BLUE}Project structure:${NC}"
echo "  src/           - Idris2 source files"
echo "  generated/     - AI-generated code"
echo "  build/         - Idris2 compilation output"
echo "  .claude/       - Configuration and templates"

echo -e "\n${BLUE}Next steps:${NC}"
echo "  1. Review: .claude/project_config.yaml"
echo "  2. Try: /convert src/Example.idr (in Claude Code)"
echo "  3. Read: QUICKSTART.md"

echo -e "\n${BLUE}Example commands:${NC}"
echo -e "  ${YELLOW}# Compile Idris2${NC}"
echo "  idris2 --check src/Example.idr"
echo ""
echo -e "  ${YELLOW}# In Claude Code${NC}"
echo "  /convert src/Example.idr"
echo ""
echo -e "  ${YELLOW}# Run tests${NC}"
echo "  pytest generated/tests/ -v"

echo -e "\n${GREEN}Happy type-driven development! 🎉${NC}\n"
