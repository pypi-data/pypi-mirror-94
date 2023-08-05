[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![Downloads](https://pepy.tech/badge/kabaret.sqarf_flow/month)](https://pepy.tech/project/kabaret.sqarf_flow)

# kabaret.sqarf_flow

Kabaret flow extension to quality test your assets using https://pypi.org/project/sqarf

# Usage

1) Create your sqarf.QATest types (see sqarf documentation).
2) Subclass the `kabaret.sqarf_flow.qarun.QARun` Action and override its `get_test_types()`
method to return all your "root" test type.
4) Place this subclass as a child of the Object you want to test. It will be available 
in your test context as `context['TESTED']`.