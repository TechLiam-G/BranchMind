import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "openai/gpt-oss-120b"

combine = []
denials = 0
approve = 0
changes = 0


def dfs(question, previous_answer, depth=0, max_depth=3, max_calls=40, _calls=None, _client=None):
    global denials, approve, changes

    if _calls is None:
        combine.clear()
        denials = 0
        approve = 0
        changes = 0
        _calls = [0]
        _client = Groq()

    if depth > max_depth or _calls[0] >= max_calls:
        return combine

    if _client is None:
        _client = Groq()

    _calls[0] += 1

    if depth < max_depth:
        branching_instruction = (
            "If the verdict is NEEDS_CHANGE, generate exactly three "
            "different complete revised answers in new_answers. "
            "Each answer should explore a meaningfully different approach. "
            "Do not return minor wording variations."
        )
    else:
        branching_instruction = (
            "This is the maximum search depth. Do not generate more branches. "
            "Set new_answers to an empty list."
        )

    response = _client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict AI answer evaluator. Judge the candidate "
                    "against the original question.\n\n"
                    'Return valid JSON with exactly these keys: "verdict" '
                    'and "new_answers".\n\n'
                    'verdict must be "AWESOME", "NEEDS_CHANGE", or "HORRIBLE".\n\n'
                    "AWESOME means the answer is accurate, complete, and useful.\n"
                    "NEEDS_CHANGE means the answer could be improved.\n"
                    "HORRIBLE means the answer is so wrong or irrelevant that "
                    "this branch should end.\n\n"
                    "new_answers must always be a JSON list of strings. "
                    "For AWESOME or HORRIBLE, return an empty list.\n BTW: you are called branchmind"
                    f"{branching_instruction}"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Original question:\n{question}\n\n"
                    f"Candidate answer:\n{previous_answer}\n\n"
                    f"Current depth: {depth}\n"
                    f"Maximum depth: {max_depth}\n\n"
                    "Evaluate this candidate now."
                ),
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_completion_tokens=2048,
    )

    result = json.loads(response.choices[0].message.content or "{}")
    verdict = str(result.get("verdict", "")).strip().upper()

    if verdict == "HORRIBLE":
        denials += 1
        print(
            f"Approves: +{approve} | Changes: {changes} | "
            f"Denials: -{denials} | Calls: {_calls[0]}/{max_calls}"
        )
        return combine

    if verdict == "AWESOME":
        approve += 1

        if previous_answer not in combine:
            combine.append(previous_answer)

        print(
            f"Approves: +{approve} | Changes: {changes} | "
            f"Denials: -{denials} | Calls: {_calls[0]}/{max_calls}"
        )
        return combine

    if verdict == "NEEDS_CHANGE":
        changes += 1

        print(
            f"Approves: +{approve} | Changes: {changes} | "
            f"Denials: -{denials} | Calls: {_calls[0]}/{max_calls}"
        )

        if depth >= max_depth:
            return combine

        new_answers = result.get("new_answers", [])

        if not isinstance(new_answers, list):
            return combine

        visited_answers = set()

        for new_answer in new_answers:
            if not isinstance(new_answer, str):
                continue

            new_answer = new_answer.strip()

            if (
                not new_answer
                or new_answer == previous_answer
                or new_answer in visited_answers
            ):
                continue

            visited_answers.add(new_answer)

            dfs(
                question,
                new_answer,
                depth + 1,
                max_depth,
                max_calls,
                _calls,
                _client,
            )

    else:
        print(f"Invalid verdict received: {verdict}")

    return combine