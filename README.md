# BranchMind

**A DFS-based AI answer search, evaluation, and synthesis system powered by Groq.**

BranchMind explores multiple possible answers to a question using Depth-First Search (DFS). It evaluates each answer, explores alternative revisions when necessary, rejects bad branches, and combines approved answers into one final response.

Run BranchMind in your terminal or use its Flask-powered website.

[![How It Works](https://img.shields.io/badge/How_It_Works-4A6CF7?style=for-the-badge)](#how-it-works)
[![Installation](https://img.shields.io/badge/Installation-2E8B57?style=for-the-badge)](#installation)
[![Terminal Version](https://img.shields.io/badge/Terminal_Version-FF8C42?style=for-the-badge)](#terminal-version)
[![Flask Website](https://img.shields.io/badge/Flask_Website-7952B3?style=for-the-badge)](#flask-website)
[![Configuration](https://img.shields.io/badge/Configuration-555555?style=for-the-badge)](#configuration)

---

## Table of Contents

- [How It Works](#how-it-works)
- [Installation](#installation)
- [Configuration](#configuration)
- [Terminal Version](#terminal-version)
- [Flask Website](#flask-website)
- [Project Structure](#project-structure)
- [Important Notes](#important-notes)
- [License](#license)

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

1. Evaluate the initial answer.
2. Generate three alternatives if the answer needs changes.
3. Explore the first alternative and its descendants.
4. Return to explore the next alternative.
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

```bash
git clone https://github.com/TechLiam-G/BranchMind.git
cd BranchMind
```

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

### 4. Install Flask

To use the website, install Flask:

```bash
python -m pip install flask
```

The terminal version does not require Flask unless it is included as a dependency of the project.

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

Keep your `.env` file private. Do not upload your real API key to GitHub.

### 3. Model configuration

The current model setting in `src/branchmind/dfs.py` is:

```python
MODEL = "openai/gpt-oss-120b"
```

Change this value if you want to use another model available to your Groq account.

---

## Terminal Version

The terminal version lets you interact with BranchMind directly through your command line.

### Run BranchMind

Make sure your virtual environment is activated and your `.env` file is configured.

From the project root, run:

```bash
python -m branchmind
```

This runs `__main__.py`, which launches the `main()` function in `cli.py`.

### Example

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

### Run the CLI another way

You can also run the CLI through its Python entry point if your package is configured for it:

```bash
python -m branchmind
```

---

## Flask Website

BranchMind also includes a web interface built with Flask. Instead of typing questions into the terminal, you can enter them in a browser and view the final answer on a webpage.

### Start the website

First, activate your virtual environment and make sure Flask is installed:

```bash
python -m pip install flask
```

Make sure your `.env` file contains your Groq API key.

Then, from the project root, run:

```bash
python app.py
```

You should see output similar to:

```text
* Running on http://127.0.0.1:5000
```

Open this address in your browser:

**http://127.0.0.1:5000**

### Using the website

1. Open the BranchMind webpage.
2. Enter a question in the text box.
3. Click **Find Better Answers**.
4. Wait for the search and synthesis process to finish.
5. Read the final answer displayed on the page.

The website also includes example questions, loading feedback, and a button to copy the final answer.

### Stop the website

Return to the terminal where Flask is running and press:

```text
Ctrl + C
```

### How the Flask version works

The Flask version uses the same DFS algorithm as the terminal version.

```text
Browser
   |
   v
app.py
   |
   v
Initial Groq Answer
   |
   v
dfs.py
   |
   v
Approved Answers
   |
   v
Groq Answer Synthesis
   |
   v
Final Answer on Webpage
```

The Flask route handles the submitted question, requests an initial answer, calls `dfs()`, combines the approved answers, and sends the final result to the HTML template.

### Terminal vs. Flask

| Feature | Terminal | Flask Website |
|---|---|---|
| Entry point | `python -m branchmind` | `python app.py` |
| Interface | Command line | Web browser |
| Input | Terminal prompt | Text box |
| Final answer | Printed in terminal | Displayed on webpage |
| DFS algorithm | Shared `dfs.py` | Shared `dfs.py` |
| Requires Flask | No | Yes |

**Important:** The Flask development server is intended for local development. Do not expose it publicly with debug mode enabled.

---

## Project Structure

The project should have a structure similar to this:

```text
BranchMind/
├── src/
│   └── branchmind/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       └── dfs.py
├── templates/
│   └── index.html
├── tests/
│   ├── __init__.py
│   └── test_dfs.py
├── app.py
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

### What Each File Does

- `app.py` — Starts the Flask website and handles webpage requests.
- `templates/index.html` — Defines the website's layout, styling, and browser interactions.
- `__init__.py` — Marks the BranchMind package directory.
- `__main__.py` — Allows BranchMind to run with `python -m branchmind`.
- `cli.py` — Accepts the user's question, requests the initial answer, runs DFS, and combines approved answers.
- `dfs.py` — Evaluates answers, creates alternative branches, tracks verdict counts, and searches the tree.
- `tests/` — Contains tests for the search algorithm.
- `.env` — Stores the private Groq API key.
- `.env.example` — Shows which environment variables are needed without exposing secrets.
- `.gitignore` — Prevents private files and generated files from being committed.
- `pyproject.toml` — Defines the Python package and its dependencies.
- `README.md` — Explains the project and how to install and run it.

---

## Important Notes

- BranchMind depends on responses from an external AI model. It does not guarantee that approved answers are correct.
- DFS determines the order in which alternatives are explored; it does not automatically make the underlying AI more accurate.
- Search depth and call limits help control API usage, but API costs and rate limits depend on your provider and account.
- The final synthesis step can combine approved answers, but it may still introduce mistakes. Verify important information independently.
- The Flask website runs the search synchronously, so the page waits for the search and synthesis steps to finish.
- The local Flask development server is not intended for production deployment.
- Keep your API key private and never commit real credentials to version control.

## License

Add your chosen open-source license here, such as the MIT License, if you decide to release BranchMind under it.
