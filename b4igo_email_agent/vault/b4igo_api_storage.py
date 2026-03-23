"""HTTP-backed vault storage adapter for B4iGO API integration."""

import os
from typing import Any, Optional
from uuid import uuid4

from b4igo_email_agent.vault.storage import VAULT_RECORD_TYPES

# Field name used to extract the newly created record's ID from the API response.
# Most types return "id"; medication returns "medicationId".
_RESPONSE_ID_FIELD: dict[str, str] = {
    "doctor": "id",
    "insurance": "id",
    "medication": "medicationId",
    "medical_history": "id",
}

# Field name used for the record ID in delete/update request bodies, per record type.
_RECORD_ID_FIELD: dict[str, str] = {
    "doctor": "doctorId",
    "insurance": "insuranceId",
    "medication": "recordId",
    "medical_history": "historyId",
}


class B4igoVaultApiStorage:
    """Vault storage implementation backed by the B4iGO API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        session: Optional[Any] = None,
    ):
        """Initialize API adapter and reusable HTTP session."""
        try:
            import requests as requests_lib
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
        except ModuleNotFoundError:
            requests_lib = None  # type: ignore[assignment]
            HTTPAdapter = None  # type: ignore[assignment,misc]
            Retry = None  # type: ignore[assignment,misc]

        self.base_url = (base_url or os.environ.get("B4IGO_API_BASE_URL") or "").rstrip(
            "/"
        )
        self.api_key = api_key or os.environ.get("B4IGO_API_KEY", "")
        self.timeout_seconds = timeout_seconds or float(
            os.environ.get("B4IGO_API_TIMEOUT_SECS", "10")
        )
        self._records_endpoint = os.environ.get(
            "B4IGO_API_RECORDS_ENDPOINT", "/vault/records"
        )
        self._record_type_endpoints = {
            "doctor": os.environ.get("B4IGO_API_DOCTOR_ENDPOINT", ""),
            "insurance": os.environ.get("B4IGO_API_INSURANCE_ENDPOINT", ""),
            "medication": os.environ.get("B4IGO_API_MEDICATION_ENDPOINT", ""),
            "medical_history": os.environ.get("B4IGO_API_MEDICAL_HISTORY_ENDPOINT", ""),
        }

        if session is None and requests_lib is None:
            raise RuntimeError(
                "requests must be installed to use B4igoVaultApiStorage "
                "without an injected session"
            )

        self._session = session or requests_lib.Session()
        if self.api_key:
            self._session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        self._session.headers.update({"Content-Type": "application/json"})

        if Retry is not None and HTTPAdapter is not None:
            retry = Retry(
                total=2,
                backoff_factor=0.2,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=frozenset(["GET", "PUT", "PATCH", "DELETE"]),
            )
            adapter = HTTPAdapter(max_retries=retry)
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)

    def _build_url(self, path: str) -> str:
        if not self.base_url:
            return path
        return f"{self.base_url}{path}"

    def _endpoint_for_type(self, record_type: str) -> str:
        if record_type in VAULT_RECORD_TYPES and self._record_type_endpoints.get(
            record_type
        ):
            return self._record_type_endpoints[record_type]
        return self._records_endpoint

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json_data: Optional[dict[str, Any]] = None,
    ) -> Optional[Any]:
        headers = {"X-Correlation-ID": str(uuid4())}
        try:
            response = self._session.request(
                method=method,
                url=self._build_url(path),
                params=params,
                json=json_data,
                headers=headers,
                timeout=self.timeout_seconds,
            )
        except Exception:
            return None
        return response

    def _safe_json(self, response: Any) -> Any:
        try:
            return response.json()
        except ValueError:
            return {}

    def _normalize_record(
        self, raw: dict[str, Any], fallback_username: str, fallback_type: Optional[str]
    ) -> dict[str, Any]:
        payload = raw.get("payload") or raw.get("data") or {}
        if not isinstance(payload, dict):
            payload = {}
        return {
            "id": raw.get("id"),
            "username": raw.get("username", fallback_username),
            "record_type": raw.get("record_type", fallback_type),
            "payload": payload,
        }

    # --- Per-type create payload builders ---

    def _doctor_create_payload(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Doctor schema to CreateFamilyDoctor API fields."""
        return {
            # TODO: userId may differ from local username; resolve via GetUserId API
            "userId": username,
            "doctorName": payload.get("doctor_name", ""),
            "typeName": payload.get("type") or "General",
            # TODO: resolve typeId via getTypeOfDoctor API; 0 is a placeholder
            "typeId": 0,
            "contactInformation": payload.get("location", ""),
            "city": payload.get("location", ""),
            "stateName": "",
            "countryName": "",
            "markAsImportant": False,
            "createdBy": username,
        }

    def _insurance_create_payload(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Insurance schema to CreateHealthInsurance API fields."""
        return {
            "userId": username,
            "memberName": username,
            "memberId": "",
            "groupId": "",
            # TODO: resolve InsuranceTypeId via getTypeOfHealthInsurance API
            "InsuranceTypeId": 0,
            "othersValue": payload.get("type_of_health_insurance", ""),
            "markAsImportant": False,
            "createdBy": username,
        }

    def _medication_create_payload(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Medication schema to CreateMedicationAllergy API fields."""
        return {
            "userId": username,
            "medicine_name": payload.get("name_of_medicine", ""),
            "purpose": payload.get("purpose", ""),
            "start_date": payload.get("date", ""),
            "markAsImportant": False,
            "createdBy": username,
        }

    def _medical_history_create_payload(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal MedicalHistory schema to CreateMedicalHistory API fields."""
        disease = payload.get("disease", "")
        description = payload.get("description", "")
        history = f"{disease} - {description}" if description else disease
        return {
            "userId": username,
            "history": history,
            "recordDate": payload.get("date", ""),
            "markAsImportant": False,
            "createdBy": username,
        }

    def _create_payload_for_type(
        self, record_type: str, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        builders = {
            "doctor": self._doctor_create_payload,
            "insurance": self._insurance_create_payload,
            "medication": self._medication_create_payload,
            "medical_history": self._medical_history_create_payload,
        }
        builder = builders.get(record_type)
        if builder:
            return builder(username, payload)
        return {"userId": username, **payload}

    # --- Per-type update payload builders ---

    def _doctor_update_payload(
        self, id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map Doctor fields to UpdateFamilyDoctor API body."""
        return {
            "doctorId": id,
            "userId": username,
            "doctorName": payload.get("doctor_name", ""),
            "typeName": payload.get("type") or "General",
            "typeId": 0,
            "contactInformation": payload.get("location", ""),
            "city": payload.get("location", ""),
            "stateName": "",
            "countryName": "",
            "markAsImportant": False,
        }

    def _insurance_update_payload(
        self, id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map Insurance fields to UpdateHealthInsurance API body."""
        return {
            "insuranceId": id,
            "userId": username,
            "insuranceName": payload.get("type_of_health_insurance", ""),
            "InsuranceTypeId": 0,
            "markAsImportant": False,
        }

    def _medication_update_payload(
        self, id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map Medication fields to UpdateMedicationAllergy API body."""
        return {
            "recordId": id,
            "userId": username,
            "medication": payload.get("name_of_medicine", ""),
            "purpose": payload.get("purpose", ""),
            "start_date": payload.get("date", ""),
        }

    def _medical_history_update_payload(
        self, id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map MedicalHistory fields to UpdateMedicalHistory API body."""
        disease = payload.get("disease", "")
        description = payload.get("description", "")
        history = f"{disease} - {description}" if description else disease
        return {
            "historyId": id,
            "userId": username,
            "history": history,
            "recordDate": payload.get("date", ""),
        }

    def _update_payload_for_type(
        self, record_type: str, id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        builders = {
            "doctor": self._doctor_update_payload,
            "insurance": self._insurance_update_payload,
            "medication": self._medication_update_payload,
            "medical_history": self._medical_history_update_payload,
        }
        builder = builders.get(record_type)
        if builder:
            return builder(id, payload, username)
        id_field = _RECORD_ID_FIELD.get(record_type, "id")
        return {id_field: id, "userId": username, **payload}

    def _delete_payload_for_type(
        self, record_type: str, id: int, username: str
    ) -> dict[str, Any]:
        id_field = _RECORD_ID_FIELD.get(record_type, "id")
        return {id_field: id, "userId": username}

    # --- Public storage protocol methods ---

    def add_record(
        self, username: str, record_type: str, payload: dict[str, Any]
    ) -> Optional[int]:
        """Create a new vault record via the B4iGO API.

        Args:
            username: Owner of the record.
            record_type: One of doctor, insurance, medication, medical_history.
            payload: Schema field dict.

        Returns:
            New record id, or None on failure.
        """
        endpoint = self._endpoint_for_type(record_type)
        body = self._create_payload_for_type(record_type, username, payload)
        response = self._request("POST", endpoint, json_data=body)
        if response is None or not (200 <= response.status_code < 300):
            return None
        data = self._safe_json(response)
        id_field = _RESPONSE_ID_FIELD.get(record_type, "id")
        return data.get(id_field)

    def get_records(
        self,
        username: str,
        record_type: Optional[str] = None,
        id: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Fetch vault records for a user from the B4iGO API.

        Args:
            username: Owner to filter by.
            record_type: Optional record type filter.
            id: Optional single record id.

        Returns:
            List of normalized record dicts.
        """
        endpoint = self._endpoint_for_type(record_type or "")
        params: dict[str, Any] = {"userId": username}
        if record_type:
            params["record_type"] = record_type
        if id is not None:
            params["id"] = id
        response = self._request("GET", endpoint, params=params)
        if response is None or not (200 <= response.status_code < 300):
            return []
        data = self._safe_json(response)
        raw_list = data.get("records") or data.get("data") or []
        if not isinstance(raw_list, list):
            return []
        return [
            self._normalize_record(item, username, record_type) for item in raw_list
        ]

    def update_record(
        self,
        id: int,
        payload: dict[str, Any],
        record_type: str = "",
        username: str = "",
    ) -> bool:
        """Update a vault record via the B4iGO API.

        Args:
            id: Record id.
            payload: New field dict.
            record_type: Record type (needed for correct endpoint/body mapping).
            username: Owner username.

        Returns:
            True if successful, False otherwise.
        """
        endpoint = self._endpoint_for_type(record_type)
        body = self._update_payload_for_type(record_type, id, payload, username)
        response = self._request("PUT", endpoint, json_data=body)
        return response is not None and 200 <= response.status_code < 300

    def delete_record(self, id: int, record_type: str = "", username: str = "") -> bool:
        """Delete a vault record via the B4iGO API.

        Args:
            id: Record id.
            record_type: Record type (needed for correct body field name).
            username: Owner username.

        Returns:
            True if successful, False otherwise.
        """
        endpoint = self._endpoint_for_type(record_type)
        body = self._delete_payload_for_type(record_type, id, username)
        response = self._request("DELETE", endpoint, json_data=body)
        return response is not None and 200 <= response.status_code < 300
