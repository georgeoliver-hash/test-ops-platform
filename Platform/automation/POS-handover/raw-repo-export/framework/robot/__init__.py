"""Robot Framework Library layer.

Replaces `framework/fixtures.py` + the root `conftest.py`. Each module here is
a thin wrapper instantiating the *existing*, framework-native classes
(`framework.transport.*`, `framework.android.*`, `framework.bos.*`,
`framework.wince.*`) — none of that code changed for the RF migration, only
the glue that wires it into a test runner did.
"""
