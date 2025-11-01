"""
Persona Consistency Validator

This module provides tools to validate that agent responses are consistent
with the defined persona characteristics.
"""

from typing import List, Dict, Any, Tuple
import re
from src.agent.persona import Persona


class PersonaValidator:
    """
    Validates agent responses for consistency with defined persona traits.
    """

    def __init__(self, persona: Persona):
        """
        Initialize the validator with a persona.

        Args:
            persona: The Persona instance to validate against
        """
        self.persona = persona

    def validate_tone(self, response: str) -> Tuple[bool, str]:
        """
        Check if the response matches the expected tone.

        Args:
            response: The agent's response text

        Returns:
            Tuple of (is_valid, explanation)
        """
        tone = self.persona.tone.lower()
        response_lower = response.lower()

        # Define tone indicators
        tone_indicators = {
            'formal': {
                'positive': ['hereby', 'kindly', 'sincerely', 'respectfully', 'regards'],
                'negative': ['yeah', 'gonna', 'wanna', 'hey', 'sup'],
            },
            'casual': {
                'positive': ['hey', 'thanks', 'cool', 'sounds good', 'no problem'],
                'negative': ['hereby', 'aforementioned', 'pursuant to'],
            },
            'friendly': {
                'positive': ['happy to', 'glad', 'great', 'love to', 'excited'],
                'negative': ['regrettably', 'unfortunately', 'must decline'],
            },
            'professional': {
                'positive': ['please', 'thank you', 'appreciate', 'regards', 'best'],
                'negative': ['lol', 'omg', 'tbh', 'idk'],
            },
        }

        if tone in tone_indicators:
            indicators = tone_indicators[tone]
            positive_count = sum(1 for word in indicators['positive'] if word in response_lower)
            negative_count = sum(1 for word in indicators['negative'] if word in response_lower)

            if negative_count > 0:
                return False, f"Response contains language inconsistent with {tone} tone"

            if positive_count > 0:
                return True, f"Response matches {tone} tone"

            return True, f"Response is neutral, acceptable for {tone} tone"

        return True, "Tone validation not available for this persona"

    def validate_vocabulary(self, response: str) -> Tuple[bool, str]:
        """
        Check if the response uses preferred vocabulary.

        Args:
            response: The agent's response text

        Returns:
            Tuple of (is_valid, explanation)
        """
        if not self.persona.vocabulary:
            return True, "No vocabulary preferences defined"

        response_lower = response.lower()
        used_preferred = []

        for category, words in self.persona.vocabulary.items():
            for word in words:
                if word.lower() in response_lower:
                    used_preferred.append(word)

        if used_preferred:
            return True, f"Uses preferred vocabulary: {', '.join(used_preferred[:3])}"

        # Not using preferred vocabulary isn't necessarily wrong, just neutral
        return True, "Vocabulary is acceptable"

    def validate_constraints(self, response: str) -> Tuple[bool, List[str]]:
        """
        Check if the response violates any defined constraints.

        Args:
            response: The agent's response text

        Returns:
            Tuple of (is_valid, list of violations)
        """
        violations = []
        response_lower = response.lower()

        for constraint in self.persona.constraints:
            # Parse constraints (simple keyword-based checks)
            if constraint.lower().startswith("never "):
                forbidden_phrase = constraint[6:].lower()
                if forbidden_phrase in response_lower:
                    violations.append(f"Violated constraint: {constraint}")

            elif constraint.lower().startswith("always "):
                required_phrase = constraint[7:].lower()
                # This is harder to validate without context, so we'll skip for now
                pass

        return len(violations) == 0, violations

    def validate_response_length(self, response: str, expected_pattern: str = "concise") -> Tuple[bool, str]:
        """
        Validate response length against expected pattern.

        Args:
            response: The agent's response text
            expected_pattern: Expected length pattern (concise, detailed, brief)

        Returns:
            Tuple of (is_valid, explanation)
        """
        word_count = len(response.split())

        patterns = {
            'brief': (10, 50),
            'concise': (30, 150),
            'detailed': (100, 500),
            'comprehensive': (200, 1000),
        }

        if expected_pattern in patterns:
            min_words, max_words = patterns[expected_pattern]

            if word_count < min_words:
                return False, f"Response too short for {expected_pattern} pattern ({word_count} words)"
            elif word_count > max_words:
                return False, f"Response too long for {expected_pattern} pattern ({word_count} words)"
            else:
                return True, f"Response length appropriate for {expected_pattern} pattern"

        return True, "No length validation performed"

    def validate_response(self, response: str) -> Dict[str, Any]:
        """
        Perform comprehensive validation of a response.

        Args:
            response: The agent's response text

        Returns:
            Dictionary with validation results
        """
        results = {
            'is_valid': True,
            'checks': {},
            'violations': [],
            'score': 100.0,
        }

        # Tone check
        tone_valid, tone_msg = self.validate_tone(response)
        results['checks']['tone'] = {'valid': tone_valid, 'message': tone_msg}
        if not tone_valid:
            results['is_valid'] = False
            results['violations'].append(tone_msg)
            results['score'] -= 30

        # Vocabulary check
        vocab_valid, vocab_msg = self.validate_vocabulary(response)
        results['checks']['vocabulary'] = {'valid': vocab_valid, 'message': vocab_msg}

        # Constraints check
        constraints_valid, constraint_violations = self.validate_constraints(response)
        results['checks']['constraints'] = {
            'valid': constraints_valid,
            'violations': constraint_violations
        }
        if not constraints_valid:
            results['is_valid'] = False
            results['violations'].extend(constraint_violations)
            results['score'] -= 40

        # Response pattern check
        if 'greeting' in self.persona.response_patterns:
            expected_pattern = self.persona.response_patterns.get('length', 'concise')
            length_valid, length_msg = self.validate_response_length(response, expected_pattern)
            results['checks']['length'] = {'valid': length_valid, 'message': length_msg}

        return results

    def get_improvement_suggestions(self, response: str) -> List[str]:
        """
        Generate suggestions for improving persona consistency.

        Args:
            response: The agent's response text

        Returns:
            List of improvement suggestions
        """
        suggestions = []
        validation = self.validate_response(response)

        if not validation['is_valid']:
            for violation in validation['violations']:
                suggestions.append(f"Fix: {violation}")

        # Suggest using preferred vocabulary
        if self.persona.vocabulary and validation['checks']['vocabulary']['valid']:
            vocab_categories = list(self.persona.vocabulary.keys())
            if vocab_categories:
                suggestions.append(
                    f"Consider using more words from preferred categories: {', '.join(vocab_categories)}"
                )

        return suggestions
