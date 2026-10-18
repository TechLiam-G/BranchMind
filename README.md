# FYI: readme.md is AI generated due to my hand hurt lmao
# BranchMind

**A DFS-based AI answer search, evaluation, and synthesis system powered by Groq.**

BranchMind explores multiple possible answers to a question using Depth-First Search (DFS). It evaluates each answer, explores alternative revisions when necessary, rejects bad branches, and combines approved answers into one final response.

[![How It Works](https://img.shields.io/badge/How_It_Works-4A6CF7?style=for-the-badge)](#how-it-works)
[![Installation](https://img.shields.io/badge/Installation-2E8B57?style=for-the-badge)](#installation)
[![Usage](https://img.shields.io/badge/Usage-FF8C42?style=for-the-badge)](#usage)
[![Configuration](https://img.shields.io/badge/Configuration-7952B3?style=for-the-badge)](#configuration)
[![Project Structure](https://img.shields.io/badge/Project_Structure-555555?style=for-the-badge)](#project-structure)

---

## How It Works

BranchMind starts with a question and an initial AI-generated answer. It then evaluates the answer and decides whether to approve it, reject it, or explore alternatives.

### The Three Verdicts

| Verdict | Meaning | Action |
|---|---|---|
| `AWESOME` | The answer is accurate, complete, and useful. | Save the answer and stop exploring that branch. |
| `NEEDS_CHANGE` | The answer could be improved. | Generate three alternative answers and explore them recursively. |
| `HORRIBLE` | The answer is too wrong or irrelevant to continue. | Reject the branch and return to its parent. |

### The Search Tree

When an answer needs changes, BranchMind asks the AI to generate three different alternatives.

For example, with `max_depth=3`:

```text
                         Question
                            |
                     Initial Answer
                         Depth 0
                            |
                +-----------+-----------+
                |           |           |
             Answer A    Answer B    Answer C
              Depth 1     Depth 1     Depth 1
                |           |           |
             +--+--+     +--+--+     +--+--+
             |  |  |     |  |  |     |  |  |
            A1 A2 A3    B1 B2 B3    C1 C2 C3
                        Depth 2
```

Each answer that receives `NEEDS_CHANGE` can produce three more alternatives, continuing until the maximum depth or call limit is reached.

**The tree only branches when an answer needs changes.** Approved and rejected answers end their respective branches immediately.

### Why Depth-First Search?

BranchMind uses DFS to explore one possible revision path before returning to explore other alternatives.

For example:

1. Evaluate the initial answer.
2. Generate three alternatives if it needs changes.
3. Explore the first alternative and its descendants.
4. Return to explore the second alternative.
5. Continue until the branches are finished or the call limit is reached.
6. Combine the approved answers into a final response.

### Search Limits

The default settings in `dfs.py` are:

- `max_depth=3`: Limits how many recursive levels the search can explore below the initial answer.
- `max_calls=40`: Limits the total number of answer evaluations.

A fully branching tree at depth 3 can evaluate up to **40 answers**: 1 initial answer, 3 at depth 1, 9 at depth 2, and 27 at depth 3.

Actual searches usually evaluate fewer answers because some branches end early.

---

## Installation

### Requirements

- Python 3.10 or newer
- A Groq API key
- Internet access for API requests

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username.

```bash
git clone https://github.com/YOUR_USERNAME/BranchMind.git
cd BranchMind
```

If your repository has a different name, use its actual URL and folder name.

### 2. Create a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 3. Install BranchMind

Run this command from the project root, where `pyproject.toml` is located:

```bash
python -m pip install -e .
```

This installs the package and its declared dependencies.

---

## Configuration

BranchMind uses Groq to generate and evaluate answers.

### 1. Get an API key

Create an API key through the [Groq Console](https://console.groq.com/).

### 2. Create your `.env` file

In the project root, create a file named `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your actual API key.

**Never commit your `.env` file or publish your API key on GitHub.** Make sure `.env` is listed in `.gitignore`.

### 3. Model configuration

The current model setting in `dfs.py` is:

```python
MODEL = "openai/gpt-oss-120b"
```

Change this value if you want to use another model available to your Groq account.

---

## Usage

Make sure your virtual environment is activated and your `.env` file is configured.

Run BranchMind from the project root:

```bash
python -m branchmind
```

The program prompts you to enter a question:

```text
Enter your question: Why does binary search run in O(log n) time?

Searching for better answers...

Approves: +1 | Changes: 1 | Denials: -0 | Calls: 1/40
Approves: +1 | Changes: 2 | Denials: -0 | Calls: 2/40
...
```

The progress output is illustrative; the actual verdicts and call counts depend on the AI responses.

After the search finishes, BranchMind combines the approved answers and prints a final response:

```text
BranchMind's final answer:

Binary search runs in O(log n) time because each step
eliminates approximately half of the remaining search space...
```

Your exact output will vary with the question and the model's responses.

---

## Project Structure

```text
BranchMind/
├── src/
│   └── branchmind/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── dfs.py
├── tests/
│   ├── __init__.py
│   └── test_dfs.py
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

### What Each File Does

- `__init__.py` — Marks the package directory.
- `__main__.py` — Allows BranchMind to run with `python -m branchmind`.
- `cli.py` — Accepts the user's question, requests the initial answer, runs DFS, and combines approved answers.
- `dfs.py` — Evaluates answers, creates alternative branches, tracks verdict counts, and searches the tree.
- `tests/` — Contains tests for the search algorithm.
- `.env` — Stores the private Groq API key.
- `.env.example` — Shows which environment variables are needed without exposing secrets.
- `.gitignore` — Prevents private files and generated files from being committed.
- `pyproject.toml` — Defines the Python package and its dependencies.

---

## Important Notes

- BranchMind depends on responses from an external AI model. It does not guarantee that approved answers are correct.
- DFS determines the order in which alternatives are explored; it does not automatically make the underlying AI more accurate.
- Search depth and call limits help control API usage, but API costs and rate limits depend on your provider and account.
- The final synthesis step can combine approved answers, but it may still introduce mistakes. Verify important information independently.

## License

Add your chosen open-source license here, such as the MIT License, if you decide to release BranchMind under it.
