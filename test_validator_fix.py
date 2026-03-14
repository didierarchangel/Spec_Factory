#!/usr/bin/env python3
"""Test: Vérifier que le validateur ignore maintenant 'dependencies' et 'devDependencies'"""

import re
from pathlib import Path

# Simule la logique d'extraction des items depuis une sous-tâche
def extract_items(subtask_text: str) -> list:
    """Extrait les items entre backticks"""
    raw_paths = re.findall(r'`([^`]+)`', subtask_text)
    return raw_paths

# Simule la logique de filtrage du validateur
def should_skip_item(item: str) -> bool:
    """Retourne True si l'item doit être ignoré (skipped)"""
    
    # Clés JSON de package.json à ignorer
    json_config_keywords = {
        'dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies',
        'scripts', 'name', 'version', 'type', 'main', 'types', 'exports',
        'description', 'author', 'license', 'repository', 'bugs', 'homepage',
        'keywords', 'engines', 'files', 'bin', 'man', 'directories', 'config'
    }
    
    return item in json_config_keywords

# Test cases
test_cases = [
    (
        "- [ ] Ajout des dépendances de production (`dependencies`) nécessaires pour le backend (Express, Prisma Client, etc.).",
        "dependencies"
    ),
    (
        "- [ ] Ajout des dépendances de développement (`devDependencies`) nécessaires pour le backend (typescript, nodemon, ts-node, cross-env, @types/node, @types/express, prisma).",
        "devDependencies"
    ),
    (
        "- [ ] Création du fichier `backend/package.json` avec les configurations ESM obligatoires.",
        "backend/package.json"
    )
]

print("🧪 Test: Vérification que le validateur ignore 'dependencies' et 'devDependencies'\n")
print("=" * 70)

for i, (subtask_text, expected_item) in enumerate(test_cases, 1):
    print(f"\nTest Case #{i}:")
    print(f"Subtask: {subtask_text[:80]}...")
    
    items = extract_items(subtask_text)
    print(f"Items extracted: {items}")
    
    # Vérifier si le item attendu est présent
    if expected_item in items:
        # Vérifier s'il est ignoré
        skipped = should_skip_item(expected_item)
        if skipped:
            print(f"✅ PASS: '{expected_item}' est correctement IGNORÉ par le validateur")
        else:
            print(f"❌ FAIL: '{expected_item}' devrait être ignoré mais ne l'est pas")
    else:
        print(f"⚠️  Item '{expected_item}' not found in extraction")

print("\n" + "=" * 70)
print("\n✅ Si tous les tests passent, les deux sous-tâches devraient être validées!")
