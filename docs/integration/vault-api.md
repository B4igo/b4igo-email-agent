# B4iGO Vault API — Integration Reference

Focused reference for the B4iGO API endpoints used by `B4igoVaultApiStorage`.
Source: `docs/integration/API.md` (Health Microservice sections).

> **Note:** The full `API.md` does not include endpoint URLs — only operation names
> and field schemas. Actual URLs must be configured via environment variables (see
> [Backend selection](#backend-selection)).

---

## Backend Selection

Set environment variables to switch vault backends:

| Variable | Default | Description |
|---|---|---|
| `B4IGO_VAULT_BACKEND` | `sqlite` | Set to `api` to use B4iGO API |
| `B4IGO_API_BASE_URL` | — | Base URL for all API requests |
| `B4IGO_API_KEY` | — | Bearer token sent as `Authorization` header |
| `B4IGO_API_TIMEOUT_SECS` | `10` | Request timeout in seconds |

### Per-type endpoint overrides

If the API uses separate URLs per record type, set these:

| Variable | Fallback |
|---|---|
| `B4IGO_API_DOCTOR_ENDPOINT` | `B4IGO_API_RECORDS_ENDPOINT` |
| `B4IGO_API_INSURANCE_ENDPOINT` | `B4IGO_API_RECORDS_ENDPOINT` |
| `B4IGO_API_MEDICATION_ENDPOINT` | `B4IGO_API_RECORDS_ENDPOINT` |
| `B4IGO_API_MEDICAL_HISTORY_ENDPOINT` | `B4IGO_API_RECORDS_ENDPOINT` |
| `B4IGO_API_RECORDS_ENDPOINT` | `/vault/records` |

---

## Common Patterns

- All requests include an `X-Correlation-ID` UUID header for traceability.
- All responses include `code` (Int), `success` (Bool), `message` (String), `error` (String).
- `success: true` + HTTP 2xx = success. The created record's ID is returned in the response.
- Response ID field varies by type: `id` for doctor/insurance/medical_history, `medicationId` for medication.

---

## Health Vault

### Doctor (`record_type: "doctor"`)

#### Create — `CreateFamilyDoctor`

**Request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | Maps from `username` |
| `typeId` | Int | ✅ | Doctor type ID — **TODO: resolve via `getTypeOfDoctor` API; currently hardcoded 0** |
| `typeName` | String | ✅ | e.g. "General", "Cardiologist". Maps from `Doctor.type` |
| `doctorName` | String | ✅ | Maps from `Doctor.doctor_name` |
| `contactInformation` | String | ✅ | Maps from `Doctor.location` |
| `city` | String | ✅ | Maps from `Doctor.location` (same field, no separate city) |
| `stateName` | String | ✅ | Not in schema — sent as `""` |
| `countryName` | String | ✅ | Not in schema — sent as `""` |
| `createdBy` | String | ✅ | Same as `userId` |
| `markAsImportant` | Boolean | ✅ | Hardcoded `false` |

**Response — key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | Int | New record ID (`_RESPONSE_ID_FIELD["doctor"] = "id"`) |
| `doctorId` | Int | Returned in read responses (GetAllDoctors uses `doctorId`) |

#### Read — `GetAllDoctors`

**Request params:** `userId` (String)

**Response — doctor object fields:**

| Field | Type |
|---|---|
| `doctorId` | Int |
| `userId` | String |
| `typeId` | Int |
| `typeName` | String |
| `doctorName` | String |
| `contactInformation` | String |
| `city` | String |
| `state` | String |
| `country` | String |
| `markAsImportant` | Boolean |
| `createdAt` | String |
| `updatedAt` | String |
| `recordIdentifier` | String |

#### Update — `UpdateFamilyDoctor`

**Request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | |
| `doctorId` | Int | ✅ | `_RECORD_ID_FIELD["doctor"] = "doctorId"` |
| `doctorName` | String | ✅ | Maps from `Doctor.doctor_name` |
| `typeName` | String | | Maps from `Doctor.type` |
| `typeId` | Int | | Hardcoded 0 |
| `contactInformation` | String | | Maps from `Doctor.location` |
| `city` | String | | Maps from `Doctor.location` |
| `stateName` | String | | Sent as `""` |
| `countryName` | String | | Sent as `""` |
| `markAsImportant` | Boolean | | Hardcoded `false` |

#### Delete — `DeleteDoctorDetails`

**Request body:**

| Field | Type | Required |
|---|---|---|
| `userId` | String | ✅ |
| `doctorId` | Int | ✅ |

---

### Insurance (`record_type: "insurance"`)

#### Create — `CreateHealthInsurance`

**Request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | Maps from `username` |
| `memberName` | String | ✅ | Hardcoded to `username` (no member name in schema) |
| `memberId` | String | ✅ | Not in schema — sent as `""` |
| `groupId` | String | ✅ | Not in schema — sent as `""` |
| `InsuranceTypeId` | Int | | **TODO: resolve via `getTypeOfHealthInsurance` API; currently hardcoded 0** |
| `othersValue` | String | | Maps from `Insurance.type_of_health_insurance` |
| `createdBy` | String | | Same as `userId` |
| `markAsImportant` | Boolean | ✅ | Hardcoded `false` |
| `dependents` | [String] | | Not in schema — omitted |
| `healthDependents` | [Object] | | Not in schema — omitted |

**Response — key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | Int | New record ID (`_RESPONSE_ID_FIELD["insurance"] = "id"`) |

#### Read

No dedicated GetAllInsurance endpoint documented. Uses generic records endpoint with `userId` + `record_type=insurance` params.

#### Update — `UpdateHealthInsurance`

**Request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | |
| `insuranceId` | Int | ✅ | `_RECORD_ID_FIELD["insurance"] = "insuranceId"` |
| `insuranceName` | String | | Maps from `Insurance.type_of_health_insurance` |
| `policyNumber` | String | | Not in schema — omitted |
| `provider` | String | | Not in schema — omitted |
| `InsuranceTypeId` | Int | | Hardcoded 0 |
| `markAsImportant` | Boolean | | Hardcoded `false` |

#### Delete — `DeleteHealthInsurance`

**Request body:**

| Field | Type | Required |
|---|---|---|
| `userId` | String | ✅ |
| `insuranceId` | Int | ✅ |

---

### Medication (`record_type: "medication"`)

#### Create — `CreateMedicationAllergy`

**Request body (full schema from API.md):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | Maps from `username` |
| `medicine_name` | String | ✅ | Maps from `Medication.name_of_medicine` |
| `treatment_name` | Int | ✅ | Not in schema — **currently omitted (TODO)** |
| `purpose` | String | ✅ | Maps from `Medication.purpose` |
| `dosage` | String | ✅ | Not in schema — **currently omitted (TODO)** |
| `start_date` | String | ✅ | Maps from `Medication.date` |
| `end_date` | String | ✅ | Not in schema — **currently omitted (TODO)** |
| `frequency_dosage` | String | ✅ | Not in schema — **currently omitted (TODO)** |
| `side_effect` | String | ✅ | Not in schema — **currently omitted (TODO)** |
| `markAsImportant` | Boolean | ✅ | Hardcoded `false` |
| `files` | [File] | ✅ | Not used — **currently omitted** |

**Response — key fields:**

| Field | Type | Notes |
|---|---|---|
| `medicationId` | Int | New record ID (`_RESPONSE_ID_FIELD["medication"] = "medicationId"`) |
| `recordId` | String | UUID for traceability |

#### Update — `UpdateMedicationAndAllergies`

**Request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | |
| `recordId` | Int | ✅ | `_RECORD_ID_FIELD["medication"] = "recordId"` |
| `medication` | String | | Maps from `Medication.name_of_medicine` |
| `purpose` | String | | Maps from `Medication.purpose` |
| `start_date` | String | | Maps from `Medication.date` |
| `allergy` | String | | Not in schema — omitted |

#### Delete — `DeleteMedicationAndAllergies`

**Request body:**

| Field | Type | Required |
|---|---|---|
| `userId` | String | ✅ |
| `recordId` | Int | ✅ |

---

### Medical History (`record_type: "medical_history"`)

#### Create — `CreateMedicalHistory`

> ⚠️ **Discrepancy in API.md:** Two sections conflict.
> - Detailed section (line ~800): `typeOfRecordId`, `recordDate`, `files` — no `history` field.
> - Simplified section (line ~4635): `history`, `createdBy` — no `typeOfRecordId`.
> Current implementation uses `history` + `recordDate` (hybrid approach).

**Request body (current implementation):**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | Maps from `username` |
| `history` | String | ✅ | Combined `"{disease} - {description}"` or just `disease` |
| `recordDate` | String | | Maps from `MedicalHistory.date` |
| `createdBy` | String | | Same as `userId` |
| `markAsImportant` | Boolean | | Hardcoded `false` |

**Response — key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | Int | New record ID (`_RESPONSE_ID_FIELD["medical_history"] = "id"`) |

#### Update — `UpdateMedicalHistory`

**Request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `userId` | String | ✅ | |
| `historyId` | Int | ✅ | `_RECORD_ID_FIELD["medical_history"] = "historyId"` |
| `history` | String | | Combined disease/description string |
| `recordDate` | String | | Maps from `MedicalHistory.date` |

#### Delete — `DeleteMedicalHistory`

**Request body:**

| Field | Type | Required |
|---|---|---|
| `userId` | String | ✅ |
| `historyId` | Int | ✅ |

---

## Planned Vaults (not yet implemented)

These vault domains are planned but have no schema or API mapping yet.
Add a new section here + a new `record_type` in `schemas.py` + entries in
`B4igoVaultApiStorage` when ready.

### Legal (`record_type: "legal"`) — TODO

Potential schema fields: case type, attorney, firm, document reference, date.
B4iGO microservice: Legal Microservice.

### Personal Info (`record_type: "personal"`) — TODO

Potential schema fields: TBD.
B4iGO microservice: PersonalInfo Microservice.

### Education (`record_type: "education"`) — TODO

Potential schema fields: institution, degree, graduation date, GPA.
B4iGO microservice: (TBD — not clearly listed in current API.md).

---

## Known TODOs / Gaps

| # | Issue | Location |
|---|---|---|
| 1 | `typeId` for doctor hardcoded to `0` — needs `getTypeOfDoctor` lookup | `_doctor_create_payload` |
| 2 | `InsuranceTypeId` hardcoded to `0` — needs `getTypeOfHealthInsurance` lookup | `_insurance_create_payload` |
| 3 | `userId` assumed equal to local `username` — may need `GetUserId` API call | all payloads |
| 4 | Medication fields `treatment_name`, `dosage`, `end_date`, `frequency_dosage`, `side_effect` not in `Medication` schema | `_medication_create_payload` |
| 5 | `CreateMedicalHistory` field conflict between two API.md sections — needs clarification | `_medical_history_create_payload` |
| 6 | No read endpoints documented for insurance/medication/medical_history — using generic records endpoint | `get_records` |
| 7 | File uploads not implemented (doctor/medication/insurance all accept `files`) | all create payloads |
| 8 | Endpoint URLs not in API.md — must be configured via env vars | `B4igoVaultApiStorage.__init__` |
