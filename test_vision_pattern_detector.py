import unittest

from core.vision_pattern_detector import PatternVisionDetector


IMAGE_META_SAMPLE = {
    "dominant_colors": [
        "#3B82F6",
        "#2563EB",
        "#0F172A",
        "#020617",
        "#94A3B8",
        "#10B981",
    ],
    "STYLE": {
        "theme": "dark",
        "effects": {
            "glow": "blue neon",
            "gradients": "blue to cyan",
        },
        "material": {
            "primary": "#3B82F6",
            "secondary": "#2563EB",
            "accent": "#10B981",
            "background_dark": "#020617",
            "surface_dark": "#0F172A",
            "text_primary": "#FFFFFF",
            "text_secondary": "#94A3B8",
        },
    },
}


class _FailingModel:
    def invoke(self, _messages):
        raise RuntimeError("simulated llm outage")


class PatternVisionDetectorTests(unittest.TestCase):
    def test_llm_failure_fallback_keeps_image_meta_palette(self):
        detector = PatternVisionDetector(model=_FailingModel())
        result = detector.analyze(
            "speckit vibe-design : Dark SaaS UI with glassmorphism",
            image_meta=IMAGE_META_SAMPLE,
        )
        colors = result["tokens"]["colors"]

        self.assertEqual(colors["primary"], "#3B82F6")
        self.assertEqual(colors["secondary"], "#2563EB")
        self.assertEqual(colors["accent"], "#10B981")
        self.assertEqual(colors["background"], "#020617")
        self.assertNotIn("gradients", colors)
        self.assertNotIn("glow", colors)

    def test_custom_prompt_without_model_uses_local_extraction(self):
        detector = PatternVisionDetector(model=None)
        result = detector.analyze(
            "speckit vibe-design : premium dark dashboard style",
            image_meta=IMAGE_META_SAMPLE,
        )
        colors = result["tokens"]["colors"]
        self.assertEqual(colors["primary"], "#3B82F6")
        self.assertEqual(colors["accent"], "#10B981")


if __name__ == "__main__":
    unittest.main()
