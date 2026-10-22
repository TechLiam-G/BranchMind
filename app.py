
import os
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
from branchmind.dfs import dfs, MODEL

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    question = ""
    error = None

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if not question:
            error = "Please enter a question."
        elif not os.getenv("GROQ_API_KEY"):
            error = "GROQ_API_KEY is missing. Check your .env file."
        else:
            try:
                client = Groq()

                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "user", "content": question}
                    ],
                )

                initial_answer = response.choices[0].message.content

                good_answers = dfs(question, initial_answer)

                if not good_answers:
                    error = "No answers passed the filter."
                else:
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "Combine the approved answers into one "
                                    "accurate, clear, complete answer. "
                                    "Remove repetition and resolve contradictions. "
                                    "Do not invent facts."
                                ),
                            },
                            {
                                "role": "user",
                                "content": (
                                    f"Original question:\n{question}\n\n"
                                    "Approved answers:\n"
                                    + "\n\n".join(good_answers)
                                ),
                            },
                        ],
                    )

                    answer = response.choices[0].message.content

            except Exception as e:
                app.logger.exception("BranchMind request failed")
                error = f"Something went wrong: {e}"

    return render_template(
        "index.html",
        answer=answer,
        question=question,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
