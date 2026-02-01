# Testing the Email Workflow

This guide explains how to test the email workflow system.

## Quick Start

### Basic Test (Mock Agent)

Run the test script with a mock agent:

```bash
# Synchronous test (default)
python test_workflow.py

# Or explicitly
python test_workflow.py sync

# Asynchronous test
python test_workflow.py async

# Healthcare-specific test
python test_workflow.py healthcare
```

The mock agent will simulate responses without requiring an actual LLM.

### Test with Real Agent

To test with a real LLM (requires Ollama or similar):

1. Make sure you have Ollama running locally with a model installed:
   ```bash
   ollama serve
   ollama pull llama3.2  # or your preferred model
   ```

2. Uncomment and modify the `test_with_real_agent()` function in `test_workflow.py`

3. Run:
   ```bash
   python test_workflow.py real
   ```

## What the Test Does

The test script:

1. **Creates a test email** - Generates a sample `EmailInput` object
2. **Initializes the workflow** - Creates an `AgentWorkflow` instance
3. **Processes the email** - Runs through all workflow steps:
   - Planning
   - Extraction
   - Validation
   - Finalization
4. **Displays results** - Shows extracted data, processing time, errors, etc.

## Workflow Steps

The workflow processes emails through these steps:

1. **Classification** - Determines the vault type (e.g., healthcare, financial)
2. **Extraction** - Extracts structured data from the email matching the vault schema
3. **Validation** - Validates the extracted data against the vault schema
4. **Finalization** - Creates the final `AgentResponse`

## Healthcare Vault Testing

To test the healthcare vault schema specifically:

```bash
# Run healthcare test
python test_workflow.py healthcare

# Or use the helper script
./test_healthcare.sh
```

The healthcare test:
- Uses a sample appointment reminder email
- Tests classification as "healthcare" vault type
- Validates extraction against the `HealthcareVaultSchema`
- Checks that appointments, providers, and test results are extracted correctly
- Verifies Pydantic schema validation

Expected healthcare output includes:
- `appointments` - List of appointment details
- `test_results` - Lab results and diagnostics
- `prescriptions` - Medication information
- `providers` - Healthcare provider details
- `insurance` - Insurance information
- `medical_records` - Medical documents
- `bills` - Medical billing
- `conditions` - Health conditions mentioned

## Mock vs Real Agent

### Mock Agent
- **Pros**: Fast, no LLM required, good for testing workflow logic
- **Cons**: Returns predetermined responses, doesn't test actual LLM integration

### Real Agent
- **Pros**: Tests full integration, real LLM responses
- **Cons**: Requires LLM setup, slower, may cost money (if using cloud APIs)

## Expected Output

When the test runs successfully, you should see:

```
============================================================
Testing Email Workflow (Sync)
============================================================
INFO: Processing email: Test Email for Workflow
INFO: Workflow completed successfully!
INFO: Result type: <class 'src.agent.schemas.AgentResponse'>
INFO: Vault type: communications
INFO: Confidence: 0.85
INFO: Extracted data keys: ['sender', 'recipient', 'subject', ...]
INFO: Processing time: 2.34s
INFO: Agent was called 3 times
```

## Troubleshooting

### Import Errors

If you see import errors for `email_parser` or `schemas`:
- The test script includes mock implementations
- For production use, create these modules:
  - `src/email/email_parser.py` with `format_email_for_llm()` function
  - `src/agent/schemas.py` with `VaultExtraction` and `AgentResponse` classes

### Workflow Errors

If the workflow fails:
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Verify the Python interpreter is set correctly (see `.vscode/settings.json`)
- Check logs for specific error messages

### Agent Not Responding

If using a real agent:
- Verify Ollama is running: `curl http://localhost:11434/api/tags`
- Check the model is installed: `ollama list`
- Verify network connectivity if using remote LLM

## Next Steps

1. **Create missing modules** - Implement `email_parser.py` and `schemas.py` for production
2. **Add more test cases** - Test different email types, edge cases
3. **Integration tests** - Test with real email data
4. **Performance testing** - Measure workflow performance with various email sizes
