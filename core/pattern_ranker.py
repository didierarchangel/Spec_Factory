class PatternRanker:
    """Algorithm to rank UI patterns based on UX, response, and aesthetic scores."""
    def score(self, pattern, constitution_score):
        """Calculates the final score for a pattern."""
        scores = (pattern or {}).get("scores", {}) or {}

        def _safe_score(value, default=0.5):
            try:
                numeric = float(value)
            except Exception:
                return default
            # Clamp to [0, 1] to keep weighted scoring stable.
            return max(0.0, min(1.0, numeric))

        ux = _safe_score(scores.get("ux"))
        resp = _safe_score(scores.get("responsive"))
        aest = _safe_score(scores.get("aesthetic"))
        constitution = _safe_score(constitution_score)

        # weighted average including alignment with design constitution
        score = (
            ux * 0.35
            + resp * 0.25
            + aest * 0.25
            + constitution * 0.15
        )

        return score

    def rank(self, patterns, constitution_score):
        """Ranks a list of patterns and returns the best one."""
        if not patterns:
            return None
            
        scored = []
        for p in patterns:
            s = self.score(p, constitution_score)
            scored.append((s, p))

        # Sort by score descending
        scored.sort(reverse=True, key=lambda x: x[0])

        return scored[0][1]
