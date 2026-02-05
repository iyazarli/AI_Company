#!/usr/bin/env python3
"""
Print to Logger Migration Script
Otomatik olarak print() ifadelerini logger.info() ile değiştirir
"""
import re
import sys
from pathlib import Path

def add_logging_import(content: str) -> str:
    """Dosyaya logging import ekle"""
    # Zaten logging import var mı?
    if 'import logging' in content:
        return content
    
    # İlk import satırından sonra ekle
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            # Import bloğunun sonunu bul
            insert_idx = i
            while insert_idx < len(lines) and (
                lines[insert_idx].startswith('import ') or 
                lines[insert_idx].startswith('from ') or
                lines[insert_idx].strip() == ''
            ):
                insert_idx += 1
            
            # Logging import ve logger ekle
            lines.insert(insert_idx, '')
            lines.insert(insert_idx + 1, 'import logging')
            lines.insert(insert_idx + 2, 'logger = logging.getLogger(__name__)')
            return '\n'.join(lines)
    
    # Import yoksa başa ekle
    return f'import logging\nlogger = logging.getLogger(__name__)\n\n{content}'

def migrate_prints(content: str) -> tuple[str, int]:
    """print() ifadelerini logger'a çevir"""
    count = 0
    
    # logger.info(f"...") -> logger.info(f"...")
    content, n1 = re.subn(
        r'print\((f"[^"]*")\)',
        r'logger.info(\1)',
        content
    )
    count += n1
    
    # logger.info("...") -> logger.info("...")  
    content, n2 = re.subn(
        r'print\(("[\s\S]*?")\)',
        r'logger.info(\1)',
        content
    )
    count += n2
    
    # logger.info('...') -> logger.info('...')
    content, n3 = re.subn(
        r"print\(('[\s\S]*?')\)",
        r"logger.info(\1)",
        content
    )
    count += n3
    
    # logger.info(str(variable)) -> logger.info(str(variable))
    content, n4 = re.subn(
        r'print\(([a-zA-Z_][a-zA-Z0-9_\.]*)\)',
        r'logger.info(str(\1))',
        content
    )
    count += n4
    
    return content, count

def process_file(filepath: Path) -> int:
    """Bir dosyayı işle"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
        
        # print() var mı?
        if 'logger.info(' not in original:
            return 0
        
        # Logging ekle
        content = add_logging_import(original)
        
        # Print'leri migr migrate et
        content, count = migrate_prints(content)
        
        if count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ {filepath}: {count} print() → logger")
            return count
        
        return 0
    
    except Exception as e:
        logger.info(f"❌ {filepath}: {e}")
        return 0

def main():
    """Ana fonksiyon"""
    root = Path('/tmp/workspace')
    total = 0
    
    # Tüm Python dosyalarını bul
    python_files = [
        f for f in root.rglob('*.py')
        if '__pycache__' not in str(f) and 'venv' not in str(f)
    ]
    
    logger.info(f"🔍 {len(python_files)} Python dosyası taranıyor...\n")
    
    for filepath in python_files:
        total += process_file(filepath)
    
    logger.info(f"\n✨ Toplam {total} print() → logger migration tamamlandı!")

if __name__ == '__main__':
    main()
