#!/usr/bin/env python3
"""Test script for the email workflow.

This script demonstrates how to test the workflow with a mock agent.
For real testing, you'll need to set up a ReActAgent with proper LLM configuration.

IMPORTANT: Make sure you're using the virtual environment Python:
    /home/err/repo/.venv/bin/python test_workflow.py
    
Or activate the virtual environment first:
    source /home/err/repo/.venv/bin/activate
    python test_workflow.py
"""

import asyncio
import logging
import sys
from datetime import datetime
from typing import Any

# Setup logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if we're using the venv Python
if not sys.executable.startswith('/home/err/repo/.venv'):
    logger.warning(
        f"Warning: Not using virtual environment Python.\n"
        f"Current Python: {sys.executable}\n"
        f"Recommended: /home/err/repo/.venv/bin/python test_workflow.py\n"
        f"Or activate venv: source /home/err/repo/.venv/bin/activate"
    )

# Mock the missing dependencies if they don't exist
try:
    from src.email.email_parser import format_email_for_llm
except ImportError:
    logger.warning("email_parser not found, using mock")
    def format_email_for_llm(email) -> str:
        """Mock email formatter."""
        return f"From: {email.from_address}\nSubject: {email.subject}\n\n{email.body}"

try:
    from src.agent.schemas import VaultExtraction, AgentResponse
except ImportError:
    logger.warning("schemas not found, using mock")
    try:
        from pydantic import BaseModel
    except ImportError:
        logger.error("pydantic is not installed. Please install dependencies:")
        logger.error("  pip install -r requirements.txt")
        logger.error("Or use the virtual environment Python:")
        logger.error("  /home/err/repo/.venv/bin/python test_workflow.py")
        raise ImportError(
            "pydantic is required but not installed. "
            "Install with: pip install -r requirements.txt"
        )
    
    class VaultExtraction(BaseModel):
        """Mock VaultExtraction."""
        vault_type: str
        confidence: float
        extracted_data: dict
        suggested_actions: list = []
        reasoning: str = ""
    
    class AgentResponse(BaseModel):
        """Mock AgentResponse."""
        extraction: VaultExtraction
        processing_time: float
        tools_used: list = []
        errors: list = []
        warnings: list = []

from src.email.models import EmailInput
from src.agent.workflow import AgentWorkflow


class MockAgent:
    """Mock ReActAgent for testing purposes.
    
    Replace this with a real ReActAgent instance for actual testing.
    Example:
        from llama_index.agent import ReActAgent
        from llama_index.llms.ollama import Ollama
        
        llm = Ollama(model="llama3.2", request_timeout=120.0)
        agent = ReActAgent.from_tools([], llm=llm, verbose=True)
    """
    
    def __init__(self):
        self.call_count = 0
    
    def chat(self, prompt: str) -> Any:
        """Mock chat method that returns a simple response."""
        self.call_count += 1
        logger.info(f"Mock agent called (call #{self.call_count})")
        logger.debug(f"Prompt: {prompt[:200]}...")
        
        # Return a mock response object
        class MockResponse:
            def __init__(self, text: str):
                self.response = text
        
        # Simulate different responses based on the step
        if "classify" in prompt.lower() or "vault type" in prompt.lower():
            # Check if email content suggests healthcare
            if any(word in prompt.lower() for word in ["appointment", "doctor", "medical", "health", "prescription", "test result"]):
                return MockResponse("""
                {
                    "vault_type": "healthcare",
                    "confidence": 0.95,
                    "reasoning": "Email contains healthcare-related information",
                    "multiple_vaults": null
                }
                """)
            else:
                return MockResponse("""
                {
                    "vault_type": "communications",
                    "confidence": 0.85,
                    "reasoning": "Email appears to be a general communication message",
                    "multiple_vaults": null
                }
                """)
        elif "extract" in prompt.lower():
            # Check if this is healthcare extraction
            if "healthcare" in prompt.lower() or "appointment" in prompt.lower():
                return MockResponse("""
                {
                    "appointments": [
                        {
                            "date": "2024-02-15T10:00:00",
                            "time": "10:00 AM",
                            "provider": "Dr. Sarah Johnson",
                            "location": "123 Medical Center, Suite 200",
                            "appointment_type": "Annual Checkup",
                            "duration": 30,
                            "notes": "Please arrive 15 minutes early"
                        }
                    ],
                    "test_results": [
                        {
                            "test_name": "Blood Panel",
                            "date": "2024-01-20",
                            "results": "All values within normal range",
                            "provider": "LabCorp"
                        }
                    ],
                    "prescriptions": [],
                    "providers": [
                        {
                            "name": "Dr. Sarah Johnson",
                            "specialty": "Internal Medicine",
                            "contact": "555-123-4567",
                            "facility": "123 Medical Center"
                        }
                    ],
                    "insurance": null,
                    "medical_records": [],
                    "bills": [],
                    "conditions": [],
                    "notes": "Annual checkup scheduled"
                }
                """)
            else:
                return MockResponse("""
                {
                    "sender": "test@example.com",
                    "recipient": "user@example.com",
                    "subject": "Test Email",
                    "topics": ["testing", "workflow"],
                    "action_items": ["Review test results"],
                    "deadline": null
                }
                """)
        elif "validate" in prompt.lower():
            return MockResponse("""
            {
                "validation_passed": true,
                "validation_errors": [],
                "reasoning": "All required fields are present and valid"
            }
            """)
        else:
            return MockResponse("Mock response for testing")
    
    async def chat_async(self, prompt: str) -> Any:
        """Mock async chat method."""
        return self.chat(prompt)


