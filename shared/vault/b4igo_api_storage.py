"""GraphQL-backed vault storage adapter for B4iGO API integration."""

import os
from typing import Any, Optional
from uuid import uuid4

from shared.vault.storage import VAULT_RECORD_TYPES

# Mutation names per record type
_CREATE_MUTATIONS: dict[str, str] = {
    "doctor": "createFamilyDoctor",
    "insurance": "createHealthInsurance",
    "medication": "createMedicationAndAllergy",
    "medical_history": "createMedicalHistories",
    "education": "createEducation",
    "contact": "createContact",
    "attorney": "createContact",
}

_UPDATE_MUTATIONS: dict[str, str] = {
    "doctor": "updateFamilyDoctor",
    "insurance": "updateHealthInsurance",
    "medication": "updateMedicationAndAllergies",
    "medical_history": "updateMedicalHistory",
}

_DELETE_MUTATIONS: dict[str, str] = {
    "doctor": "deleteDoctorDetails",
    "insurance": "deleteHealthInsurance",
    "medication": "deleteMedicationAllergies",
    "medical_history": "deleteMedicalHistory",
    "education": "deleteEducationById",
    "contact": "deleteContact",
    "attorney": "deleteContact",
}

# Input type names for create mutations
_CREATE_INPUT_TYPES: dict[str, str] = {
    "doctor": "createFamilyDoctorInput",
    "insurance": "CreateHealthInsuranceInput",
    "medication": "createMedicationAndAllergyInput",
    "medical_history": "CreateMedicalHistoriesInput",
    "education": "CreateEducationInput",
    "contact": "CreateContactInput",
    "attorney": "CreateContactInput",
}

# Input type names for update mutations
_UPDATE_INPUT_TYPES: dict[str, str] = {
    "doctor": "UpdateFamilyDoctorInput",
    "insurance": "UpdateHealthInsuranceInput",
    "medication": "UpdateMedicationAndAllergiesInput",
    "medical_history": "UpdateMedicalHistoryInput",
}

# deleteContact does not use the standard DeleteRequest input wrapper.
# It takes direct arguments: id: [Int!]! and userId: String!
_DIRECT_ARG_DELETE_TYPES: frozenset[str] = frozenset({"contact", "attorney"})

_READ_QUERIES: dict[str, str] = {
    "doctor": "getAllDoctors",
    "insurance": "getHealthInsurancesByUserId",
    "medication": "getMedicationsByUserId",
    "medical_history": "getAllMedicalHistory",
    "education": "getEducationByUserId",
    "contact": "getContactByUserId",
    "attorney": "getContactByUserId",
}

# Response array field names per record type
_RESPONSE_ARRAY_FIELD: dict[str, str] = {
    "doctor": "doctor",
    "insurance": "healthInsurances",
    "medication": "data",
    "medical_history": "medicalHistory",
    "education": "education",
    "contact": "contacts",
    "attorney": "contacts",
}

# Doctor create response nests the ID inside a 'data' object as 'doctorId'.
# All other types return 'id' flat on the response.
_NESTED_RESPONSE_ID_FIELD: dict[str, str] = {
    "doctor": "doctorId",
}

# ID field names in returned records per type
_RECORD_ID_FIELD: dict[str, str] = {
    "doctor": "doctorId",
    "insurance": "insuranceId",
    "medication": "medicationId",
    "medical_history": "medicalHistoryId",
    "education": "educationId",
    "contact": "contactId",
    "attorney": "contactId",
}


