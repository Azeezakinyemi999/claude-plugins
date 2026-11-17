# The ten strategies as a sequence

Run the strategies in this order when the learner wants the full method. Each
step gives them something to use in the next one, from a first intuitive
explanation to the questions they'll review later. How to run each strategy
is in [strategies.md](strategies.md).

## The order

| Step | Name | Strategy | What the learner does, and what carries forward |
| --- | --- | --- | --- |
| 1 | Get oriented | ELI5 | Gets a simple explanation and writes the main idea in one sentence. |
| 2 | Pick what to learn first | 80/20 | Chooses the few concepts needed to explain that sentence properly. |
| 3 | Organize the topic | Mind map | Puts the topic in the center, branches into its parts, and marks the connections they can't yet explain. |
| 4 | Draw the system | Schematic | Sketches the system and labels boundaries, flows, where conditions are imposed and where things are measured. |
| 5 | Build the explanation | First principles | Uses the sketch to reason from basic facts to the governing law. |
| 6 | Challenge the explanation | Socratic questioning | Asks what step 5 assumed, and where each assumption holds or breaks down. |
| 7 | Teach it back | Feynman technique | Explains the whole process with notes closed, and fixes each place they get stuck. |
| 8 | Create a reference | Visual study guide | Puts the corrected explanation, schematic, equations and a plot on one page. |
| 9 | Check recall and application | Quiz me | Puts the guide away and answers a recall question, then a new application question. |
| 10 | Revisit what was missed | Sticky notes | Turns each missed question into a prompt with the answer hidden, reviewed tomorrow and a few days later. |

**The quiz says where to go back:**

- forgot an equation → make a sticky note;
- remembered the equation but couldn't explain why it applies → return to
  first principles (step 5);
- solved the problem but struggled to explain it clearly → teach it back
  again (step 7).

## Worked example: transient diffusion through a metal wall

Use this to calibrate depth and format. The topic is hydrogen entering a metal
wall and diffusing through it until a steady state is reached.

1. **ELI5.** Explain what happens when hydrogen first enters a metal wall.
   For example: hydrogen atoms crowd in at the surface and wander randomly
   between the metal atoms; because more of them are near the entry side,
   more wander inward than back, so the hydrogen gradually spreads through
   the wall. The learner writes one sentence, such as "Hydrogen spreads
   through the wall from where there's more of it to where there's less,
   until the flow in balances the flow out."
2. **80/20.** Learn first: concentration gradients, diffusivity, and how
   concentration changes with time. Later: trapping, surface reaction
   kinetics, stress-driven diffusion.
3. **Mind map.** Transient diffusion in the center. Branches: physical
   mechanism, governing equation, initial and boundary conditions, outputs
   (concentration profiles, exit flux, time lag). Mark the links the learner
   can't yet explain, e.g. `?` boundary conditions → time to steady state.
4. **Schematic.** Draw the wall with its two surfaces, x = 0 (entry) and
   x = L (exit), and the direction of hydrogen transport. Label where each
   boundary condition is imposed and where the flux is measured (the exit
   face).
5. **First principles.** Take a thin slice of the wall. If more hydrogen
   enters the slice than leaves, its concentration rises. Connect that mass
   balance to Fick's first law to get the governing equation (see the answer
   key).
6. **Socratic questioning.** Ask what step 5 assumed. "What changes if
   diffusivity varies through the wall?" "What sets the concentration at the
   entry surface?" "What if some hydrogen gets trapped at defects?" Follow
   each answer with a question about why it holds or where it breaks down.
7. **Feynman.** With notes closed, the learner explains the process from the
   first moment hydrogen enters the wall to steady state. When they get stuck,
   go back to the specific idea, then try again.
8. **Visual study guide.** One page with the corrected explanation, the
   schematic, the governing equation, and a plot of concentration profiles at
   several times, rising toward the straight steady-state line.
9. **Quiz me.** A recall question ("Write the equation for transient
   diffusion with constant D and define each symbol"), then an application
   question ("If the wall thickness doubles and diffusivity stays fixed, how
   does the characteristic diffusion time change?").
10. **Sticky notes.** Each missed question becomes a prompt with the answer
    hidden, due tomorrow, then a few days later.

### Answer key (for Claude; don't show it before the learner answers)

- Mass balance on a slice: ∂C/∂t = −∂J/∂x.
- Fick's first law: J = −D ∂C/∂x. The minus sign means the flux runs down the
  gradient.
- With constant D they combine into Fick's second law: ∂C/∂t = D ∂²C/∂x².
- If D varies with position: ∂C/∂t = ∂/∂x (D ∂C/∂x).
- A common permeation setup: no hydrogen in the wall at t = 0; the entry face
  is held at C₀ and the exit face near C = 0. If the surface reactions are fast,
  C₀ follows Sieverts' law, C₀ = S√p (S is the solubility, p the H₂ partial
  pressure).
- Steady state with constant D: a linear profile, and exit flux J_ss = D·C₀/L.
- Characteristic diffusion time τ ~ L²/D, so doubling L makes it four times
  longer.
- For the setup above, the permeation time lag is t_lag = L²/(6D).
- Assumptions worth probing in step 6: constant D, no trapping (traps slow the
  approach to steady state), surface concentration fixed instantly
  (diffusion-limited rather than surface-limited), one-dimensional transport
  (a wall thin compared with its width), constant temperature, no stress
  effects.

## Templates

### `progress.md`

```markdown
# <Topic> — learning progress

- **Goal:** <why they're learning it>
- **Starting point:** <what they already knew>
- **Depth:** intuition | working use | derivation
- **One-sentence idea:** <from step 1, refined as they go>
- **Step reached:** <N — strategy> (next: <N+1 — strategy>)
- **Go back to:** <steps the last quiz routed to, or "none">
- **Unsure:** <facts marked UNSURE, and what would settle each>
- **Started:** <YYYY-MM-DD> · **Last session:** <YYYY-MM-DD>
```

### `notes.md`

```markdown
# <Topic> — notes

## Step 1 — ELI5
<explanation, the analogy's limit, the learner's one-sentence idea>

## Step 2 — 80/20
Learn first: <…>
Later: <…>

<one section per step, or `## <Strategy> — <YYYY-MM-DD>` for a standalone
strategy; append, never rewrite earlier sections>
```
