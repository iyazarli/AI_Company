#!/usr/bin/env python3
"""
Bare Except Fix Script
except: ifadelerini except Exception: ile değiştirir
"""
import re
from pathlib import Path

def fix_bare_excepts(content: str) -> tuple[str, int]:
    """Bare except ifadelerini düzelt"""
    count = 0
    
    # except:\n -> except Exception as e:\n
    content, n = re.subn(
        r'except:\s*\n',
        'except Exception as e:\n',
        content
    )
    count += n
    
    # except Exception:
            pass -> except Exception: pass
    content, n = re.subn(
        r'except:\s*pass',
        'except Exception:\n            pass',
        content
    )
    count += n
    
    return content, count

def process_file(filepath: Path) -> int:
    """Bir dosyayı işle"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        if 'except:' not in original:
            return 0
        
        content, count = fix_bare_excepts(original)
        
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filepath}: {count} bare except düzeltildi")
            return count
        
        return 0
    
    except Exception as e:
        print(f"❌ {filepath}: {e}")
        return 0

def main():
    """Ana fonksiyon"""
    root = Path('/tmp/workspace')
    total = 0
    
    python_files = [
        f for f in root.rglob('*.py')
        if '__pycache__' not in str(f)
    ]
    
    print(f"🔍 {len(python_files)} Python dosyası taranıyor...\n")
    
    for filepath in python_files:
        total += process_file(filepath)
    
    print(f"\n✨ Toplam {total} bare except düzeltildi!")

if __name__ == '__main__':
    main()
