"""Simple email processing workflow: classify → extract → validate → finalize."""

import asyncio
import json
import logging
import re
import time
from typing import Any, Dict, List, Optional

from src.email.models import EmailInput
from src.email.email_parser import format_email_for_llm
from src.agent.schemas import (
    VaultExtraction,
    AgentResponse,
    SuggestedAction,
    get_vault_schema_definition,
    HealthcareVaultSchema,
)

logger = logging.getLogger(__name__)


def _extract_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """Extract JSON object from text (handles code fences and plain JSON)."""
    if not text:
        return None

    # Try fenced JSON first (```json ... ```)
    fenced_re = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL | re.IGNORECASE)
    m = fenced_re.search(text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass

    # Try balanced braces
    start_positions = [i for i, ch in enumerate(text) if ch == "{"]
    for i in start_positions:
        depth = 0
        for j in range(i, len(text)):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        parsed = json.loads(text[i: j + 1])
                        if isinstance(parsed, dict):
                            return parsed
                    except json.JSONDecodeError:
                        continue
                    break

    return None


def _parse_suggested_actions(response_text: str) -> List[str]:
    """Extract suggested actions from response text."""
    data = _extract_json_from_text(response_text)
    if data and "suggested_actions" in data and isinstance(data["suggested_actions"], list):
        return [str(a).strip() for a in data["suggested_actions"] if str(a).strip()]
    
    # Fallback: look for bullet points under "Suggested actions"
    lines = response_text.splitlines()
    suggestions = []
    capture = False
    for line in lines:
        if "suggested actions" in line.lower():
            capture = True
            continue
        if capture:
            s = line.strip().lstrip("-* ").strip()
            if not s:
                break
            suggestions.append(s)
            if len(suggestions) > 10:
                break
    return suggestions


def _convert_suggested_actions(action_strings: List[str]) -> List[SuggestedAction]:
    """Convert action strings to SuggestedAction objects."""
    if not action_strings:
        return []
    
    actions = []
    for action_str in action_strings:
        if not action_str or not isinstance(action_str, str):
            continue
        
        # Infer action type from description
        action_type = "general"
        action_lower = action_str.lower()
        if any(word in action_lower for word in ["calendar", "schedule", "appointment", "meeting"]):
            action_type = "calendar"
        elif any(word in action_lower for word in ["reminder", "remind"]):
            action_type = "reminder"
        elif any(word in action_lower for word in ["contact", "update"]):
            action_type = "update_contact"
        elif any(word in action_lower for word in ["bill", "payment", "pay"]):
            action_type = "payment"
        
        actions.append(SuggestedAction(
            action_type=action_type,
            description=action_str.strip(),
            params={},
        ))
    
    return actions


async def _call_agent(agent: Any, prompt: str) -> str:
    """Call agent and return response as string."""
    try:
        if hasattr(agent, "chat_async"):
            resp = await agent.chat_async(prompt)
        else:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: agent.chat(prompt))
        
        if hasattr(resp, "response"):
            return getattr(resp, "response") or ""
        return str(resp or "")
    except Exception as e:
        logger.exception("Agent call failed")
        return ""


async def classify_email(agent: Any, email: EmailInput) -> Dict[str, Any]:
    """Classify email and determine vault type."""
    logger.info("Step 1: Classify Email")
    
    email_content = format_email_for_llm(email)
    
    prompt = f"""Classify this email and determine which vault type it belongs to.

Email:
{email_content}

The 8 vault types are:
- personal_info: Personal identification, documents, etc.
- healthcare: Medical records, appointments, health information
- digital_accounts: Online accounts, passwords, digital services
- key_master_directives: Important instructions, preferences
- legal: Legal documents, contracts, legal matters
- communications: General communications, messages
- end_of_life: End-of-life planning, wills, final wishes
- financial: Bills, payments, financial transactions

Return a JSON object with:
- vault_type: the determined vault type
- confidence: confidence score (0.0 to 1.0)
- reasoning: brief explanation
- multiple_vaults: optional list if email belongs to multiple vaults
"""

    response = await _call_agent(agent, prompt)
    result = _extract_json_from_text(response)
    
    if not result:
        # Fallback
        result = {"vault_type": "communications", "confidence": 0.5, "reasoning": response[:200]}
        vault_types = ["personal_info", "healthcare", "digital_accounts", "key_master_directives",
                       "legal", "communications", "end_of_life", "financial"]
        lower_text = response.lower()
        for vt in vault_types:
            if vt in lower_text:
                result["vault_type"] = vt
                break
    
    vault_type = result.get("vault_type", "communications")
    confidence = float(result.get("confidence", 0.5))
    
    logger.info("Email classified as: %s (confidence: %.2f)", vault_type, confidence)
    
    return {
        "vault_type": vault_type,
        "confidence": confidence,
        "reasoning": result.get("reasoning"),
        "email_content": email_content,
    }


