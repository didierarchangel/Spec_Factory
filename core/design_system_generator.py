from __future__ import annotations

from typing import Any, Dict, List


class DesignSystemGenerator:
    """Module Design System Generator : transforme tokens + composants en DS catalogue."""

    def generate(
        self,
        tokens: Dict[str, Any],
        components_manifest: Dict[str, Any],
        style_name: str = "premium-tailwind",
    ) -> Dict[str, Any]:
        ds_components = self._build_components(components_manifest.get("components", []))
        return {
            "style": style_name,
            "tokens": tokens,
            "components": ds_components,
            "rules": self._build_rules(),
            "code": self._build_code_examples(ds_components),
        }

    def _build_components(self, components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        output = []
        for idx, comp in enumerate(components, start=1):
            output.append(
                {
                    "id": f"DS-{idx:02d}",
                    "name": comp.get("name", "Component").title(),
                    "variants": comp.get("variants", ["default"]),
                    "tags": comp.get("tags", []),
                    "props": self._extract_props(comp),
                }
            )
        if not output:
            output.append(
                {
                    "id": "DS-01",
                    "name": "Primary Button",
                    "variants": ["filled", "outline", "ghost"],
                    "tags": ["action", "cta"],
                    "props": {"size": ["sm", "md", "lg"], "status": ["default", "active"]},
                }
            )
        return output

    def _extract_props(self, comp: Dict[str, Any]) -> Dict[str, Any]:
        props = {"size": ["sm", "md", "lg"]}
        variants = comp.get("variants")
        if variants:
            props["variant"] = variants
        return props

    def _build_rules(self) -> List[str]:
        return [
            "Respect padding tokens (spacing.medium) between cards.",
            "Use accent color for CTA states and hover outlines.",
            "Apply radius.card to cards and radius.button to actions.",
        ]

    def _build_code_examples(self, components: List[Dict[str, Any]]) -> Dict[str, str]:
        examples = {}
        for comp in components[:3]:
            name = comp["name"].replace(" ", "")
            examples[name] = f"<div className=\"{comp['tags'][0] if comp['tags'] else 'component'}\">{name}</div>"
        return examples
