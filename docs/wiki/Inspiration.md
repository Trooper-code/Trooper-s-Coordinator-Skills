# Inspiration: from neural networks to an agentic workflow

## The problem
I build hobby projects with two AI agents: Claude plans and reviews, and a coding agent (Antigravity with Gemini)
does the heavy research and coding. It worked, but kept hitting the same walls:

- **Long chats got slow, expensive and forgetful.** Details from early in a chat got lost, and every new message
  cost more than the last.
- **New chats started from zero.** Starting fresh fixed the cost, but I had to re-explain everything, and things
  slipped through.
- **The two agents didn't share what they knew.** I was the only bridge between them, copying summaries back and
  forth.
- **Wrong "facts" spread.** One agent would state a guess confidently, the other would build on it, and it ended
  up in the code.

## The insight
A language model's weights don't change while you use it. Claude doesn't learn my project, and neither does Gemini.
Anything either of them "knows" about it has to be loaded into the chat every time.

So the problem isn't making the AI remember. It's **designing a memory**: deciding where it lives, what goes in it,
what gets forgotten, and how each step reads it. That's a problem neural networks have been solving for decades.

## What I borrowed

### Recurrent networks: a small state passed forward
A recurrent neural network (RNN) reads a sequence one step at a time. It doesn't keep every past input. Instead it
carries a small **hidden state** from step to step that sums up what matters so far.

That became the handoff. **Each chat is one step**, and `docs/HANDOFF.md` is the hidden state: about 100 lines of
current state and next steps, passed to the next chat. The chat doesn't need the whole history, just the state.

### LSTMs: deciding what to keep
Plain RNNs forget things they need and keep things they don't. LSTMs (Long Short-Term Memory networks) fixed that
with **gates**:
- the **forget gate** drops what's no longer useful;
- the **input gate** decides what new information gets written;
- the **output gate** decides what the next step gets to see.

Each became a handoff rule:
- **Forget:** HANDOFF.md has a size budget. Old summaries get replaced, and lessons get merged. A script enforces
  the budget.
- **Input:** findings go into the research docs first, labeled with evidence, before anything is cut from the
  handoff.
- **Output:** "First thing to do" and each prompt's "Read first" list tell the next step exactly what to load.

### External memory: big storage, small working set
Memory-augmented networks (Neural Turing Machines, Differentiable Neural Computers) and retrieval systems (RAG) keep
a large memory **outside** the model and read only the parts they need, by address.

That became the repo docs: research docs, the milestone board, and the agent's reports. The handoff and the prompts
don't copy them. They **point** to exact sections, like an address. Both agents read and write the same memory, so
neither depends on me to relay what the other found.

### Error propagation: stop bad facts early
In a recurrent network, an error in the hidden state carries into every later step. Agent workflows fail the
same way, so every finding gets a label: **confirmed** (proven), **unverified** (read, not tested) or **wrong**
(fixed where it was written). A guess can't quietly become a "fact".

## Why it works well for agentic workflows
- **Cost:** a chat re-reads its whole context every turn, so a long chat's cost grows with the square of its
  length. Short chats linked by a small handoff cut that sharply. Details: [[Memory Model]].
- **Division of labor:** the expensive model reads summaries and judges, and the cheaper agent does the
  context-heavy digging. Each spends tokens where it's strongest.
- **Continuity:** any new chat, a different model, or someone forking the repo starts from the same memory.
- **Trust:** labeled findings with evidence make review a spot-check instead of a re-investigation.

## Where the comparison stops
This is a design borrowed from neural networks, not a neural network. Nothing here is trained, and there are no
gradients. Nobody learns anything automatically. Claude follows written rules about what to keep and what to cut.

In one way, that's the advantage: a network's memory is millions of numbers nobody can read, and this memory is
plain text. You can read it, check it, correct it, and roll it back with git.

## Where to go next
- [[Memory Model]]: the technical version, with the gate mapping, the external-memory mapping and the token math.
- [[Session Handoffs]]: the handoff in practice.
- [[The Workflow]]: how it all fits together day to day.
