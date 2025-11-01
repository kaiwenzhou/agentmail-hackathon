"""
Tests for persona consistency in the AgentMail system
"""

import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.persona import Persona
from src.agent.email_agent import PersonaConsistentAgent
from src.agent.validator import PersonaValidator


class TestPersona:
    """Tests for the Persona class"""

    def test_persona_creation(self):
        """Test creating a basic persona"""
        persona = Persona(
            name="Test Agent",
            traits=["friendly", "helpful"],
            tone="casual",
            values=["honesty", "clarity"]
        )

        assert persona.name == "Test Agent"
        assert "friendly" in persona.traits
        assert persona.tone == "casual"
        assert len(persona.values) == 2

    def test_persona_context_memory(self):
        """Test adding and retrieving context"""
        persona = Persona(name="Test")

        # Add some interactions
        for i in range(5):
            persona.add_context({
                'type': 'email',
                'summary': f'Interaction {i}'
            })

        assert len(persona.context_memory) == 5

        # Add more to test limit
        for i in range(10):
            persona.add_context({
                'type': 'email',
                'summary': f'Interaction {i+5}'
            })

        # Should keep only last 10
        assert len(persona.context_memory) == 10

    def test_persona_prompt_generation(self):
        """Test generating persona prompt"""
        persona = Persona(
            name="Test Agent",
            traits=["professional", "accurate"],
            tone="formal",
            values=["precision"],
            constraints=["Never make assumptions"]
        )

        prompt = persona.get_persona_prompt()

        assert "Test Agent" in prompt
        assert "professional" in prompt
        assert "formal" in prompt
        assert "Never make assumptions" in prompt

    def test_persona_to_dict(self):
        """Test converting persona to dictionary"""
        persona = Persona(
            name="Test",
            traits=["helpful"],
            tone="neutral"
        )

        data = persona.to_dict()

        assert isinstance(data, dict)
        assert data['name'] == "Test"
        assert data['traits'] == ["helpful"]
        assert data['tone'] == "neutral"

    def test_persona_from_dict(self):
        """Test creating persona from dictionary"""
        data = {
            'name': 'DictAgent',
            'traits': ['smart', 'quick'],
            'tone': 'professional',
            'values': ['speed']
        }

        persona = Persona.from_dict(data)

        assert persona.name == 'DictAgent'
        assert 'smart' in persona.traits
        assert persona.tone == 'professional'


class TestPersonaValidator:
    """Tests for the PersonaValidator class"""

    def test_tone_validation_formal(self):
        """Test validating formal tone"""
        persona = Persona(
            name="Formal Agent",
            tone="formal"
        )
        validator = PersonaValidator(persona)

        # Should pass formal tone
        formal_response = "I hereby confirm that I shall kindly assist you."
        is_valid, msg = validator.validate_tone(formal_response)
        assert is_valid

        # Should fail informal tone
        informal_response = "Yeah, gonna help you out!"
        is_valid, msg = validator.validate_tone(informal_response)
        assert not is_valid

    def test_tone_validation_casual(self):
        """Test validating casual tone"""
        persona = Persona(
            name="Casual Agent",
            tone="casual"
        )
        validator = PersonaValidator(persona)

        # Should pass casual tone
        casual_response = "Hey! Thanks for reaching out, sounds good to me!"
        is_valid, msg = validator.validate_tone(casual_response)
        assert is_valid

        # Should fail very formal tone
        formal_response = "Pursuant to the aforementioned request, I hereby confirm."
        is_valid, msg = validator.validate_tone(formal_response)
        assert not is_valid

    def test_constraints_validation(self):
        """Test validating constraints"""
        persona = Persona(
            name="Constrained Agent",
            constraints=[
                "Never use the word 'maybe'",
                "Never make promises"
            ]
        )
        validator = PersonaValidator(persona)

        # Should pass
        good_response = "I will look into this for you."
        is_valid, violations = validator.validate_constraints(good_response)
        assert is_valid
        assert len(violations) == 0

        # Should fail
        bad_response = "Maybe I can help you with this."
        is_valid, violations = validator.validate_constraints(bad_response)
        assert not is_valid
        assert len(violations) > 0

    def test_response_length_validation(self):
        """Test validating response length"""
        persona = Persona(name="Test")
        validator = PersonaValidator(persona)

        # Brief response
        brief = "Okay, will do."
        is_valid, msg = validator.validate_response_length(brief, "brief")
        assert is_valid

        # Too short for detailed
        is_valid, msg = validator.validate_response_length(brief, "detailed")
        assert not is_valid

    def test_full_validation(self):
        """Test comprehensive response validation"""
        persona = Persona(
            name="Professional Agent",
            tone="professional",
            constraints=["Never use slang"]
        )
        validator = PersonaValidator(persona)

        response = "Thank you for your email. I appreciate your inquiry and will be happy to assist."

        result = validator.validate_response(response)

        assert isinstance(result, dict)
        assert 'is_valid' in result
        assert 'checks' in result
        assert 'score' in result


