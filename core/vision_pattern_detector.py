from __future__ import annotations
import re
import logging
import json
from typing import Any, Dict, List

# --- 0. Configuration des Limites ---
MAX_RETRIES = 3
MAX_DEP_INSTALL_ATTEMPTS = 3  # Limit dependency install loops
MAX_GRAPH_STEPS = 10  # [SAFE] Maximum number of graph routing decisions (prevents infinite cycles)
MAX_DEPENDENCY_CYCLES = 2  # [SAFE] Max cycles in Diagnostics -> TaskEnforcer -> InstallDeps loop

# --- Packages deprecies que le LLM hallucine souvent ---
DEPRECATED_PACKAGES = {
    "@testing-library/react-hooks": "@testing-library/react",  # Deprecie depuis 2020
    "react-test-utils": "@testing-library/react",              # Ancien pattern
    "react-dom/test-utils": "@testing-library/react"           # Ancien pattern
}

class PatternVisionDetector:
    """Module UI Pattern Detector (Vision) : detecte les tokens visuels sans dependance aux emojis."""

    def __init__(self, model: Any = None):
        self.model = model
        self.logger = logging.getLogger(__name__)

    BASE_COLORS = {
        "primary": "#2563eb", "secondary": "#1e293b", "accent": "#6366f1",
        "background": "#f8fafc", "surface": "#ffffff", "success": "#059669",
        "warning": "#d97706", "error": "#dc2626", "on_primary": "#ffffff",
        "on_background": "#0f172a",
    }

    BASE_TYPO = {
        "font_family": "Inter, system-ui, sans-serif",
        "weights": {"regular": 400, "medium": 500, "bold": 700},
        "scale": {"h1": "3rem", "h2": "2.5rem", "body": "1rem"},
    }

    BASE_TOKENS = {
        "radius": {"card": "1.25rem", "button": "1rem", "pill": "999px"},
        "shadow": {"elevated": "0 20px 45px -30px rgba(15, 23, 42, 0.55)"},
        "spacing": {"small": "8px", "medium": "16px", "large": "32px"},
    }

    def analyze(self, prompt: str, image_meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Analyse le prompt pour extraire des tokens de design (Version optimisee)."""
        
        # 1. Nettoyage de la commande CLI 'vibe-design'
        clean_context = prompt
        command_match = re.search(r"vibe-design\s*:\s*['\"]?(.*?)['\"]?$", prompt, re.I | re.S)
        if command_match:
            clean_context = command_match.group(1).strip()

        # 2. Détection du mode de traitement
        keywords = ["design", "style", "modern", "minimalist", "premium", "dark", "light", "glass"]
        is_custom = any(kw in clean_context.lower() for kw in keywords)

        # 3. Extraction de la section de style (recherche de mots-clés au lieu d'émojis)
        extraction_context = clean_context
        if len(clean_context) > 500:
            # On cherche des délimiteurs textuels standardisés
            style_match = re.search(r"(?:DESIGN|VISUAL[_ ]IDENTITY|STYLE).*?(?=CONFIG|STRUCTURE|FONCTION|FUNCTION|$)",
                                    clean_context, re.S | re.I)
            if style_match:
                extraction_context = style_match.group(0).strip()
            else:
                extraction_context = clean_context[:2000]

        # 4. Logique d'extraction
        if is_custom:
            if self.model is None:
                self.logger.warning("Aucun LLM configure. Extraction locale des tokens depuis le prompt/image_meta.")
                tokens = self._extract_custom_tokens(extraction_context, image_meta)
            else:
                self.logger.info("Extraction par Intelligence Artificielle en cours...")
                tokens = self._extract_tokens_with_llm(extraction_context, image_meta=image_meta)
        elif image_meta:
            tokens = self._extract_custom_tokens(extraction_context, image_meta)
        else:
            tokens = {
                "colors": self._build_palette(clean_context, image_meta),
                "typography": self.BASE_TYPO,
                "tokens": self.BASE_TOKENS,
            }

        return {
            "style": "custom" if is_custom else "standard",
            "tokens": tokens,
            "components": self._extract_components(clean_context, image_meta),
            "image_metadata": image_meta or {},
        }

    def _extract_tokens_with_llm(self, prompt: str, image_meta: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Appel LLM sécurisé avec fallback automatique."""
        from langchain_core.messages import HumanMessage
        
        system_prompt = (
            "Extraire les design tokens en JSON pur. "
            "Schéma: {\"colors\": {\"primary\": \"HEX...\"}, \"typography\": {...}, \"tokens\": {\"radius\": {...}}}. "
            "Réponds uniquement en JSON."
        )
        
        try:
            self.logger.info("Calling LLM with prompt...")
            meta_block = f"\n\nimage_meta: {json.dumps(image_meta, ensure_ascii=False)}" if image_meta else ""
            response = self.model.invoke([HumanMessage(content=f"{system_prompt}\n\nTexte: {prompt}{meta_block}")])
            self.logger.info(f"LLM response: {response}")

            # Extraction JSON robuste (evite l'acces .group sur un match potentiellement None)
            response_text = response.content if isinstance(response.content, str) else str(response.content)
            json_match = re.search(r"(\{.*\})", response_text.replace("\n", " "), re.DOTALL)
            if not json_match:
                raise ValueError("No JSON object found in LLM response content.")
            json_str = json_match.group(1)
            return json.loads(json_str)
        except Exception as e:
            self.logger.error(f"Erreur LLM: {e}. Bascule sur l'extraction manuelle.")
            return self._extract_custom_tokens(prompt, image_meta)

    def _extract_custom_tokens(self, text: str, meta: dict | None) -> Dict[str, Any]:
        """Extraction par expressions regulieres (Regex)."""
        palette = self._build_palette(text, meta)
            
        lower_text = text.lower()
        
        # Détection des couleurs Hex
        hex_codes = re.findall(r'#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})', text)
        color_keys = ["primary", "secondary", "accent", "background"]
        for i, code in enumerate(hex_codes[:4]):
            palette[color_keys[i]] = f"#{code}"

        # Détection de thèmes sombres
        if any(w in lower_text for w in ["dark", "sombre", "black", "night"]):
            palette.setdefault("background", "#0f172a")
            palette.setdefault("surface", "#1e293b")
            palette.setdefault("on_background", "#f8fafc")

        return {
            "colors": palette,
            "typography": self.BASE_TYPO,
            "tokens": self.BASE_TOKENS
        }

    def _extract_components(self, text: str, meta: dict | None) -> List[str]:
        comp_list = ["button", "card", "modal", "navbar", "sidebar", "table", "form"]
        found = [c for c in comp_list if c in text.lower()]
        if meta and "detected_components" in meta:
            found.extend(meta["detected_components"])
        return sorted(list(set(found)))

    def _build_palette(self, text: str, meta: dict | None = None) -> Dict[str, str]:
        p = dict(self.BASE_COLORS)
        
        # 1. Inférence basique via le texte et les métadonnées globales
        combined_text = (text + " " + json.dumps(meta) if meta else text).lower()
        
        style = "premium"
        if "material" in combined_text: style = "material"
        elif "fluent" in combined_text: style = "fluent"
        
        styles = {
            "material": {"primary": "#3b82f6", "accent": "#10b981"},
            "fluent": {"primary": "#0ea5e9", "accent": "#22d3ee"},
            "premium": {"primary": "#1d4ed8", "accent": "#8b5cf6"}
        }
        p.update(styles.get(style, {}))
        self.logger.info(f"Palette base set to style {style}: {styles.get(style, {})}")
        
        # 2. Surcharge spécifique depuis image_meta (dominant_colors + STYLE.material)
        meta_palette: Dict[str, str] = {}
        if meta and isinstance(meta, dict):
            dominant = meta.get("dominant_colors")
            if isinstance(dominant, list):
                dominant_slots = ["primary", "secondary", "surface", "background", "on_background", "accent"]
                for slot, color in zip(dominant_slots, dominant):
                    normalized = self._normalize_hex(color)
                    if normalized:
                        meta_palette[slot] = normalized

            style_block = meta.get("STYLE")
            if isinstance(style_block, dict):
                meta_palette.update(self._extract_color_map(style_block))
                material_block = style_block.get("material")
                if isinstance(material_block, dict):
                    meta_palette.update(self._extract_color_map(material_block))

        if meta_palette:
            p.update(meta_palette)
            self.logger.info(f"Palette overridden from image_meta: {meta_palette}")
                    
        return p

    def _extract_color_map(self, data: Dict[str, Any]) -> Dict[str, str]:
        aliases = {
            "background_dark": "background",
            "surface_dark": "surface",
            "text_primary": "on_background",
        }
        allowed_keys = set(self.BASE_COLORS.keys()) | set(aliases.keys())

        colors: Dict[str, str] = {}
        for key, value in data.items():
            if not isinstance(key, str):
                continue
            source_key = key.strip().lower()
            if source_key not in allowed_keys:
                continue

            normalized = self._normalize_hex(value)
            if not normalized:
                continue

            target_key = aliases.get(source_key, source_key)
            colors[target_key] = normalized
        return colors

    def _normalize_hex(self, value: Any) -> str | None:
        if not isinstance(value, str):
            return None
        stripped = value.strip()
        if re.fullmatch(r"#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})", stripped):
            return stripped.upper()
        return None

