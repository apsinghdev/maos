# Multi-Agent Orchestration System

## Demo

![maos Demo](./m-demo.gif)

## Architecture

![architecture](./architecture.png)

## Codebase

```
/src
  /agents              # Contains all agent logic
    master_router.py   # Coordinates all the agents
    search.py          # Search agent implementation
    intent.py          # Intent detection agent
    instruction.py     # Instruction-following agent
    conversation.py    # Conversation flow agent
    memory.py          # Memory agent (chat history/context)
  /api                 # API layer
    main.py            # FastAPI entrypoint
  /utils               # Utility modules
    caching.py         # Redis-based caching utilities
    circuit_breaker.py # Circuit breaker for service interruptions
  tests/               # Test suite

```

## Steps to run locally

1. Copy `.env.local` to `.env` and add the required environment variables.

2. Install dependencies (using pip or uv):
   ```sh
   pip install -r requirements.txt
   # or, if using uv:
   uv pip install -r requirements.txt
   ```

3. Run the app: `make run` or `uvicorn src.api.main:app --host 127.0.0.1 --port 6000 --reload`.

## Tweet

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">i&#39;ve built a multi-agent orchestrator.<br><br>agents:<br><br>&gt; master router agent<br>&gt; search agent<br>&gt; intent agent<br>&gt; instruction agent<br>&gt; conversation agent<br>&gt; memory agent<br><br>toppings:<br><br>- parallel execution<br>- worker threads for agent isolation<br>- caching for performance optimization<br>- circuit… <a href="https://t.co/KiG70kHqqt">https://t.co/KiG70kHqqt</a> <a href="https://t.co/bX5A9BXFOB">pic.twitter.com/bX5A9BXFOB</a></p>&mdash; Ajeet (opensox.in) (@ajeetunc) <a href="https://twitter.com/ajeetunc/status/1939904295044010472?ref_src=twsrc%5Etfw">July 1, 2025</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
