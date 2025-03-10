# Agents Overview

## Agent System Architecture

The Financial Analysis Agent System uses a role-based approach where each agent specializes in specific tasks:

### Base Agent
All agents inherit from the BaseAgent class, which provides:
- OpenAI integration
- Conversation memory management
- Error handling
- Common utilities

### Specialized Agents

1. **Planner Agent**
   - Research planning
   - Task organization
   - Strategy development

2. **Data Collection Agent**
   - Financial data gathering
   - API interactions
   - Data validation

3. **Research Agent**
   - Web research
   - News analysis
   - Competitor analysis

4. **Analysis Agent**
   - Financial analysis
   - Data interpretation
   - Insight generation

5. **Writer Agent**
   - Report generation
   - Content structuring
   - Data visualization

6. **Fact Check Agent**
   - Data validation
   - Citation checking
   - Quality assurance

## Agent Communication

Agents communicate through structured data formats:
- JSON for data exchange
- Markdown for report content
- Standardized error formats

## Adding New Agents

To create a new agent:

1. Inherit from BaseAgent
2. Implement required methods
3. Add to orchestrator
4. Update configuration
