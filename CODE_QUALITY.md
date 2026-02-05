# 📋 Kod Kalitesi Rehberi

## ✅ En İyi Pratikler

### 1. Logging Kullanımı

```python
# ❌ YANLIŞ
print("User logged in")

# ✅ DOĞRU
import logging
logger = logging.getLogger(__name__)
logger.info("User logged in", extra={'user_id': user.id})
```

### 2. Exception Handling

```python
# ❌ YANLIŞ
try:
    risky_operation()
except:  # Bare except
    pass

# ✅ DOĞRU
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except Exception as e:
    logger.exception("Unexpected error occurred")
    raise
```

### 3. Path Yönetimi

```python
# ❌ YANLIŞ
config_path = "config/settings.yaml"  # Relatif path sorunlu

# ✅ DOĞRU
from pathlib import Path
config_path = Path(__file__).parent / "config" / "settings.yaml"
```

### 4. Type Hints

```python
# ❌ YANLIŞ
def process_data(data):
    return data.get('value')

# ✅ DOĞRU
from typing import Dict, Any, Optional

def process_data(data: Dict[str, Any]) -> Optional[str]:
    return data.get('value')
```

### 5. Environment Variables

```python
# ❌ YANLIŞ
API_KEY = "sk-1234567890"  # Hardcoded

# ✅ DOĞRU
import os
API_KEY = os.getenv('OPENAI_API_KEY')
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not set")
```

### 6. Async/Await

```python
# ❌ YANLIŞ
def slow_operation():
    time.sleep(5)
    return result

# ✅ DOĞRU
async def slow_operation():
    await asyncio.sleep(5)
    return result
```

### 7. Resource Management

```python
# ❌ YANLIŞ
f = open('file.txt')
data = f.read()
f.close()

# ✅ DOĞRU
with open('file.txt') as f:
    data = f.read()
```

### 8. Error Messages

```python
# ❌ YANLIŞ
raise Exception("Error")

# ✅ DOĞRU
raise ValueError(
    f"Invalid configuration: expected 'model' key in {config_path}"
)
```

## 🔧 Kullanım Örnekleri

### Logging Setup

```python
from utils import setup_logging, get_logger

# Uygulama başlangıcında
setup_logging(log_level=logging.INFO)

# Her modülde
logger = get_logger(__name__)
logger.info("Processing started")
```

### Error Handling

```python
from utils import handle_errors, safe_get

@handle_errors(default_return={}, log_errors=True)
def fetch_user_data(user_id: str):
    # Risky operation
    return api.get_user(user_id)

# Safe nested access
name = safe_get(user, 'profile', 'name', default='Unknown')
```

### Performance Monitoring

```python
from utils import timer, PerformanceMonitor

@timer
def expensive_operation():
    # Long running task
    pass

# Or with context manager
with PerformanceMonitor("Database Query"):
    results = db.query()
```

### Config Management

```python
from utils import Config

# Path handling
config_path = Config.get_config_path('company_config.yaml')

# Environment check
if Config.is_streamlit_cloud():
    # Cloud-specific config
    pass
```

## 📊 Kod Kalitesi Metrikleri

### Hedefler

- **Test Coverage:** >80%
- **Cyclomatic Complexity:** <10
- **Function Length:** <50 lines
- **File Length:** <500 lines
- **Type Hints Coverage:** >90%

### Tools

```bash
# Code formatting
black .

# Linting
flake8 .

# Type checking
mypy .

# Security
bandit -r .

# Complexity
radon cc . -a
```

## 🚀 Deployment Checklist

- [ ] Tüm secrets environment variables'da
- [ ] Logging production mode'a set
- [ ] Error handling tüm kritik noktalarda
- [ ] Type hints eklendi
- [ ] Docstrings yazıldı
- [ ] Tests yazıldı
- [ ] Performance optimizasyonu yapıldı
- [ ] Security scan tamamlandı

## 📝 Review Checklist

Kod review yaparken kontrol et:

- [ ] Logging kullanılmış mı?
- [ ] Exception handling uygun mu?
- [ ] Type hints var mı?
- [ ] Docstring yazılmış mı?
- [ ] Path handling güvenli mi?
- [ ] Resource leak riski var mı?
- [ ] Security issue var mı?
- [ ] Performance optimize edilmiş mi?