async def extract_information(agent: Any, email: EmailInput, vault_type: str, email_content: str) -> Dict[str, Any]:
    """Extract structured information from email."""
    logger.info("Step 2: Extract Information")
    
    schema_definition = get_vault_schema_definition(vault_type)
    
    prompt = (
        f"Extract structured information from the email for the {vault_type} vault.\n\n"
        f"Email:\n{email_content}\n\n"
        f"Schema definition:\n{schema_definition}\n\n"
        f"Extract all relevant information from the email matching this schema. "
        f"Return a JSON object with the extracted data. Only include fields that have data in the email."
    )
    
    response = await _call_agent(agent, prompt)
    extracted_data = _extract_json_from_text(response) or {}
    suggested_actions = _parse_suggested_actions(response)
    
    logger.info("Extracted data keys: %s", list(extracted_data.keys()) if isinstance(extracted_data, dict) else "N/A")
    
    return {
        "extracted_data": extracted_data,
        "suggested_actions": suggested_actions,
    }


async def validate_extraction(agent: Any, vault_type: str, extracted_data: Dict[str, Any]) -> bool:
    """Validate extracted data against vault schema."""
    logger.info("Step 3: Validate Extraction")
    
    # Try Pydantic validation first for healthcare
    if vault_type == "healthcare":
        try:
            HealthcareVaultSchema(**extracted_data)
            logger.info("Validation passed (Pydantic schema validation)")
            return True
        except Exception as e:
            logger.warning(f"Pydantic validation failed: {e}, falling back to LLM validation")
    
    # Fallback to LLM validation
    schema_definition = get_vault_schema_definition(vault_type)
    
    prompt = f"""Validate the extracted data against the {vault_type} vault schema.

Schema definition:
{schema_definition}

Extracted data:
{json.dumps(extracted_data, indent=2)}

Check if the extracted data matches the schema structure and required fields.
If there are missing or malformed fields, list them clearly and suggest fixes.
Return a JSON object with:
- validation_passed: boolean
- validation_errors: list (empty if none)
- reasoning: short explanation
"""

    response = await _call_agent(agent, prompt)
    result = _extract_json_from_text(response)
    
    if result and isinstance(result, dict) and "validation_passed" in result:
        validation_passed = bool(result["validation_passed"])
    else:
        # Fallback: check if data exists
        validation_passed = bool(extracted_data)
    
    if not validation_passed:
        logger.warning("Validation had issues")
    
    logger.info("Validation %s", "passed" if validation_passed else "failed")
    
    return validation_passed


async def process_email_async(agent: Any, email: EmailInput) -> AgentResponse:
    """Process email through the complete workflow."""
    start_time = time.time()
    errors = []
    warnings = []
    
    try:
        # Step 1: Classify
        classification = await classify_email(agent, email)
        vault_type = classification["vault_type"]
        email_content = classification["email_content"]
        
        # Step 2: Extract
        extraction = await extract_information(agent, email, vault_type, email_content)
        extracted_data = extraction["extracted_data"]
        suggested_actions_raw = extraction["suggested_actions"]
        
        # Step 3: Validate
        validation_passed = await validate_extraction(agent, vault_type, extracted_data)
        if not validation_passed:
            warnings.append("Schema validation had issues")
        
        # Step 4: Finalize
        suggested_actions = _convert_suggested_actions(suggested_actions_raw)
        
        confidence = 0.3
        if extracted_data:
            confidence = 0.7
        if validation_passed:
            confidence = min(confidence + 0.15, 1.0)
        
        vault_extraction = VaultExtraction(
            vault_type=vault_type,
            confidence=confidence,
            extracted_data=extracted_data,
            suggested_actions=suggested_actions,
            reasoning=f"Extracted using {vault_type} schema. Validation: {'passed' if validation_passed else 'issues'}",
        )
        
        processing_time = time.time() - start_time
        
        logger.info("Workflow completed in %.2fs", processing_time)
        
        return AgentResponse(
            extraction=vault_extraction,
            processing_time=processing_time,
            tools_used=[],
            errors=errors,
            warnings=warnings,
        )
        
    except Exception as e:
        logger.exception("Workflow failed")
        errors.append(str(e))
        return AgentResponse(
            extraction=VaultExtraction(
                vault_type="communications",
                confidence=0.0,
                extracted_data={},
                suggested_actions=[],
                reasoning=f"Error: {str(e)}",
            ),
            processing_time=time.time() - start_time,
            tools_used=[],
            errors=errors,
            warnings=warnings,
        )


class AgentWorkflow:
    """Simple wrapper for email processing workflow."""
    
    def __init__(self, agent: Any):
        self.agent = agent
    
    async def process_email_async(self, email: EmailInput) -> AgentResponse:
        """Process email asynchronously."""
        return await process_email_async(self.agent, email)
    
    def process_email(self, email: EmailInput) -> AgentResponse:
        """Process email synchronously."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(lambda: asyncio.run(self.process_email_async(email)))
                    return future.result()
            else:
                return loop.run_until_complete(self.process_email_async(email))
        except RuntimeError:
            return asyncio.run(self.process_email_async(email))
