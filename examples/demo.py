"""
Demo script showing how to use the PersonaConsistentAgent

This example demonstrates:
1. Loading personas from configuration
2. Creating an agent with a specific persona
3. Responding to emails while maintaining consistency
4. Validating response consistency
5. Switching between personas
"""

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.persona import Persona
from src.agent.email_agent import PersonaConsistentAgent


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def demo_professional_persona():
    """Demonstrate the professional persona"""
    print_section("Professional Persona Demo")

    # Load the professional persona
    persona = Persona.from_file("src/config/personas.yaml", "professional")
    agent = PersonaConsistentAgent(persona, validate_responses=True)

    print(agent.get_persona_summary())
    print("\n")

    # Sample email to respond to
    email = """
Subject: Meeting Request for Q4 Planning

Dear Team,

I hope this email finds you well. I would like to schedule a meeting
to discuss our Q4 planning and strategic initiatives.

Could we meet sometime next week? Please let me know your availability.

Best regards,
John
    """

    print("Incoming Email:")
    print("-" * 60)
    print(email)
    print("-" * 60)

    # Generate response
    result = agent.respond_to_email(email)

    print("\nAgent Response:")
    print("-" * 60)
    print(result['response'])
    print("-" * 60)

    if 'validation' in result:
        print("\nValidation Results:")
        print(f"  Valid: {result['validation']['is_valid']}")
        print(f"  Score: {result['validation']['score']}")
        print(f"  Checks: {len(result['validation']['checks'])}")


def demo_friendly_persona():
    """Demonstrate the friendly persona"""
    print_section("Friendly Persona Demo")

    # Load the friendly persona
    persona = Persona.from_file("src/config/personas.yaml", "friendly")
    agent = PersonaConsistentAgent(persona, validate_responses=True)

    print(agent.get_persona_summary())
    print("\n")

    # Sample email
    email = """
Hey!

Just wanted to check in and see how the project is going.
Do you need any help with anything?

Let me know!
Sarah
    """

    print("Incoming Email:")
    print("-" * 60)
    print(email)
    print("-" * 60)

    # Generate response
    result = agent.respond_to_email(email)

    print("\nAgent Response:")
    print("-" * 60)
    print(result['response'])
    print("-" * 60)


def demo_technical_persona():
    """Demonstrate the technical persona"""
    print_section("Technical Persona Demo")

    # Load the technical persona
    persona = Persona.from_file("src/config/personas.yaml", "technical")
    agent = PersonaConsistentAgent(persona, validate_responses=True)

    print(agent.get_persona_summary())
    print("\n")

    # Sample technical email
    email = """
Subject: API Integration Issue

Hello,

We're experiencing issues with the API integration. The authentication
endpoint is returning 401 errors intermittently.

Can you help troubleshoot this?

Thanks,
Dev Team
    """

    print("Incoming Email:")
    print("-" * 60)
    print(email)
    print("-" * 60)

    # Generate response
    result = agent.respond_to_email(email)

    print("\nAgent Response:")
    print("-" * 60)
    print(result['response'])
    print("-" * 60)


def demo_persona_consistency():
    """Demonstrate persona consistency across multiple interactions"""
    print_section("Persona Consistency Demo")

    persona = Persona.from_file("src/config/personas.yaml", "professional")
    agent = PersonaConsistentAgent(persona, validate_responses=True)

    emails = [
        "Can you provide an update on the project timeline?",
        "What's the status of the budget approval?",
        "Do we need to schedule a follow-up meeting?",
    ]

    print(f"Agent: {persona.name}")
    print(f"Processing {len(emails)} emails to test consistency...\n")

    for i, email in enumerate(emails, 1):
        print(f"\nEmail {i}: {email}")
        result = agent.respond_to_email(email)
        print(f"Response: {result['response'][:100]}...")

    print("\n")
    analysis = agent.analyze_consistency()
    print("Consistency Analysis:")
    for key, value in analysis.items():
        print(f"  {key}: {value}")


def demo_custom_persona():
    """Demonstrate creating a custom persona programmatically"""
    print_section("Custom Persona Demo")

    # Create a custom persona
    custom_persona = Persona(
        name="Executive Assistant",
        traits=["organized", "proactive", "diplomatic", "efficient"],
        tone="professional",
        values=["discretion", "accuracy", "responsiveness"],
        response_patterns={
            "greeting": "Good morning/afternoon",
            "closing": "Regards",
            "length": "concise"
        },
        vocabulary={
            "scheduling": ["coordinate", "arrange", "schedule", "confirm"],
            "action": ["prioritize", "handle", "manage", "organize"]
        },
        constraints=[
            "Never share confidential information",
            "Always confirm before making commitments"
        ]
    )

    agent = PersonaConsistentAgent(custom_persona, validate_responses=True)

    print("Custom Persona Created:")
    print(agent.get_persona_summary())
    print("\n")

    # Save the custom persona
    custom_persona.save_to_file("src/config/personas.yaml")
    print("Custom persona saved to configuration file!")


def main():
    """Run all demos"""
    print("\n" + "=" * 60)
    print("  AGENTMAIL - Persona-Consistent Email Agent Demo")
    print("=" * 60)

    try:
        demo_professional_persona()
        demo_friendly_persona()
        demo_technical_persona()
        demo_persona_consistency()
        demo_custom_persona()

        print_section("Demo Complete!")
        print("All personas demonstrated successfully.")
        print("\nKey Takeaways:")
        print("  • Each persona maintains consistent tone and style")
        print("  • Responses are validated for persona consistency")
        print("  • Context is preserved across interactions")
        print("  • Custom personas can be created and saved")
        print("\n")

    except Exception as e:
        print(f"\nError running demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