class B4igoVaultApiStorage:
    """Vault storage implementation backed by the B4iGO GraphQL API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        session: Optional[Any] = None,
    ):
        """Initialize GraphQL API adapter and reusable HTTP session.

        Args:
            base_url: Base URL for the B4iGO API (e.g. https://api.b4igo.com).
            api_key: API key for authentication (Bearer token).
            timeout_seconds: Request timeout in seconds.
            session: Optional requests.Session for dependency injection.
        """
        try:
            import requests as requests_lib
        except ModuleNotFoundError:
            requests_lib = None  # type: ignore[assignment]

        self.base_url = (base_url or os.environ.get("B4IGO_API_BASE_URL") or "").rstrip(
            "/"
        )
        self.api_key = api_key or os.environ.get("B4IGO_API_KEY", "")
        self.timeout_seconds = timeout_seconds or float(
            os.environ.get("B4IGO_API_TIMEOUT_SECS", "10")
        )
        self._graphql_endpoint = os.environ.get("B4IGO_GRAPHQL_ENDPOINT", "/graphql")

        if session is None and requests_lib is None:
            raise RuntimeError(
                "requests must be installed to use B4igoVaultApiStorage "
                "without an injected session"
            )

        self._session = session or requests_lib.Session()
        if self.api_key:
            self._session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        self._session.headers.update({"Content-Type": "application/json"})

    def _request(self, query: str, variables: dict[str, Any]) -> Optional[Any]:
        """Execute a GraphQL request and return the data portion of the response.

        Args:
            query: GraphQL query or mutation string.
            variables: Variables dict to send with the query.

        Returns:
            The 'data' portion of the GraphQL response, or None on error.
        """
        url = f"{self.base_url}{self._graphql_endpoint}" if self.base_url else ""
        headers = {"X-Correlation-ID": str(uuid4())}
        body = {"query": query, "variables": variables}

        try:
            response = self._session.post(
                url,
                json=body,
                headers=headers,
                timeout=self.timeout_seconds,
            )
        except Exception:
            return None

        try:
            json_response = response.json()
        except ValueError:
            return None

        # GraphQL returns errors in 'errors' key, even with HTTP 200
        if "errors" in json_response and json_response["errors"]:
            return None

        return json_response.get("data")

    def _graphql_success(self, data: Optional[Any], mutation_name: str) -> bool:
        """Check if a GraphQL mutation was successful.

        Args:
            data: The 'data' portion of the GraphQL response.
            mutation_name: Name of the mutation to check.

        Returns:
            True if the mutation succeeded, False otherwise.
        """
        if data is None:
            return False
        mutation_result = data.get(mutation_name, {})
        return bool(mutation_result.get("success"))

    def _graphql_id(
        self, data: Optional[Any], mutation_name: str, record_type: str
    ) -> Optional[int]:
        """Extract the record ID from a GraphQL create mutation response.

        Args:
            data: The 'data' portion of the GraphQL response.
            mutation_name: Name of the mutation.
            record_type: Record type (determines nested vs flat ID extraction).

        Returns:
            The record ID, or None if not found or mutation failed.
        """
        if data is None:
            return None
        mutation_result = data.get(mutation_name, {})
        if not mutation_result.get("success"):
            return None
        nested_field = _NESTED_RESPONSE_ID_FIELD.get(record_type)
        if nested_field:
            return (mutation_result.get("data") or {}).get(nested_field)
        return mutation_result.get("id")

    # --- Per-type create variable builders ---

    def _doctor_create_variables(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Doctor schema to CreateFamilyDoctor variables.

        Args:
            username: User ID for the record.
            payload: Doctor schema field dict.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "typeId": 1,
            "doctorName": payload.get("doctor_name", ""),
            "contactInformation": payload.get("location", ""),
        }

    def _insurance_create_variables(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Insurance schema to CreateHealthInsurance variables.

        Args:
            username: User ID for the record.
            payload: Insurance schema field dict.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "memberName": payload.get("type_of_health_insurance", ""),
            "insuranceTypeId": 1,
            "dependents": [],
            "files": [],
        }

    def _medication_create_variables(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Medication schema to CreateMedicationAllergy variables.

        Args:
            username: User ID for the record.
            payload: Medication schema field dict.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "medicineName": payload.get("name_of_medicine", ""),
            "sideEffect": payload.get("side_effect", ""),
            "medicationFiles": [],
        }

    def _medical_history_create_variables(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal MedicalHistory schema to CreateMedicalHistory variables.

        Args:
            username: User ID for the record.
            payload: MedicalHistory schema field dict.

        Returns:
            GraphQL variables dict.
        """
        disease = payload.get("disease", "")
        description = payload.get("description", "")
        general_health = f"{disease} - {description}" if description else disease
        return {
            "userId": username,
            "createdBy": username,
            "userName": username,
            "generalHealth": general_health,
            "age": 0,
            "bloodGroupId": 1,
            "sectionId": 1,
            "responses": [],
        }

    def _education_create_variables(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Education schema to CreateEducation variables.

        Args:
            username: User ID for the record.
            payload: Education schema field dict.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "educationCertificateName": payload.get("degree", ""),
            "nameAsPerCertificate": username,
            "universityOrCollegeName": payload.get("institution", ""),
            "isCurrentlyPursuing": payload.get("is_currently_pursuing", False),
            "createdBy": username,
            "others": "",
            "files": [],
        }

    def _contact_create_variables(
        self, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Map internal Contact or Attorney schema to CreateContact variables.

        contactTypeId is a required list; value 1 is used as the default.
        Fetch valid type IDs via: { getContactType { contacts { contactId contactName } } }

        Args:
            username: User ID for the record.
            payload: Contact or Attorney schema field dict.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "name": payload.get("name", ""),
            "contactTypeId": [1],
            "createdBy": username,
            "relationship": payload.get("relationship", ""),
            "contactNumber": payload.get("phone", ""),
            "emailId": payload.get("email", ""),
        }

    def _create_variables_for_type(
        self, record_type: str, username: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """Build create mutation variables for the given record type.

        Args:
            record_type: One of the supported VAULT_RECORD_TYPES.
            username: User ID for the record.
            payload: Schema field dict.

        Returns:
            GraphQL variables dict.
        """
        builders = {
            "doctor": self._doctor_create_variables,
            "insurance": self._insurance_create_variables,
            "medication": self._medication_create_variables,
            "medical_history": self._medical_history_create_variables,
            "education": self._education_create_variables,
            "contact": self._contact_create_variables,
            "attorney": self._contact_create_variables,
        }
        builder = builders.get(record_type)
        if builder:
            return builder(username, payload)
        return {"userId": username}

    # --- Per-type update variable builders ---

    def _doctor_update_variables(
        self, record_id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map Doctor fields to UpdateFamilyDoctor variables.

        Args:
            record_id: Doctor ID to update.
            payload: Doctor schema field dict.
            username: User ID.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "doctorId": record_id,
            "doctorName": payload.get("doctor_name", ""),
            "contactInformation": payload.get("location", ""),
        }

    def _insurance_update_variables(
        self, record_id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map Insurance fields to UpdateHealthInsurance variables.

        Args:
            record_id: Insurance ID to update.
            payload: Insurance schema field dict.
            username: User ID.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "insuranceId": record_id,
            "insuranceName": payload.get("type_of_health_insurance", ""),
            "policyNumber": "",
            "provider": "",
        }

    def _medication_update_variables(
        self, record_id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map Medication fields to UpdateMedicationAndAllergies variables.

        Args:
            record_id: Medication record ID to update.
            payload: Medication schema field dict.
            username: User ID.

        Returns:
            GraphQL variables dict.
        """
        return {
            "userId": username,
            "recordId": record_id,
            "medication": payload.get("name_of_medicine", ""),
            "allergy": payload.get("side_effect", ""),
        }

    def _medical_history_update_variables(
        self, record_id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Map MedicalHistory fields to UpdateMedicalHistory variables.

        Args:
            record_id: Medical history ID to update.
            payload: MedicalHistory schema field dict.
            username: User ID.

        Returns:
            GraphQL variables dict.
        """
        disease = payload.get("disease", "")
        description = payload.get("description", "")
        history = f"{disease} - {description}" if description else disease
        return {
            "userId": username,
            "historyId": record_id,
            "history": history,
        }

    def _update_variables_for_type(
        self, record_type: str, record_id: int, payload: dict[str, Any], username: str
    ) -> dict[str, Any]:
        """Build update mutation variables for the given record type.

        Args:
            record_type: One of doctor, insurance, medication, medical_history.
            record_id: Record ID to update.
            payload: New field dict.
            username: User ID.

        Returns:
            GraphQL variables dict.
        """
        builders = {
            "doctor": self._doctor_update_variables,
            "insurance": self._insurance_update_variables,
            "medication": self._medication_update_variables,
            "medical_history": self._medical_history_update_variables,
        }
        builder = builders.get(record_type)
        if builder:
            return builder(record_id, payload, username)
        return {"userId": username}

    def _delete_variables_for_type(
        self, record_type: str, record_id: int, username: str
    ) -> dict[str, Any]:
        """Build delete mutation variables for the given record type.

        Args:
            record_type: One of the supported VAULT_RECORD_TYPES.
            record_id: Record ID to delete.
            username: User ID.

        Returns:
            GraphQL variables dict. For DIRECT_ARG_DELETE_TYPES the dict is
            used as top-level variables; for all others it is wrapped in
            {"input": ...} by delete_record.
        """
        if record_type in _DIRECT_ARG_DELETE_TYPES:
            # deleteContact takes id: [Int!]! directly (not via DeleteRequest)
            return {"id": [record_id], "userId": username}
        return {"id": record_id, "userId": username}

    # --- GraphQL mutation/query builders ---

    def _build_create_mutation(self, record_type: str) -> str:
        """Build the GraphQL mutation string for creating a record.

        Args:
            record_type: One of doctor, insurance, medication, medical_history.

        Returns:
            GraphQL mutation string.
        """
        mutation_name = _CREATE_MUTATIONS.get(record_type, "")
        input_type = _CREATE_INPUT_TYPES.get(record_type, "")
        if not mutation_name or not input_type:
            return ""
        nested_field = _NESTED_RESPONSE_ID_FIELD.get(record_type)
        id_selection = f"data {{ {nested_field} }}" if nested_field else "id"
        return f"""
mutation($input: {input_type}!) {{
  {mutation_name}(input: $input) {{
    code
    success
    message
    error
    {id_selection}
  }}
}}
"""

    def _build_update_mutation(self, record_type: str) -> str:
        """Build the GraphQL mutation string for updating a record.

        Args:
            record_type: One of doctor, insurance, medication, medical_history.

        Returns:
            GraphQL mutation string.
        """
        mutation_name = _UPDATE_MUTATIONS.get(record_type, "")
        input_type = _UPDATE_INPUT_TYPES.get(record_type, "")
        if not mutation_name or not input_type:
            return ""
        return f"""
mutation($input: {input_type}!) {{
  {mutation_name}(input: $input) {{
    code
    success
    message
    error
  }}
}}
"""

    def _build_delete_mutation(self, record_type: str) -> str:
        """Build the GraphQL mutation string for deleting a record.

        Args:
            record_type: One of the supported VAULT_RECORD_TYPES.

        Returns:
            GraphQL mutation string.
        """
        mutation_name = _DELETE_MUTATIONS.get(record_type, "")
        if not mutation_name:
            return ""
        if record_type in _DIRECT_ARG_DELETE_TYPES:
            # deleteContact takes direct args, not a DeleteRequest wrapper
            return f"""
mutation($id: [Int!]!, $userId: String!) {{
  {mutation_name}(id: $id, userId: $userId) {{
    code
    success
    message
    error
  }}
}}
"""
        return f"""
mutation($input: DeleteRequest) {{
  {mutation_name}(input: $input) {{
    code
    success
    message
    error
  }}
}}
"""

    def _build_read_query(self, record_type: str) -> str:
        """Build the GraphQL query string for reading records.

        Args:
            record_type: One of doctor, insurance, medication, medical_history.

        Returns:
            GraphQL query string.
        """
        query_name = _READ_QUERIES.get(record_type, "")
        array_field = _RESPONSE_ARRAY_FIELD.get(record_type, "data")
        id_field = _RECORD_ID_FIELD.get(record_type, "id")

        if record_type == "doctor":
            return f"""
query {query_name}($userId: String!) {{
  {query_name}(userId: $userId) {{
    code
    success
    message
    error
    {array_field} {{
      {id_field}
      userId
      doctorName
      contact
    }}
  }}
}}
"""
        elif record_type == "insurance":
            return f"""
query {query_name}($userId: String!) {{
  {query_name}(userId: $userId) {{
    code
    success
    message
    error
    {array_field} {{
      {id_field}
      userId
      insuranceTypeName
      memberId
      groupId
    }}
  }}
}}
"""
        elif record_type == "medication":
            return f"""
query {query_name}($userId: String!) {{
  {query_name}(userId: $userId) {{
    code
    success
    message
    error
    {array_field} {{
      {id_field}
      userId
      medicineName
      purpose
      sideEffect
    }}
  }}
}}
"""
        elif record_type == "medical_history":
            return f"""
query {query_name}($userId: String!) {{
  {query_name}(userId: $userId) {{
    code
    success
    message
    error
    {array_field} {{
      {id_field}
      userId
      recordTypeName
      recordDate
    }}
  }}
}}
"""
        elif record_type == "education":
            return f"""
query {query_name}($userId: String!) {{
  {query_name}(userId: $userId) {{
    code
    success
    message
    error
    {array_field} {{
      {id_field}
      userId
      educationCertificateName
      universityOrCollegeName
      isCurrentlyPursuing
    }}
  }}
}}
"""
        elif record_type in ("contact", "attorney"):
            return f"""
query {query_name}($userId: String!) {{
  {query_name}(userId: $userId) {{
    code
    success
    message
    error
    {array_field} {{
      {id_field}
      userId
      name
      relationship
      contactNumber
      emailId
    }}
  }}
}}
"""
        return ""

    def _normalize_record(
        self,
        raw: dict[str, Any],
        record_type: str,
        fallback_username: str,
    ) -> dict[str, Any]:
        """Normalize a raw GraphQL record to the internal format.

        Args:
            raw: Raw record dict from GraphQL response.
            record_type: Record type for ID field lookup.
            fallback_username: Username to use if not in record.

        Returns:
            Normalized record dict with id, username, record_type, payload.
        """
        id_field = _RECORD_ID_FIELD.get(record_type, "id")
        record_id = raw.get(id_field) or raw.get("id")

        # Build payload based on record type
        if record_type == "doctor":
            payload = {
                "doctor_name": raw.get("doctorName", ""),
                "location": raw.get("contact", ""),
            }
        elif record_type == "insurance":
            payload = {
                "type_of_health_insurance": raw.get("insuranceTypeName", ""),
            }
        elif record_type == "medication":
            payload = {
                "name_of_medicine": raw.get("medicineName", ""),
                "purpose": raw.get("purpose", ""),
                "side_effect": raw.get("sideEffect", ""),
            }
        elif record_type == "medical_history":
            payload = {
                "disease": raw.get("recordTypeName", ""),
                "date": raw.get("recordDate", ""),
            }
        elif record_type == "education":
            payload = {
                "degree": raw.get("educationCertificateName", ""),
                "institution": raw.get("universityOrCollegeName", ""),
                "is_currently_pursuing": raw.get("isCurrentlyPursuing", False),
            }
        elif record_type in ("contact", "attorney"):
            payload = {
                "name": raw.get("name", ""),
                "relationship": raw.get("relationship", ""),
                "phone": raw.get("contactNumber", ""),
                "email": raw.get("emailId", ""),
            }
        else:
            payload = {}

        return {
            "id": record_id,
            "username": raw.get("userId", fallback_username),
            "record_type": record_type,
            "payload": payload,
        }

    # --- Public storage protocol methods ---

    def add_record(
        self, username: str, record_type: str, payload: dict[str, Any]
    ) -> Optional[int]:
        """Create a new vault record via the B4iGO GraphQL API.

        Args:
            username: Owner of the record.
            record_type: One of doctor, insurance, medication, medical_history.
            payload: Schema field dict.

        Returns:
            New record id, or None on failure.
        """
        if record_type not in VAULT_RECORD_TYPES:
            return None

        mutation = self._build_create_mutation(record_type)
        if not mutation:
            return None

        variables = {
            "input": self._create_variables_for_type(record_type, username, payload)
        }
        data = self._request(mutation, variables)

        mutation_name = _CREATE_MUTATIONS.get(record_type, "")
        return self._graphql_id(data, mutation_name, record_type)

    def get_records(
        self,
        username: str,
        record_type: Optional[str] = None,
        id: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Fetch vault records for a user from the B4iGO GraphQL API.

        Args:
            username: Owner to filter by.
            record_type: Optional record type filter.
            id: Optional single record id.

        Returns:
            List of normalized record dicts.
        """
        # If no record_type specified, fetch all types
        if not record_type:
            all_records: list[dict[str, Any]] = []
            for rtype in VAULT_RECORD_TYPES:
                all_records.extend(self.get_records(username, rtype, id))
            return all_records

        if record_type not in VAULT_RECORD_TYPES:
            return []

        query = self._build_read_query(record_type)
        if not query:
            return []

        variables: dict[str, Any] = {"userId": username}
        data = self._request(query, variables)

        if data is None:
            return []

        query_name = _READ_QUERIES.get(record_type, "")
        query_result = data.get(query_name, {})

        if not query_result.get("success"):
            return []

        array_field = _RESPONSE_ARRAY_FIELD.get(record_type, "data")
        raw_list = query_result.get(array_field, [])

        if not isinstance(raw_list, list):
            return []

        records = [
            self._normalize_record(item, record_type, username) for item in raw_list
        ]

        # Filter by id if specified
        if id is not None:
            records = [r for r in records if r.get("id") == id]

        return records

    def update_record(
        self,
        id: int,
        payload: dict[str, Any],
        record_type: str = "",
        username: str = "",
    ) -> bool:
        """Update a vault record via the B4iGO GraphQL API.

        Args:
            id: Record id.
            payload: New field dict.
            record_type: Record type (needed for correct mutation).
            username: Owner username.

        Returns:
            True if successful, False otherwise.
        """
        if not record_type or record_type not in VAULT_RECORD_TYPES:
            return False

        mutation = self._build_update_mutation(record_type)
        if not mutation:
            return False

        variables = {
            "input": self._update_variables_for_type(record_type, id, payload, username)
        }
        data = self._request(mutation, variables)

        mutation_name = _UPDATE_MUTATIONS.get(record_type, "")
        return self._graphql_success(data, mutation_name)

    def delete_record(self, id: int, record_type: str = "", username: str = "") -> bool:
        """Delete a vault record via the B4iGO GraphQL API.

        Args:
            id: Record id.
            record_type: Record type (needed for correct mutation).
            username: Owner username.

        Returns:
            True if successful, False otherwise.
        """
        if not record_type or record_type not in VAULT_RECORD_TYPES:
            return False

        mutation = self._build_delete_mutation(record_type)
        if not mutation:
            return False

        raw_vars = self._delete_variables_for_type(record_type, id, username)
        variables = (
            raw_vars
            if record_type in _DIRECT_ARG_DELETE_TYPES
            else {"input": raw_vars}
        )
        data = self._request(mutation, variables)

        mutation_name = _DELETE_MUTATIONS.get(record_type, "")
        return self._graphql_success(data, mutation_name)
