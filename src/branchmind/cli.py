
import os
from groq import Groq
from .dfs import dfs, MODEL


def main():
    client = Groq()
    question = input("Enter your question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": question}
        ],
    )

    initial_answer = response.choices[0].message.content

    print("\nSearching for better answers...\n")

    good_answers = dfs(question, initial_answer)

    if not good_answers:
        print("No answers passed the filter.")
        return

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Combine the approved answers into one accurate, clear, "
                    "complete answer. Remove repetition and resolve contradictions. "
                    "Do not invent facts."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original question:\n{question}\n\n"
                    f"Approved answers:\n" +
                    "\n\n".join(good_answers)
                ),
            },
        ],
    )

    print("BranchMind's final answer:\n")
    print(response.choices[0].message.content)
