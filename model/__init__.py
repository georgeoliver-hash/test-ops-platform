"""Shared, tool-agnostic schema.

Imports nothing from testops/ or sit-mirror/ tooling — testops/ imports FROM here, never the
reverse. Every model here is a thin, validated wrapper over real mirrored/distilled data; nothing
in this package invents facts.
"""
