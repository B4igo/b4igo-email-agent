"""Defines DomainClassifier of AI Pipeline."""

from typing import Dict, Literal, Optional, TypedDict

from sentence_transformers import CrossEncoder

Domain = Literal["education", "health", "legal", "personal", "other"]


class ClassificationResult(TypedDict):
    """Result of document domain classification."""

    domain: Domain
    confidence: float
    all_scores: dict[str, float]


class DomainClassifier:
    """Semantic document categorizer using a CrossEncoder."""

    DEFAULT_RERANKER = "Qwen/Qwen3-Reranker-0.6B"

    # Minimum softmax-normalised score to accept a non-"other" domain.
    # With 5 categories, pure-random baseline is 0.20. Below this value the
    # classifier is too uncertain to commit to a structured domain, so the
    # result is overridden to "other". Tune based on observed false positives
    # (spam/system emails bleeding into health/legal/personal) vs. false
    # negatives (legitimate structured emails being dropped).
    CONFIDENCE_THRESHOLD: float = 0.35

    def __init__(self, reranker_model: Optional[str] = None):
        """Initialize model and categories."""
        if not reranker_model:
            reranker_model = self.DEFAULT_RERANKER

        self.model = CrossEncoder(
            reranker_model,
            prompts={
                "classification": "Classify whether the document matches the query topic"
            },
            device="cpu",
        )
        # Qwen3-Reranker doesn't define a pad token by default, which breaks
        # batched inference. Fall back to eos_token (standard practice for Qwen).
        tokenizer = self.model.tokenizer
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            # Keep the model config in sync so attention masking works correctly
            self.model.model.config.pad_token_id = tokenizer.pad_token_id

        # Define category descriptions for semantic matching
        self._categories = {
            "education": (
                "Educational institutions, universities, colleges, schools, "
                "academic courses, degrees, diplomas, certifications, transcripts, "
                "student records, enrollment, tuition, learning platforms, "
                "educational materials, professors, academic advisors"
            ),
            "health": (
                "Healthcare providers, doctors, physicians, hospitals, clinics, "
                "medical appointments, prescriptions, medications, health insurance, "
                "lab results, test results, medical records, patient portal, "
                "wellness programs, vaccines, treatments, diagnoses"
            ),
            "legal": (
                "Legal services, attorneys, lawyers, law firms, court documents, "
                "contracts, agreements, property deeds, titles, wills, trusts, "
                "legal notices, compliance, regulatory matters, litigation, "
                "legal counsel, notary, patents, trademarks"
            ),
            "personal": (
                "Personal correspondence, family members, friends, relatives, "
                "personal interests, hobbies, leisure activities, personal projects, "
                "casual communication, catch-ups, personal updates, birthday wishes, "
                "personal invitations, private matters"
            ),
        }
        self._category_list: list[str] = list(self._categories.keys())

    def __call__(self, text: str) -> ClassificationResult:
        """Classify a document into a predefined category.

        Args:
            text (str): Document text to classify.

        Returns:
            ClassificationResult: Result with category, confidence, and all scores.
        """
        pairs = [(text, self._categories[category]) for category in self._category_list]
        raw_scores = self.model.predict(pairs)

        # Normalise raw scores to [0, 1] via softmax so they sum to 1
        exp_scores = [float(__import__("math").exp(s)) for s in raw_scores]
        total = sum(exp_scores)
        normalised = [s / total for s in exp_scores]

        all_scores: Dict[str, float] = dict(zip(self._category_list, normalised))
        best_index = int(max(range(len(normalised)), key=lambda i: normalised[i]))
        best_domain: Domain = self._category_list[best_index]  # type: ignore
        best_confidence = normalised[best_index]

        # Fall back to "other" when confidence is too low to trust the top domain.
        if best_domain != "other" and best_confidence < self.CONFIDENCE_THRESHOLD:
            best_domain = "other"

        return ClassificationResult(
            domain=best_domain,
            confidence=best_confidence,
            all_scores=all_scores,
        )
