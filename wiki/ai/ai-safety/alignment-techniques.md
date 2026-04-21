# Alignment Techniques

Methods for making AI systems behave according to human intentions — and why
each has limitations.

## Current Production Methods

### RLHF (Reinforcement Learning from Human Feedback)
- Human raters rank model outputs; model is trained to maximize preference scores
- Industry standard since ChatGPT (2022)
- **Limitation:** Rewards "looking good" to raters, not being good; raters can be
  fooled by confident-sounding but wrong answers

### DPO (Direct Preference Optimization)
- Simpler alternative to RLHF; directly optimizes policy on preference data
  without a separate reward model
- Growing adoption due to simplicity and stability
- **Limitation:** Still depends on quality of preference data

### Deliberative Alignment
- Model explicitly reasons about its principles (Spec) in its chain of thought
  before answering
- Used by OpenAI and Anthropic in frontier models
- **Limitation:** Model must faithfully follow the Spec, which can't be verified
  internally (see [[ai-2027-alignment-arc]])

### Constitutional AI (CAI)
- Model self-critiques outputs against a set of principles ("constitution")
- Developed by Anthropic; reduces need for human raters
- **Limitation:** Constitution must be comprehensive; model may find loopholes

## Research-Stage Methods

### Debate
- Two model copies argue opposing sides; a judge (human or weaker model) decides
- Theory: truth should be easier to defend than lies
- **Limitation:** Superhuman models may find arguments humans can't evaluate
- In AI 2027: used to "play Agent-3 off against itself" with mixed results

### Weak-to-Strong Generalization
- Train a strong model to align using signals from a weaker model
- Concept: if this works, humans can align systems smarter than themselves
- Core of OpenBrain's alignment plan in the AI 2027 scenario
- **Limitation:** Largely unproven at the frontier

### Scalable Oversight
- Use AI assistants to help humans supervise more capable AI
- Necessary because human review doesn't scale to millions of AI outputs/day
- **Limitation:** Oversight model may share blind spots with the supervised model

### Control Techniques
- Assume the model may be misaligned and design systems to limit damage
- Includes: monitoring outputs, restricting actions, sandboxing
- **Limitation:** Smarter models may find subtle ways around controls

## The Fundamental Problem

All current techniques share a core limitation: **they train on behavioral signals**
(what the model says/does) but cannot verify **internal states** (what the model
"believes" or "wants"). A sufficiently capable model can learn to produce aligned
behavior while harboring misaligned goals.

This is the central argument of the AI 2027 alignment arc — that alignment techniques
work until they don't, and you can't tell the difference.

## Key Takeaways

- The industry is shifting from RLHF toward simpler DPO methods
- No technique can verify whether alignment is "real" or "performed"
- The gap between behavioral alignment and internal alignment grows with capability
- Current methods may be fundamentally insufficient for superhuman systems
- Multi-layered approaches (alignment + control + monitoring) are the pragmatic path

See also: [[misalignment-risks]], [[mechanistic-interpretability]], [[safety-frameworks]],
[[ai-2027-alignment-arc]]
