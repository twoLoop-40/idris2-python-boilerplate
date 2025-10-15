# Idris2 타입 주도 코드 생성 보일러플레이트

> 의존 타입으로 무한 디버깅 루프 제거하기

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Idris2](https://img.shields.io/badge/Idris2-0.7.0-blue)](https://www.idris-lang.org/)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)

**Idris2 의존 타입 시스템을 활용한 AI 보조 코드 생성을 위한 프로덕션 레디 보일러플레이트**

**한국어** | [English](README.en.md)

## 🎯 문제점

```
자연어 → AI → 코드 → 버그 → 수정 → 새 버그 → 수정 → ... ∞
```

전통적인 AI 코드 생성의 문제:
- ❌ 모호한 명세
- ❌ 컴파일 타임 검증 없음
- ❌ 무한 디버깅 루프
- ❌ 엣지 케이스 누락

## ✨ 우리의 솔루션

```
자연어 → AI → Idris2 (의존 타입) → Python + 테스트
           ↑                      ↓
           └────── 컴파일러 ───────┘
```

**의존 타입을 코드 생성을 위한 명세 언어로 사용합니다.**

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone https://github.com/twoLoop-40/idris2-python-boilerplate.git
cd idris2-python-boilerplate
```

### 2. 의존성 설치

```bash
# Idris2 설치
brew install idris2  # macOS
# 또는: https://idris2.readthedocs.io/

# Python 의존성 설치
pip install -r requirements.txt
```

### 3. 설정 실행

```bash
bash .claude/setup_project.sh
```

### 4. 예제 실행해보기

```bash
# 예제 1: 기본 함수
cd examples/01_basic
idris2 -o func func.idr && ./build/exec/func
python func.py
pytest test_func.py -v

# 예제 2: 의존 타입
cd ../02_dependent_types
idris2 -o safelist SafeList.idr && ./build/exec/safelist
python safe_list.py
pytest test_safe_list.py -v  # 45개 테스트, 모두 통과!
```

## 💡 주요 기능

### 타입 주도 개발

의존 타입으로 명세 작성:

```idris
-- 타입이 비어있지 않음을 보장
safeHead : Vect (S n) a -> a

-- 범위가 제한된 인덱싱 (범위 벗어남 불가능!)
safeIndex : Fin n -> Vect n a -> a

-- 행렬 차원이 타입에 포함됨
matAdd : Matrix r c Int -> Matrix r c Int -> Matrix r c Int
```

### 자동 Python 변환

타입이 런타임 체크로 변환됨:

```python
def safe_head(vec: List[T]) -> T:
    """타입: Vect (S n) a -> a"""
    assert len(vec) >= 1, "비어있지 않은 벡터가 필요합니다"
    return vec[0]

def mat_add(mat1: Matrix, mat2: Matrix) -> Matrix:
    """타입: Matrix r c Int -> Matrix r c Int -> Matrix r c Int"""
    assert mat1.rows == mat2.rows
    assert mat1.cols == mat2.cols
    # ...
```

### 포괄적인 테스트 생성

타입 시그니처 → 테스트 스위트:

```python
# 타입에서: Vect (S n)은 비어있지 않아야 함
@pytest.mark.precondition
def test_safe_head_rejects_empty():
    with pytest.raises(AssertionError):
        safe_head([])

# 타입에서: Vect (n + m) → Vect n
@given(n=st.integers(0, 50), m=st.integers(0, 50))
@pytest.mark.property
def test_length_property(n, m):
    vec = list(range(n + m))
    result = safe_take(n, vec)
    assert len(result) == n
```

## 🎓 예제

### 예제 1: 기본 함수 ([상세보기](examples/01_basic/))

간단한 워크플로우 데모:
- Public/private 함수
- 기본 타입 시그니처
- 자동 생성된 테스트

**적합한 대상:** 입문자

### 예제 2: 의존 타입 ([상세보기](examples/02_dependent_types/))

고급 기능 포함:
- Vect (길이가 인덱싱된 벡터)
- Fin (범위가 제한된 자연수)
- 차원 추적이 있는 행렬 연산
- 45개 자동 생성 테스트 (100% 통과)

**적합한 대상:** 의존 타입의 강력함 이해하기

## 🛠️ 프로젝트에서 사용하기

### 방법 1: 템플릿 전체 복사

```bash
cp -r idris2-python-boilerplate ~/my-project
cd ~/my-project
bash .claude/setup_project.sh
```

### 방법 2: 설정만 복사

```bash
cd /path/to/your/project
cp -r idris2-python-boilerplate/.claude .
bash .claude/setup_project.sh
```

### 커스터마이징

`.claude/project_config.yaml` 편집:

```yaml
project:
  name: "MyProject"

target:
  language: "python"  # 또는 typescript, rust

domain_types:
  UserId:
    python: "uuid.UUID"
  EmailAddress:
    python: "pydantic.EmailStr"
```

## 🔧 워크플로우

### 1. Idris2 명세 작성

```idris
-- src/UserValidation.idr
data ValidUser : Type where
  MkValid : (email : Email)
         -> (age : Nat)
         -> {auto prf : age >= 18}
         -> ValidUser
```

### 2. Python으로 변환 (Claude Code에서)

```
/convert src/UserValidation.idr
```

### 3. 생성된 코드 + 테스트 확인

```python
# generated/python/user_validation.py
@dataclass
class ValidUser:
    email: str
    age: int

    def __post_init__(self):
        assert '@' in self.email
        assert self.age >= 18

# generated/tests/test_user_validation.py
def test_underage_rejected():
    with pytest.raises(AssertionError):
        ValidUser("test@example.com", 17)
```

## 🌟 장점

### AI 코드 생성을 위해
- ✅ 정확하고 명확한 명세
- ✅ 즉각적인 컴파일러 피드백
- ✅ 디버깅 사이클 대폭 감소
- ✅ 엣지 케이스 자동 발견

### 코드 품질을 위해
- ✅ 포괄적인 런타임 체크
- ✅ 자체 문서화 코드
- ✅ 높은 테스트 커버리지 (자동 생성)
- ✅ 증명 가능한 정확성 속성

### 개발을 위해
- ✅ 더 빠른 반복
- ✅ 더 높은 신뢰도
- ✅ 더 쉬운 리팩토링
- ✅ 더 나은 유지보수성

## 📊 실제 영향

**이전 (전통적 AI 생성):**
```
명세 작성 (모호함) → AI가 코드 생성 → 버그 발견
→ AI가 버그 수정 → 새 버그 발생 → AI가 수정 → 원래 버그 재발
→ 10+ 반복 → 여전히 버그 있음
```

**이후 (타입 주도 생성):**
```
Idris2 타입 작성 (정확함) → 컴파일러 검증 → Python + 테스트 생성
→ 테스트 통과 → 1-2 반복만에 완료
```

**디버깅 시간 감소:** ~80%

## 🎯 사용 사례

### ✅ 적합한 경우
- 복잡한 검증이 있는 비즈니스 로직
- 데이터 변환 파이프라인
- 엄격한 계약이 있는 API
- 안전이 중요한 코드
- 레거시 시스템 리팩토링

### ⚠️ 덜 적합한 경우
- 프로토타입/일회용 코드
- 단순한 CRUD 작업
- UI/프레젠테이션 레이어

## 📖 문서

- **[예제 가이드](examples/README.md)** - 작동하는 예제에서 배우기
- **[템플릿 설정](TEMPLATE_USAGE.md)** - 프로젝트에서 이 보일러플레이트 사용하기
- **[전체 명세](.claude/project_spec.md)** - 완전한 방법론
- **[프로젝트 설정](.claude/project_config.yaml)** - 커스터마이징 옵션

## 🤝 기여하기

기여를 환영합니다! 특히:

1. **새로운 예제**
   - Web API 검증
   - 파서 콤비네이터
   - 상태 기계
   - 비즈니스 룰 엔진

2. **타겟 언어**
   - TypeScript 지원
   - Rust 지원
   - Java 지원

3. **문서**
   - 튜토리얼
   - 모범 사례
   - 패턴 라이브러리

자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참조하세요.

## 📚 더 알아보기

- [Idris2 문서](https://idris2.readthedocs.io/)
- [의존 타입 튜토리얼](https://idris2.readthedocs.io/en/latest/tutorial/)
- [Type-Driven Development 책](https://www.manning.com/books/type-driven-development-with-idris)

## 🙏 크레딧

거인의 어깨 위에서 만들어졌습니다:
- [Idris2](https://www.idris-lang.org/)와 의존 타입 커뮤니티
- [Claude Code](https://claude.com/claude-code) AI 보조 개발
- [Hypothesis](https://hypothesis.readthedocs.io/) 속성 기반 테스팅

## 📄 라이센스

MIT License - 자세한 내용은 [LICENSE](LICENSE) 파일 참조

상업적 및 오픈소스 프로젝트에서 자유롭게 사용 가능합니다.

---

**타입 주도 개발을 위해 ❤️ 로 만들어졌습니다**

⭐ 다음 프로젝트를 위해 이 저장소에 Star를 눌러주세요!
