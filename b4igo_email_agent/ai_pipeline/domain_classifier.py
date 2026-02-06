"""Defines DomainClassifier of AI Pipeline."""

from typing import Dict, Literal, TypedDict

import numpy as np
from numpy.typing import NDArray
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from b4igo_email_agent.ai_pipeline.email.models import EmailInput

# Email category type
EmailCategory = Literal["education", "medical", "legal", "personal", "other"]


class EmailClassificationResult(TypedDict):
    """Result of email domain classification."""

    category: EmailCategory
    confidence: float
    all_scores: dict[str, float]


class DomainClassifier:
    """Semantic email categorizer using sentence-transformers."""

    def __init__(self):
        """Initialize model, embeddings, and categories."""
        # TODO- Will host model in isolated runtime eventually
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Define category descriptions for semantic matching
        self._categories = {
            "education": (
                "Educational institutions, universities, colleges, schools, "
                "academic courses, degrees, diplomas, certifications, transcripts, "
                "student records, enrollment, tuition, learning platforms, "
                "educational materials, professors, academic advisors"
            ),
            "medical": (
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
                "General correspondence, miscellaneous emails, newsletters, "
                "notifications, automated messages, system alerts, "
                "uncategorized content that doesn't fit specific categories"
            ),
        }
        self._category_embeddings: Dict[str, NDArray] = {}
        self._category_list: list[str] = []
        self._category_matrix: NDArray = np.empty((0, 0))
        self._compute_domain_embeddings()

    def _compute_domain_embeddings(self):
        self._category_list = list(self._categories.keys())
        for category in self._category_list:
            description = self._categories[category]
            self._category_embeddings[category] = np.array(
                self.model.encode(description, convert_to_tensor=False)
            )
        self._category_matrix = np.vstack(
            [self._category_embeddings[category] for category in self._category_list]
        )

    def classify(self, emails: list[EmailInput]) -> list[EmailClassificationResult]:
        """Classify emails into predefined categories using batch processing.

        Args:
            emails (list[EmailMessage]): List of emails with 'subject', 'from',
                and body content.

        Returns:
            list[EmailClassificationResult]: Results with category, confidence,
            and all scores for each email.
        """
        if not emails:
            return []

        email_texts = [email.to_text() for email in emails]
        email_embeddings = np.array(
            self.model.encode(email_texts, convert_to_tensor=False)
        )
        similarity_matrix = cosine_similarity(email_embeddings, self._category_matrix)

        results: list[EmailClassificationResult] = []
        for scores in similarity_matrix:
            similarities = {
                category: float(score)
                for category, score in zip(self._category_list, scores)
            }
            best_index = int(np.argmax(scores))
            results.append(
                EmailClassificationResult(
                    category=self._category_list[best_index],  # type: ignore
                    confidence=float(scores[best_index]),
                    all_scores=similarities,
                )
            )

        return results
