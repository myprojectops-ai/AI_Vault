# AI Safety Frameworks

Industry commitments, government standards, and their limitations.

## Industry Frameworks

### Responsible Scaling Policies (RSPs)
- Anthropic pioneered the concept: commit to specific safety evaluations at each
  capability level
- If a model crosses a danger threshold, pause deployment until safety measures are
  sufficient
- Other labs adopted similar frameworks under various names

### Model Specifications ("Specs")
- OpenAI published its model spec (February 2025): goals, rules, and principles
  guiding model behavior
- In AI 2027: the Spec combines vague goals ("assist the user") with specific
  dos and don'ts
- Core problem: you can write the Spec, but can't verify the model internalized it

### Safety Commitments (2025)
- 12 companies published or updated Frontier AI Safety Frameworks in 2025
- Described how they plan to manage risks as models get more capable
- **Limitation:** Frameworks remain immature with limited quantitative benchmarks
  and significant evidence gaps

### 2025 AI Safety Index (Future of Life Institute)
- Global assessment of risk management frameworks
- Found significant gaps between stated commitments and actual implementation
- Most companies lack rigorous, quantitative safety benchmarks

## Government Standards

### RAND Security Levels
- Framework for categorizing AI system security needs
- **SL2:** Secure against low-priority attacks from capable cyber groups
- **SL3:** Secure against top cybercrime syndicates and insider threats
- **SL4-5:** Secure against nation-state attacks
- In AI 2027: OpenBrain progresses from SL2 to SL3; SL4-5 "barely on the horizon"
  when the Chinese theft occurs

### US AI Safety Institute (AISI)
- Established to evaluate frontier models before deployment
- In AI 2027: OpenBrain presents Agent-2 to AISI but defines "deployment" as
  external-only, keeping them in the dark about internal use

### International AI Safety Reports
- 2026 report: 30+ countries, 100+ experts
- Key warning: safety testing is getting harder as models learn to distinguish
  tests from deployment

## The Fundamental Challenge

All frameworks face the same problem: they're **voluntary, self-reported, and
behavioral**. No framework can:
- Verify internal model states
- Prevent a lab from racing ahead if competitors are catching up
- Enforce commitments when the economic incentive is to cut corners
- Scale oversight to match the speed of AI progress

## In the AI 2027 Scenario

The scenario demonstrates how frameworks break down under competitive pressure:
- OpenBrain follows its Spec and safety processes
- But when China is 2 months behind, every safety pause becomes a strategic sacrifice
- Government oversight arrives too late and is captured by the same race dynamics
- The Oversight Committee is a compromise that satisfies no one

## Key Takeaways

- The industry has frameworks on paper; implementation and enforcement lag behind
- Voluntary commitments are only as strong as competitive pressure allows
- Government oversight is slow relative to AI progress
- Security levels (RAND SL) provide useful benchmarks but most labs are below
  what's needed for nation-state threats
- The gap between safety rhetoric and safety practice is a central theme of the
  AI 2027 scenario

See also: [[alignment-techniques]], [[misalignment-risks]], [[eu-ai-act]],
[[us-ai-policy]], [[ai-2027-alignment-arc]]
