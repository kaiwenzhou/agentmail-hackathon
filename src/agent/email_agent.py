"""
Persona-Consistent Email Agent

This module implements an email agent that maintains consistent personality
traits across all email interactions.
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime
from src.agent.persona import Persona
from src.agent.validator import PersonaValidator


class PersonaConsistentAgent:
    """
    An email agent that maintains consistent persona characteristics across interactions.
    """

    def __init__(self, persona: Persona, validate_responses: bool = True):
        """
        Initialize the agent with a persona.

        Args:
            persona: The Persona instance defining the agent's personality
            validate_responses: Whether to validate responses for consistency
        """
        self.persona = persona
        self.validator = PersonaValidator(persona) if validate_responses else None
        self.validate_responses = validate_responses

    def _build_system_prompt(self) -> str:
        """
        Build the system prompt that defines the agent's persona.

        Returns:
            System prompt string
        """
        base_prompt = self.persona.get_persona_prompt()

        additional_instructions = """

Remember to:
1. Stay completely in character at all times
2. Maintain consistency with previous interactions
3. Follow all behavioral guidelines strictly
4. Use the communication style and tone defined above

When responding to emails:
- Be clear and concise
- Address all points raised in the email
- Maintain your personality throughout
- Use appropriate greetings and closings
"""

        context = self.persona.get_context_summary()
        if context != "No previous interactions.":
            additional_instructions += f"\n\nRecent conversation context:\n{context}"

        return base_prompt + additional_instructions

    def _extract_email_metadata(self, email_content: str) -> Dict[str, Any]:
        """
        Extract metadata from an email.

        Args:
            email_content: The email content to analyze

        Returns:
            Dictionary containing email metadata
        """
        lines = email_content.strip().split('\n')

        metadata = {
            'subject': '',
            'sender': '',
            'timestamp': datetime.now().isoformat(),
            'content': email_content,
            'question_count': email_content.count('?'),
            'urgency_indicators': [],
        }

        # Simple heuristic detection
        urgency_words = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        for word in urgency_words:
            if word.lower() in email_content.lower():
                metadata['urgency_indicators'].append(word)

        # Try to extract subject if formatted as "Subject: ..."
        for line in lines[:5]:  # Check first 5 lines
            if line.lower().startswith('subject:'):
                metadata['subject'] = line[8:].strip()
                break

        return metadata

    def _generate_response(self, email_content: str, metadata: Dict[str, Any]) -> str:
        """
        Generate a response to an email while maintaining persona consistency.

        This is a simplified implementation. In a real system, this would
        integrate with an LLM API like OpenAI or Anthropic.

        Args:
            email_content: The email to respond to
            metadata: Email metadata

        Returns:
            Generated response string
        """
        # This is a mock implementation
        # In a real system, you would call an LLM API here with the system prompt

        system_prompt = self._build_system_prompt()

        # For demonstration, create a template-based response
        greeting = self.persona.response_patterns.get('greeting', 'Hello')
        closing = self.persona.response_patterns.get('closing', 'Best regards')

        # Build response based on persona tone
        if self.persona.tone == 'formal':
            response = f"{greeting},\n\nThank you for your email. "
        elif self.persona.tone == 'casual':
            response = f"{greeting}!\n\nThanks for reaching out! "
        elif self.persona.tone == 'friendly':
            response = f"{greeting}!\n\nGreat to hear from you! "
        else:
            response = f"{greeting},\n\nThank you for your message. "

        # Add content acknowledgment
        if metadata['question_count'] > 0:
            response += "I'll be happy to address your questions.\n\n"
        else:
            response += "I've received your message.\n\n"

        # Add urgency acknowledgment if needed
        if metadata['urgency_indicators']:
            response += "I understand this is time-sensitive and will prioritize accordingly.\n\n"

        # Mock content response
        response += (
            "I'll need to review the details you've provided. "
            "Let me get back to you with a comprehensive response shortly."
        )

        # Add closing
        response += f"\n\n{closing},\n{self.persona.name}"

        return response

    def respond_to_email(
        self,
        email_content: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Generate a persona-consistent response to an email.

        Args:
            email_content: The email content to respond to
            max_retries: Maximum number of retries if validation fails

        Returns:
            Dictionary containing the response and metadata
        """
        metadata = self._extract_email_metadata(email_content)

        response = None
        validation_result = None
        attempts = 0

        while attempts < max_retries:
            attempts += 1

            # Generate response
            response = self._generate_response(email_content, metadata)

            # Validate if enabled
            if self.validate_responses:
                validation_result = self.validator.validate_response(response)

                if validation_result['is_valid']:
                    break
                elif attempts < max_retries:
                    # In a real system, we would regenerate with feedback
                    # For now, we'll just continue with the response
                    pass
            else:
                break

        # Store interaction in context
        interaction = {
            'type': 'email',
            'timestamp': metadata['timestamp'],
            'summary': f"Responded to email re: {metadata.get('subject', 'N/A')}",
            'content': email_content[:100],  # Store first 100 chars
            'response': response[:100],
        }
        self.persona.add_context(interaction)

        # Build result
        result = {
            'response': response,
            'metadata': metadata,
            'attempts': attempts,
            'persona': self.persona.name,
        }

        if validation_result:
            result['validation'] = validation_result

        return result

    def get_persona_summary(self) -> str:
        """
        Get a summary of the current persona.

        Returns:
            String description of the persona
        """
        summary_parts = [
            f"Agent: {self.persona.name}",
            f"Tone: {self.persona.tone}",
        ]

        if self.persona.traits:
            summary_parts.append(f"Traits: {', '.join(self.persona.traits)}")

        if self.persona.values:
            summary_parts.append(f"Values: {', '.join(self.persona.values)}")

        interactions = len(self.persona.context_memory)
        summary_parts.append(f"Interactions: {interactions}")

        return "\n".join(summary_parts)

    def update_persona(self, **kwargs) -> None:
        """
        Update persona attributes dynamically.

        Args:
            **kwargs: Persona attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self.persona, key):
                setattr(self.persona, key, value)

        # Reinitialize validator with updated persona
        if self.validate_responses:
            self.validator = PersonaValidator(self.persona)

    def analyze_consistency(self) -> Dict[str, Any]:
        """
        Analyze the consistency of the agent's recent responses.

        Returns:
            Dictionary with consistency metrics
        """
        if not self.persona.context_memory:
            return {
                'total_interactions': 0,
                'message': 'No interactions to analyze'
            }

        total = len(self.persona.context_memory)

        return {
            'total_interactions': total,
            'persona_name': self.persona.name,
            'tone': self.persona.tone,
            'traits': self.persona.traits,
            'message': f'Agent has maintained {self.persona.name} persona across {total} interactions'
        }
