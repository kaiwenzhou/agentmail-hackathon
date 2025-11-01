# AgentMail - Persona-Consistent Email Agent

A sophisticated email agent system that maintains consistent personality traits across all interactions.

## Overview

AgentMail is an AI-powered email agent that can respond to emails while maintaining a consistent persona. The system ensures that the agent's tone, style, and behavior remain uniform across all communications, providing a reliable and professional experience.

## Features

- **Persona Consistency**: Maintains stable personality traits across all interactions
- **Customizable Personas**: Define custom personas with specific traits, tone, and communication styles
- **Context Awareness**: Tracks conversation history to maintain consistency
- **Email Integration**: Seamlessly processes and responds to emails
- **Validation System**: Ensures responses align with defined persona characteristics

## Project Structure

```
agentmail-hackathon/
├── src/
│   ├── agent/
│   │   ├── persona.py          # Persona definition and management
│   │   ├── email_agent.py      # Main email agent implementation
│   │   └── validator.py        # Persona consistency validator
│   ├── config/
│   │   └── personas.yaml       # Persona configurations
│   └── utils/
│       └── helpers.py          # Utility functions
├── tests/
│   └── test_persona_consistency.py
├── examples/
│   └── demo.py
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from src.agent.email_agent import PersonaConsistentAgent
from src.agent.persona import Persona

# Create a persona
persona = Persona.from_file("src/config/personas.yaml", "professional")

# Initialize agent
agent = PersonaConsistentAgent(persona)

# Process an email
response = agent.respond_to_email(email_content)
```

## Persona Configuration

Personas are defined with the following attributes:

- **Name**: Identifier for the persona
- **Traits**: Core personality characteristics
- **Tone**: Communication style (formal, casual, friendly, etc.)
- **Values**: Guiding principles
- **Response Patterns**: Typical ways of structuring responses
- **Vocabulary**: Preferred words and phrases

## License

MIT License
