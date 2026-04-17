"""Defines DomainClassifier of AI Pipeline."""

from typing import Dict, Literal, TypedDict

from sentence_transformers import CrossEncoder

Domain = Literal["education", "health", "legal", "personal", "other"]


class ClassificationResult(TypedDict):
    """Result of document domain classification."""

    domain: Domain
    confidence: float
    all_scores: dict[str, float]


class DomainClassifier:
    """Semantic document categorizer using a CrossEncoder."""

    def __init__(self):
        """Initialize model and categories."""
        self.model = CrossEncoder("cross-encoder/nli-MiniLM2-L6-H768")

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
            "other": (
                "General correspondence, miscellaneous content, newsletters, "
                "notifications, automated messages, system alerts, "
                "uncategorized content that doesn't fit specific categories"
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

        return ClassificationResult(
            domain=self._category_list[best_index],  # type: ignore
            confidence=normalised[best_index],
            all_scores=all_scores,
        )
