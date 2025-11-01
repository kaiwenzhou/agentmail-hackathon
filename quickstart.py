#!/usr/bin/env python3
"""
Quick Start Example - Use this to get started with AgentMail
"""

import sys
sys.path.insert(0, '.')

from src.agent.persona import Persona
from src.agent.email_agent import PersonaConsistentAgent

# Load a persona from config
persona = Persona.from_file("src/config/personas.yaml", "professional")

# Create the agent
agent = PersonaConsistentAgent(persona, validate_responses=True)

# Example email to respond to
email = """
Subject: Product Demo Request

Hi there,

I'm interested in learning more about your product.
Could we schedule a demo for next week?

Thanks!
Jane Smith
"""

# Generate response
result = agent.respond_to_email(email)

# Display results
print("=" * 60)
print("INCOMING EMAIL:")
print("=" * 60)
print(email)

print("\n" + "=" * 60)
print("AGENT RESPONSE:")
print("=" * 60)
print(result['response'])

print("\n" + "=" * 60)
print("METADATA:")
print("=" * 60)
print(f"Persona: {result['persona']}")
print(f"Subject: {result['metadata']['subject']}")
print(f"Questions: {result['metadata']['question_count']}")
print(f"Validation Score: {result['validation']['score']}")
print(f"Valid: {result['validation']['is_valid']}")
