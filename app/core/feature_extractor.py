import os
import re
from typing import List, Dict, Any

def extract_features_from_codebase(base_path: str) -> List[Dict[str, Any]]:
    features: List[Dict[str, Any]] = []
    for root, _, files in os.walk(base_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.html'):
                features.extend(_analyze_html(file_path))
            elif file.endswith('.js'):
                features.extend(_analyze_js(file_path))
            elif file.endswith('.py'):
                features.extend(_analyze_python(file_path))
    return features

def _analyze_html(file_path: str) -> List[Dict[str, Any]]:
    feats = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for match in re.finditer(r'<form[^>]*>', content, re.IGNORECASE):
        feats.append({'type': 'form', 'location': file_path, 'snippet': match.group(0)})
    for match in re.finditer(r'<button[^>]*>', content, re.IGNORECASE):
        feats.append({'type': 'button', 'location': file_path, 'snippet': match.group(0)})
    for match in re.finditer(r'<input[^>]*>', content, re.IGNORECASE):
        feats.append({'type': 'input', 'location': file_path, 'snippet': match.group(0)})
    return feats

def _analyze_js(file_path: str) -> List[Dict[str, Any]]:
    feats = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for match in re.finditer(r'fetch\(["\"][^\)]+["\"]\)', content):
        feats.append({'type': 'api_call', 'location': file_path, 'snippet': match.group(0)})
    for match in re.finditer(r'axios\.([a-zA-Z]+)\(["\"][^\)]+["\"]\)', content):
        feats.append({'type': 'api_call', 'location': file_path, 'snippet': match.group(0)})
    return feats

def _analyze_python(file_path: str) -> List[Dict[str, Any]]:
    feats = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for match in re.finditer(r'@app\.route\(["\"][^\)]+["\"]\)', content):
        feats.append({'type': 'route', 'location': file_path, 'snippet': match.group(0)})
    for match in re.finditer(r'@.*\.route\(["\"][^\)]+["\"]\)', content):
        feats.append({'type': 'route', 'location': file_path, 'snippet': match.group(0)})
    for match in re.finditer(r'def ([a-zA-Z_][a-zA-Z0-9_]*)\(', content):
        feats.append({'type': 'function', 'location': file_path, 'snippet': match.group(0)})
    return feats 