class TestPersonaConsistentAgent:
    """Tests for the PersonaConsistentAgent class"""

    def test_agent_initialization(self):
        """Test creating an agent"""
        persona = Persona(name="Test Agent", tone="professional")
        agent = PersonaConsistentAgent(persona)

        assert agent.persona.name == "Test Agent"
        assert agent.validate_responses == True

    def test_agent_without_validation(self):
        """Test creating an agent without validation"""
        persona = Persona(name="Test")
        agent = PersonaConsistentAgent(persona, validate_responses=False)

        assert agent.validator is None
        assert agent.validate_responses == False

    def test_email_metadata_extraction(self):
        """Test extracting metadata from emails"""
        persona = Persona(name="Test")
        agent = PersonaConsistentAgent(persona)

        email = """
Subject: Urgent Request

This is an urgent matter that needs immediate attention.
Can you help ASAP?
        """

        metadata = agent._extract_email_metadata(email)

        assert metadata['subject'] == "Urgent Request"
        assert metadata['question_count'] == 1
        assert len(metadata['urgency_indicators']) > 0
        assert 'urgent' in [x.lower() for x in metadata['urgency_indicators']]

    def test_respond_to_email(self):
        """Test generating email response"""
        persona = Persona(
            name="Test Agent",
            tone="professional",
            response_patterns={
                'greeting': 'Dear',
                'closing': 'Best regards'
            }
        )
        agent = PersonaConsistentAgent(persona, validate_responses=False)

        email = "Can you help me with this issue?"

        result = agent.respond_to_email(email)

        assert 'response' in result
        assert 'metadata' in result
        assert 'persona' in result
        assert result['persona'] == "Test Agent"
        assert isinstance(result['response'], str)
        assert len(result['response']) > 0

    def test_persona_summary(self):
        """Test getting persona summary"""
        persona = Persona(
            name="Summary Test",
            tone="friendly",
            traits=["helpful", "quick"],
            values=["efficiency"]
        )
        agent = PersonaConsistentAgent(persona)

        summary = agent.get_persona_summary()

        assert "Summary Test" in summary
        assert "friendly" in summary
        assert "helpful" in summary

    def test_update_persona(self):
        """Test updating persona attributes"""
        persona = Persona(name="Test", tone="formal")
        agent = PersonaConsistentAgent(persona)

        assert agent.persona.tone == "formal"

        agent.update_persona(tone="casual")

        assert agent.persona.tone == "casual"

    def test_consistency_analysis(self):
        """Test analyzing consistency across interactions"""
        persona = Persona(name="Test", tone="professional")
        agent = PersonaConsistentAgent(persona, validate_responses=False)

        # No interactions yet
        analysis = agent.analyze_consistency()
        assert analysis['total_interactions'] == 0

        # Add some interactions
        agent.respond_to_email("Test email 1")
        agent.respond_to_email("Test email 2")
        agent.respond_to_email("Test email 3")

        analysis = agent.analyze_consistency()
        assert analysis['total_interactions'] == 3
        assert analysis['persona_name'] == "Test"


class TestPersonaConfiguration:
    """Tests for persona configuration loading"""

    def test_load_persona_from_file(self):
        """Test loading persona from YAML file"""
        config_path = "src/config/personas.yaml"

        # Check if file exists
        if not Path(config_path).exists():
            pytest.skip("Configuration file not found")

        # Load professional persona
        persona = Persona.from_file(config_path, "professional")

        assert persona.name == "professional"
        assert len(persona.traits) > 0
        assert persona.tone == "professional"

    def test_load_multiple_personas(self):
        """Test loading multiple personas"""
        config_path = "src/config/personas.yaml"

        if not Path(config_path).exists():
            pytest.skip("Configuration file not found")

        persona_names = ["professional", "friendly", "technical"]

        for name in persona_names:
            persona = Persona.from_file(config_path, name)
            assert persona.name == name
            assert len(persona.traits) > 0

    def test_invalid_persona_name(self):
        """Test loading non-existent persona"""
        config_path = "src/config/personas.yaml"

        if not Path(config_path).exists():
            pytest.skip("Configuration file not found")

        with pytest.raises(KeyError):
            Persona.from_file(config_path, "nonexistent_persona")


class TestIntegration:
    """Integration tests for the complete system"""

    def test_end_to_end_workflow(self):
        """Test complete workflow from persona creation to email response"""
        # Create persona
        persona = Persona(
            name="Integration Test Agent",
            traits=["professional", "helpful"],
            tone="professional",
            values=["clarity", "accuracy"],
            response_patterns={
                'greeting': 'Hello',
                'closing': 'Best regards'
            },
            constraints=["Never use slang"]
        )

        # Create agent
        agent = PersonaConsistentAgent(persona, validate_responses=True)

        # Process email
        email = """
Subject: Question about service

Hello,

I have a question about your services. Could you provide more information?

Thanks,
Customer
        """

        result = agent.respond_to_email(email)

        # Verify result structure
        assert 'response' in result
        assert 'metadata' in result
        assert 'validation' in result
        assert 'persona' in result

        # Verify persona consistency
        assert result['persona'] == "Integration Test Agent"

        # Verify validation was performed
        validation = result['validation']
        assert 'is_valid' in validation
        assert 'checks' in validation
        assert 'score' in validation

        # Check context was stored
        assert len(agent.persona.context_memory) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