def create_test_email() -> EmailInput:
    """Create a test email for testing."""
    return EmailInput(
        from_address="sender@example.com",
        to_address="recipient@example.com",
        subject="Test Email for Workflow",
        body="""
        Hello,
        
        This is a test email to verify the workflow is working correctly.
        
        Please review the attached documents and let me know if you have any questions.
        
        Best regards,
        Test Sender
        """,
        received_at=datetime.now(),
        metadata=None,
        attachments=[],
    )


def create_healthcare_test_email() -> EmailInput:
    """Create a healthcare test email for testing."""
    return EmailInput(
        from_address="appointments@medicalcenter.com",
        to_address="patient@example.com",
        subject="Appointment Reminder - Annual Checkup",
        body="""
        Dear Patient,
        
        This is a reminder that you have an appointment scheduled:
        
        Date: February 15, 2024
        Time: 10:00 AM
        Provider: Dr. Sarah Johnson
        Location: 123 Medical Center, Suite 200
        Type: Annual Checkup
        
        Please arrive 15 minutes early to complete any necessary paperwork.
        
        Your recent blood panel results from January 20, 2024 are available and show all values within normal range.
        
        If you need to reschedule, please call us at 555-123-4567.
        
        Best regards,
        Medical Center Scheduling
        """,
        received_at=datetime.now(),
        metadata=None,
        attachments=[],
    )


async def test_workflow_async():
    """Test the workflow asynchronously."""
    logger.info("=" * 60)
    logger.info("Testing Email Workflow (Async)")
    logger.info("=" * 60)
    
    # Create mock agent
    agent = MockAgent()
    
    # Create workflow
    workflow = AgentWorkflow(agent=agent)
    
    # Create test email
    email = create_test_email()
    
    # Test the workflow
    try:
        logger.info(f"Processing email: {email.subject}")
        result = await workflow.process_email_async(email=email)
        
        logger.info("Workflow completed successfully!")
        logger.info(f"Result type: {type(result)}")
        
        if hasattr(result, 'extraction'):
            logger.info(f"Vault type: {result.extraction.vault_type}")
            logger.info(f"Confidence: {result.extraction.confidence}")
            logger.info(f"Extracted data keys: {list(result.extraction.extracted_data.keys()) if isinstance(result.extraction.extracted_data, dict) else 'N/A'}")
        
        if hasattr(result, 'processing_time'):
            logger.info(f"Processing time: {result.processing_time:.2f}s")
        
        if hasattr(result, 'errors') and result.errors:
            logger.warning(f"Errors: {result.errors}")
        
        if hasattr(result, 'warnings') and result.warnings:
            logger.warning(f"Warnings: {result.warnings}")
        
        logger.info(f"Agent was called {agent.call_count} times (expected: 3 - classify, extract, validate)")
        
        return result
        
    except Exception as e:
        logger.error(f"Workflow test failed: {e}", exc_info=True)
        raise


def test_workflow_sync():
    """Test the workflow synchronously."""
    logger.info("=" * 60)
    logger.info("Testing Email Workflow (Sync)")
    logger.info("=" * 60)
    
    # Create mock agent
    agent = MockAgent()
    
    # Create workflow
    workflow = AgentWorkflow(agent=agent)
    
    # Create test email
    email = create_test_email()
    
    # Test the workflow
    try:
        logger.info(f"Processing email: {email.subject}")
        result = workflow.process_email(email=email)
        
        logger.info("Workflow completed successfully!")
        logger.info(f"Result type: {type(result)}")
        
        if hasattr(result, 'extraction'):
            logger.info(f"Vault type: {result.extraction.vault_type}")
            logger.info(f"Confidence: {result.extraction.confidence}")
            logger.info(f"Extracted data keys: {list(result.extraction.extracted_data.keys()) if isinstance(result.extraction.extracted_data, dict) else 'N/A'}")
        
        if hasattr(result, 'processing_time'):
            logger.info(f"Processing time: {result.processing_time:.2f}s")
        
        logger.info(f"Agent was called {agent.call_count} times (expected: 3 - classify, extract, validate)")
        
        return result
        
    except Exception as e:
        logger.error(f"Workflow test failed: {e}", exc_info=True)
        raise


