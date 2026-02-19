# CognitionOS

**AI Memory-Driven Multi-Agent Knowledge Operating System**

CognitionOS is a production-grade multi-agent AI operating system built using **LangChain**, **LangGraph**, and **MCP**. It simulates a structured cognitive architecture with semantic, episodic, tool, and strategy memory layers, enabling autonomous agents to collaborate, reflect, and evolve.

## Architecture

CognitionOS uses a **Memory Matrix** to provide context to a swarm of specialized agents:

-   **Orchestrator**: LangGraph-based state machine.
-   **Agents**: Planner, Researcher, Coder, Reviewer.
-   **Memory**:
    -   *Semantic*: ChromaDB (Vector Knowledge)
    -   *Episodic*: PostgreSQL (Task Logs)
    -   *Tool*: Redis (Performance Tracking)
    -   *Strategy*: Meta-learning patterns.

## Getting Started

### Prerequisites

-   Python 3.10+
-   Docker & Docker Compose

### Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Set up environment variables:
    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```

### Running Infrastructure

Start the databases (Postgres, Redis, Chroma):

```bash
docker-compose up -d
```
