import json
import random
from pathlib import Path

class PatternEngine:
    """Logic to search and generate pattern variants from multiple datasets."""
    def __init__(self, dataset_dir):
        self.patterns = []
        self._load_all_patterns(dataset_dir)

    def _load_all_patterns(self, dataset_dir):
        """Loads all .json files from the dataset directory.
        
        Infers the 'system' field automatically from the filename:
        - premium_patterns.json  →  system = 'premium'
        - standard_patterns.json →  system = 'standard'
        """
        path = Path(dataset_dir)
        if not path.exists():
            return
            
        for json_file in path.glob("*.json"):
            if json_file.name in ("generator_rules.json", "pattern_index.json"):
                continue
            
            # Déduire le système depuis le nom de fichier
            file_system = None
            if "premium" in json_file.stem:
                file_system = "premium"
            elif "standard" in json_file.stem:
                file_system = "standard"
            
            try:
                with open(json_file, encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for pattern in data:
                            # Injecter 'system' si absent
                            if isinstance(pattern, dict) and "system" not in pattern and file_system:
                                pattern["system"] = file_system
                        self.patterns.extend(data)
                    elif isinstance(data, dict):
                        if "system" not in data and file_system:
                            data["system"] = file_system
                        self.patterns.append(data)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

    def search(self, category=None, pattern_id=None):
        """Searches for patterns by category or ID."""
        if pattern_id:
            return [p for p in self.patterns if p.get("id") == pattern_id]
        if category:
            return [p for p in self.patterns if p.get("category") == category]
        return self.patterns

    def random_variant(self, pattern):
        """Generates a random variant of a pattern (e.g. adding hover effects)."""
        variant = json.loads(json.dumps(pattern)) # deep copy
        
        # Simple example enhancement: add a subtle hover effect if it's a card/container
        if "container" in variant.get("tailwind", {}):
            if "hover:" not in variant["tailwind"]["container"]:
                variant["tailwind"]["container"] += " hover:shadow-lg transition-shadow"

        return variant
