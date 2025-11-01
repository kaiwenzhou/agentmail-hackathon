# AgentMail Architecture

## Overview

AgentMail is designed as a modular system for creating persona-consistent email agents. The architecture emphasizes separation of concerns and extensibility.

## Core Components

### 1. Persona System (`src/agent/persona.py`)

The Persona class is the foundation of the system, defining:

- **Attributes**: Name, traits, tone, values, vocabulary, constraints
- **Context Memory**: Tracks recent interactions for consistency
- **Serialization**: Save/load personas from YAML configuration
- **Prompt Generation**: Creates prompts for LLM integration

```python
persona = Persona(
    name="Professional Assistant",
    traits=["courteous", "efficient"],
    tone="professional",
    values=["clarity", "accuracy"]
)
```

### 2. Validation System (`src/agent/validator.py`)

The PersonaValidator ensures responses maintain persona consistency:

- **Tone Validation**: Checks if response matches expected tone
- **Vocabulary Validation**: Verifies use of preferred language
- **Constraint Validation**: Ensures behavioral rules are followed
- **Response Scoring**: Provides quantitative consistency metrics

```python
validator = PersonaValidator(persona)
result = validator.validate_response(response)
```

### 3. Email Agent (`src/agent/email_agent.py`)

The PersonaConsistentAgent orchestrates the system:

- **Email Processing**: Extracts metadata and context
- **Response Generation**: Creates persona-consistent responses
- **Context Management**: Maintains conversation history
- **Validation Integration**: Ensures quality responses

```python
agent = PersonaConsistentAgent(persona, validate_responses=True)
result = agent.respond_to_email(email_content)
```

## Data Flow

```
┌─────────────────┐
│  Incoming Email │
└────────┬────────┘
         │
         v
┌─────────────────────┐
│ Metadata Extraction │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│   Persona Context   │
│  + System Prompt    │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│ Response Generation │
│   (LLM or Template) │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│   Validation Check  │
└────────┬────────────┘
         │
         v
┌─────────────────────┐
│  Final Response +   │
│  Context Update     │
└─────────────────────┘
```

## Configuration System

Personas are defined in YAML format for easy management:

```yaml
personas:
  professional:
    traits: [courteous, efficient]
    tone: professional
    response_patterns:
      greeting: "Dear"
      closing: "Best regards"
```

## Extension Points

### 1. Custom Validators

Create custom validation logic:

```python
class CustomValidator(PersonaValidator):
    def validate_custom_rule(self, response):
        # Custom validation logic
        pass
```

### 2. LLM Integration

Replace mock response generation with real LLM:

```python
def _generate_response(self, email_content, metadata):
    system_prompt = self._build_system_prompt()
    # Call OpenAI, Anthropic, etc.
    response = llm_api.generate(system_prompt, email_content)
    return response
```

### 3. Storage Backends

Implement custom persistence:

```python
class DatabasePersonaStore:
    def save_persona(self, persona):
        # Save to database
        pass

    def load_persona(self, name):
        # Load from database
        pass
```

## Design Principles

1. **Separation of Concerns**: Each component has a single responsibility
2. **Extensibility**: Easy to add new validators, personas, or integrations
3. **Testability**: All components are independently testable
4. **Configuration-Driven**: Behavior controlled through YAML configs
5. **Type Safety**: Uses type hints throughout for better IDE support

## Future Enhancements

### Planned Features

- **Multi-language Support**: Persona consistency across languages
- **Learning System**: Improve persona from feedback
- **Advanced Context**: Better conversation thread tracking
- **Template Library**: Pre-built response templates
- **Analytics Dashboard**: Track persona performance metrics

### Integration Opportunities

- **Email Platforms**: Gmail, Outlook, SendGrid integration
- **CRM Systems**: Salesforce, HubSpot connectors
- **Chat Platforms**: Slack, Discord, Teams adapters
- **Monitoring**: Logging and observability tools

## Performance Considerations

- **Context Window**: Limited to last 10 interactions to prevent memory issues
- **Validation Caching**: Validation rules cached per persona
- **Lazy Loading**: Personas loaded on-demand
- **Async Support**: Ready for async/await patterns

## Security Considerations

- **Input Sanitization**: All email content is sanitized
- **Constraint Enforcement**: Hard limits on agent behavior
- **Audit Logging**: All interactions can be logged
- **Secret Management**: Credentials separate from configuration
