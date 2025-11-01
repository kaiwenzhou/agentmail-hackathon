"""
Persona Management System

This module defines the Persona class and related utilities for managing
consistent AI agent personalities.
"""

from typing import Dict, List, Optional, Any
import yaml
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Persona:
    """
    Represents a consistent AI agent persona with defined traits and behaviors.

    Attributes:
        name: Unique identifier for the persona
        traits: Core personality characteristics (e.g., friendly, professional, analytical)
        tone: Communication style (e.g., formal, casual, empathetic)
        values: Guiding principles and priorities
        response_patterns: Typical ways of structuring responses
        vocabulary: Preferred words, phrases, and expressions
        constraints: Behavioral boundaries and restrictions
        context_memory: Stores interaction history for consistency
    """
    name: str
    traits: List[str] = field(default_factory=list)
    tone: str = "neutral"
    values: List[str] = field(default_factory=list)
    response_patterns: Dict[str, str] = field(default_factory=dict)
    vocabulary: Dict[str, List[str]] = field(default_factory=dict)
    constraints: List[str] = field(default_factory=list)
    context_memory: List[Dict[str, Any]] = field(default_factory=list)

    def add_context(self, interaction: Dict[str, Any]) -> None:
        """
        Add an interaction to the persona's context memory.

        Args:
            interaction: Dictionary containing interaction details
                (e.g., {'type': 'email', 'content': '...', 'response': '...'})
        """
        self.context_memory.append(interaction)

        # Keep only the last 10 interactions to prevent memory overflow
        if len(self.context_memory) > 10:
            self.context_memory = self.context_memory[-10:]

    def get_context_summary(self) -> str:
        """
        Generate a summary of recent interactions for context.

        Returns:
            String summary of recent conversation history
        """
        if not self.context_memory:
            return "No previous interactions."

        summary_parts = []
        for i, interaction in enumerate(self.context_memory[-5:], 1):
            interaction_type = interaction.get('type', 'unknown')
            summary_parts.append(f"{i}. {interaction_type}: {interaction.get('summary', 'N/A')}")

        return "\n".join(summary_parts)

    def get_persona_prompt(self) -> str:
        """
        Generate a prompt description of this persona for use with AI models.

        Returns:
            Detailed string description of the persona's characteristics
        """
        prompt_parts = [
            f"You are {self.name}, an AI assistant with the following characteristics:\n"
        ]

        if self.traits:
            prompt_parts.append(f"Personality Traits: {', '.join(self.traits)}")

        if self.tone:
            prompt_parts.append(f"Communication Tone: {self.tone}")

        if self.values:
            prompt_parts.append(f"Core Values: {', '.join(self.values)}")

        if self.constraints:
            prompt_parts.append(f"\nBehavioral Guidelines:")
            for constraint in self.constraints:
                prompt_parts.append(f"- {constraint}")

        if self.response_patterns:
            prompt_parts.append(f"\nResponse Patterns:")
            for pattern_type, pattern in self.response_patterns.items():
                prompt_parts.append(f"- {pattern_type}: {pattern}")

        if self.vocabulary:
            prompt_parts.append(f"\nPreferred Language:")
            for category, words in self.vocabulary.items():
                prompt_parts.append(f"- {category}: {', '.join(words[:5])}")  # Show first 5 words

        return "\n".join(prompt_parts)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert persona to dictionary format.

        Returns:
            Dictionary representation of the persona
        """
        return {
            'name': self.name,
            'traits': self.traits,
            'tone': self.tone,
            'values': self.values,
            'response_patterns': self.response_patterns,
            'vocabulary': self.vocabulary,
            'constraints': self.constraints,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Persona':
        """
        Create a Persona instance from a dictionary.

        Args:
            data: Dictionary containing persona configuration

        Returns:
            Persona instance
        """
        return cls(
            name=data.get('name', 'Unknown'),
            traits=data.get('traits', []),
            tone=data.get('tone', 'neutral'),
            values=data.get('values', []),
            response_patterns=data.get('response_patterns', {}),
            vocabulary=data.get('vocabulary', {}),
            constraints=data.get('constraints', []),
        )

    @classmethod
    def from_file(cls, filepath: str, persona_name: str) -> 'Persona':
        """
        Load a persona from a YAML configuration file.

        Args:
            filepath: Path to the YAML configuration file
            persona_name: Name of the persona to load from the file

        Returns:
            Persona instance

        Raises:
            FileNotFoundError: If the file doesn't exist
            KeyError: If the persona name isn't found in the file
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {filepath}")

        with open(path, 'r') as f:
            config = yaml.safe_load(f)

        if 'personas' not in config:
            raise KeyError("Configuration file must contain a 'personas' section")

        personas = config['personas']
        if persona_name not in personas:
            available = ', '.join(personas.keys())
            raise KeyError(
                f"Persona '{persona_name}' not found. Available personas: {available}"
            )

        persona_data = personas[persona_name]
        persona_data['name'] = persona_name

        return cls.from_dict(persona_data)

    def save_to_file(self, filepath: str) -> None:
        """
        Save persona to a YAML configuration file.

        Args:
            filepath: Path where the configuration should be saved
        """
        path = Path(filepath)

        # Load existing config or create new one
        if path.exists():
            with open(path, 'r') as f:
                config = yaml.safe_load(f) or {}
        else:
            config = {}

        if 'personas' not in config:
            config['personas'] = {}

        config['personas'][self.name] = self.to_dict()

        with open(path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
