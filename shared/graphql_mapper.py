import json
import logging
import os
from typing import Any, Dict, Optional

try:
    import requests
except ImportError:
    requests = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)

# Map AI schema names to GraphQL Mutation Input Types
SCHEMA_TO_INPUT_TYPE = {
    "Doctor": "createFamilyDoctorInput",
    "Insurance": "CreateHealthInsuranceInput",
    "Medication": "createMedicationAndAllergyInput",
    "MedicalHistory": "CreateMedicalHistoryInput",
    "Appointment": "createNotesInput",  # Fallback since no specific match
    "Bill": "createNotesInput",  # Fallback
    "Contact": "CreateContactInput",
    "Attorney": "CreateContactInput",  # Map to contact or note
    "PersonalEvent": "createNotesInput",  # Fallback
    "Reminder": "createNotesInput",  # Fallback
    "Contract": "AddLegalDocumentsInput",
    "CourtDate": "AddLegalDocumentsInput",
    "LegalNotice": "AddLegalDocumentsInput",
}


def _build_doctor_vars(userId: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "userId": userId,
        "typeId": 99,
        "doctorName": payload.get("doctor_name", "Unknown Doctor"),
        "contactInformation": payload.get("location", ""),
        "markAsImportant": False,
    }


def _build_insurance_vars(userId: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "userId": userId,
        "memberName": "Self",
        "insuranceTypeId": 99,
        "dependents": [],
        "files": [],
        "othersValue": payload.get("type_of_health_insurance", ""),
        "markAsImportant": False,
    }


def _build_medication_vars(userId: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "userId": userId,
        "treatmentName": payload.get("treatment_name", ""),
        "purpose": payload.get("purpose", ""),
        "medicineName": payload.get("name_of_medicine", "Unknown Medication"),
        "startDate": payload.get("date", ""),
        "medicationFiles": [],
        "markAsImportant": False,
        "current": True,
    }


def _build_medical_history_vars(userId: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "userId": userId,
        "typeOfRecordId": 99,
        "recordTypeName": payload.get("disease", "Unknown Condition"),
        "recordDate": payload.get("date", ""),
        "files": [],
    }


def _build_contact_vars(userId: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "userId": userId,
        "contactTypeId": [99],
        "name": payload.get("name", "Unknown Contact"),
        "emailId": payload.get("email", ""),
        "contactNumber": payload.get("phone", ""),
        "relationship": payload.get("relationship", "") or payload.get("specialty", ""),
        "companyName": payload.get("firm", ""),
        "Others": payload.get("notes", ""),
    }


def _build_legal_docs_vars(userId: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "userId": userId,
        "documentTypeId": 99,
        "lawyerTypeId": 99,
        "contactIds": [],
        "legalSubject": payload.get("title", "")
        or payload.get("subject", "")
        or payload.get("type", ""),
        "caseNumber": payload.get("case_number", ""),
        "countryId": 99,
        "stateId": 99,
        "files": [],
    }


def _build_notes_vars(
    userId: str, schema_name: str, payload: Dict[str, Any]
) -> Dict[str, Any]:
    note_content = f"[{schema_name}] " + json.dumps(payload, indent=2)
    return {
        "userId": userId,
        "noteContent": note_content,
        "markAsImportant": False,
        "NotesFiles": [],
    }


def map_schema_to_graphql_variables(
    schema_name: str, userId: str, payload: Dict[str, Any]
) -> tuple[str, Dict[str, Any]]:
    """Map an AI schema name and payload to a GraphQL input type and variables.

    Falls back to a generic note (``createNotesInput``) for unknown schemas.
    """
    input_type = SCHEMA_TO_INPUT_TYPE.get(schema_name, "createNotesInput")

    try:
        if input_type == "createFamilyDoctorInput":
            return input_type, _build_doctor_vars(userId, payload)
        elif input_type == "CreateHealthInsuranceInput":
            return input_type, _build_insurance_vars(userId, payload)
        elif input_type == "createMedicationAndAllergyInput":
            return input_type, _build_medication_vars(userId, payload)
        elif input_type == "CreateMedicalHistoryInput":
            return input_type, _build_medical_history_vars(userId, payload)
        elif input_type == "CreateContactInput":
            return input_type, _build_contact_vars(userId, payload)
        elif input_type == "AddLegalDocumentsInput":
            return input_type, _build_legal_docs_vars(userId, payload)
        else:
            return "createNotesInput", _build_notes_vars(userId, schema_name, payload)
    except Exception as e:
        logger.warning(
            f"Error mapping payload to {input_type}, falling back to notes: {e}"
        )
        return "createNotesInput", _build_notes_vars(userId, schema_name, payload)


def _build_mutation_string(input_type: str) -> str:
    # Basic matching from Input type to Mutation name
    mutation_name = input_type.replace("Input", "")
    # AddLegalDocumentsInput maps to addLegalDocuments?
    # Let's just lowercase the first letter.
    if mutation_name.startswith("Add"):
        mutation_name = "a" + mutation_name[1:]
    elif mutation_name.startswith("Create"):
        mutation_name = "c" + mutation_name[1:]

    return f"""
mutation($input: {input_type}!) {{
  {mutation_name}(input: $input) {{
    success
    message
  }}
}}
"""


def execute_graphql_mutation(
    user_id: str, schema_name: str, payload: Dict[str, Any], jwt_token: str
) -> Optional[str]:
    """Execute the appropriate GraphQL mutation for the extracted AI fields.

    Returns an error message string if it failed, or None on success.
    """
    if not requests:
        return "requests module is required"

    base_url = (os.environ.get("B4IGO_API_BASE_URL") or "http://localhost:5000").rstrip(
        "/"
    )

    input_type, variables = map_schema_to_graphql_variables(
        schema_name, user_id, payload
    )
    query = _build_mutation_string(input_type)

    headers = {
        "Content-Type": "application/json",
        "Authorization": (
            jwt_token if jwt_token.startswith("Bearer ") else f"Bearer {jwt_token}"
        ),
    }

    body = {"query": query, "variables": {"input": variables}}

    try:
        response = requests.post(base_url, json=body, headers=headers, timeout=10)
        logger.info(f"GraphQL responded with {response.status_code}: {response.text}")

        if response.status_code != 200:
            return f"HTTP {response.status_code}: {response.text}"

        data = response.json()
        if "errors" in data and data["errors"]:
            return f"GraphQL Errors: {json.dumps(data['errors'])}"

        # Optional: could check data["data"][mutation_name]["success"]
        return None

    except Exception as e:
        logger.error(f"Failed to execute GraphQL mutation: {e}", exc_info=True)
        return str(e)