def test_healthcare_workflow():
    """Test the workflow with a healthcare email."""
    logger.info("=" * 60)
    logger.info("Testing Healthcare Email Workflow")
    logger.info("=" * 60)
    
    # Create mock agent
    agent = MockAgent()
    
    # Create workflow
    workflow = AgentWorkflow(agent=agent)
    
    # Create healthcare test email
    email = create_healthcare_test_email()
    
    # Test the workflow
    try:
        logger.info(f"Processing healthcare email: {email.subject}")
        result = workflow.process_email(email=email)
        
        logger.info("Workflow completed successfully!")
        logger.info(f"Result type: {type(result)}")
        
        if hasattr(result, 'extraction'):
            logger.info(f"Vault type: {result.extraction.vault_type}")
            logger.info(f"Confidence: {result.extraction.confidence}")
            
            # Show extracted healthcare data
            extracted = result.extraction.extracted_data
            logger.info(f"Extracted data keys: {list(extracted.keys()) if isinstance(extracted, dict) else 'N/A'}")
            
            if isinstance(extracted, dict):
                if "appointments" in extracted:
                    logger.info(f"Appointments found: {len(extracted['appointments'])}")
                    for i, apt in enumerate(extracted['appointments'], 1):
                        logger.info(f"  Appointment {i}: {apt.get('provider', 'N/A')} on {apt.get('date', 'N/A')}")
                
                if "test_results" in extracted:
                    logger.info(f"Test results found: {len(extracted['test_results'])}")
                
                if "providers" in extracted:
                    logger.info(f"Providers found: {len(extracted['providers'])}")
            
            if result.extraction.suggested_actions:
                logger.info(f"Suggested actions: {len(result.extraction.suggested_actions)}")
                for action in result.extraction.suggested_actions:
                    logger.info(f"  - {action.action_type}: {action.description}")
        
        if hasattr(result, 'processing_time'):
            logger.info(f"Processing time: {result.processing_time:.2f}s")
        
        if hasattr(result, 'errors') and result.errors:
            logger.warning(f"Errors: {result.errors}")
        
        if hasattr(result, 'warnings') and result.warnings:
            logger.warning(f"Warnings: {result.warnings}")
        
        logger.info(f"Agent was called {agent.call_count} times (expected: 3 - classify, extract, validate)")
        
        # Validate healthcare schema
        try:
            from src.agent.schemas import HealthcareVaultSchema
            schema = HealthcareVaultSchema(**extracted)
            logger.info("✓ Healthcare schema validation passed!")
        except Exception as e:
            logger.warning(f"Healthcare schema validation failed: {e}")
        
        return result
        
    except Exception as e:
        logger.error(f"Healthcare workflow test failed: {e}", exc_info=True)
        raise


def test_with_real_agent():
    """Example of how to test with a real ReActAgent.
    
    Uncomment and configure this function to test with a real LLM.
    """
    try:
        from llama_index.agent import ReActAgent
        from llama_index.llms.ollama import Ollama
        
        # Configure your LLM (adjust model name and settings as needed)
        llm = Ollama(model="llama3.2", request_timeout=120.0)
        
        # Create agent with tools (add your tools here)
        agent = ReActAgent.from_tools([], llm=llm, verbose=True)
        
        # Create workflow
        workflow = AgentWorkflow(agent=agent)
        
        # Create test email
        email = create_test_email()
        
        # Test
        result = workflow.process_email(email=email)
        
        logger.info("Real agent test completed!")
        return result
        
    except ImportError as e:
        logger.error(f"Could not import required packages: {e}")
        logger.info("Make sure llama-index and llama-index-llms-ollama are installed")
    except Exception as e:
        logger.error(f"Real agent test failed: {e}", exc_info=True)


if __name__ == "__main__":
    import sys
    
    # Choose test mode
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = "sync"
    
    if mode == "async":
        # Run async test
        asyncio.run(test_workflow_async())
    elif mode == "healthcare":
        # Run healthcare-specific test
        test_healthcare_workflow()
    elif mode == "real":
        # Run with real agent (requires LLM setup)
        test_with_real_agent()
    else:
        # Run sync test (default)
        test_workflow_sync()
