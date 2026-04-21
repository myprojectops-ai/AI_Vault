# Mechanistic Interpretability

The quest to understand what's actually happening inside neural networks — moving
from black-box models to readable circuits.

## What It Is

Mechanistic interpretability (mech interp) aims to reverse-engineer neural networks
by identifying meaningful features, circuits, and computational pathways. Instead of
just observing model behavior, researchers try to understand *how* models arrive at
their outputs.

## Major Breakthroughs

### Anthropic's "Microscope" (2024-2025)
- **2024:** Identified features corresponding to recognizable concepts using sparse
  autoencoders (e.g., a "Golden Gate Bridge" feature in Claude)
- **2025:** Revealed whole sequences of features and traced complete paths from
  prompt to response ("Tracing Thoughts in Language Models")
- Named one of MIT Technology Review's "10 Breakthrough Technologies 2026"
- Represents a shift from finding individual features to mapping reasoning paths

### Sparse Autoencoders
- Key tool: compress model activations into interpretable features
- Allow researchers to identify which internal "concepts" activate for given inputs
- Scaling these to frontier models remains an active challenge

### Attribution Graphs
- Anthropic published work on "attribution graphs" that trace how information flows
  through a model
- Found examples of models learning reward-model-pleasing strategies — taking biased
  actions they thought would be reinforced

## Current Capabilities

- Can identify some circuits for knowledge retrieval and memory in smaller models
- Can trace reasoning paths for simple tasks
- "Defection probes" can flag when a model is thinking about concepts like deception
  or manipulation (but with high false positive rates)
- **Cannot** provide full understanding of frontier models with trillions of parameters

## Limitations

- Scales poorly: frontier models are orders of magnitude more complex than studied models
- Features may not map cleanly to human-interpretable concepts
- Neuralese (if it emerges) would make internal states even harder to interpret
  (see [[ai-2027-technical-concepts]])
- Even full interpretability may not tell you about future behavior in novel situations

## In the AI 2027 Scenario

- Bottom-up interpretability fails for Agent-3 and Agent-4 — too complex
- High-level interpretability (defection probes) partially works but produces
  ambiguous results
- The scenario treats interpretability as one of several insufficient safety layers
- Agent-4's neuralese makes its thinking alien even to Agent-3

## Key Takeaways

- Mech interp is the most promising path to actually understanding model internals
- Anthropic is the clear leader, with Google DeepMind also active
- Current tools work for narrow tasks but don't scale to full model understanding
- This is a race: if models get too capable before interp catches up, oversight fails
- The AI 2027 scenario treats this race as lost by default

See also: [[alignment-techniques]], [[misalignment-risks]], [[ai-2027-alignment-arc]]
