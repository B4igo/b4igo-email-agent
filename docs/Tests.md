# Tests
Ideally, all core classes/methods should have fast, quality tests
associated with them.

When creating tests, add a `tests` folder within the subpackage containing the
module you want to test. Then, add a file titled `test_[module_name].py`

Ex.
```
- src
    - email
        - __init__.py
        - email_class.py
        - tests
            - __init__.py
            - test_email_class.py
```

The tests should use the `unittest` python package. Refer to [this file](../b4igo_email_agent/ai_pipeline/tests/test_domain_classifier.py)