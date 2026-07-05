import gradio as gr
from research_manager import ResearchManager

manager = ResearchManager()


async def start_clarification(query: str):
    if not query.strip():
        return gr.update(), [], [], 0, "", ""

    clarifications = await manager.get_clarifications(query)
    questions = clarifications.questions

    if not questions:
        return gr.update(visible=False), questions, [], 0, "", ""

    return (
        gr.update(visible=True),
        questions,
        [],
        0,
        f"**Question 1 of {len(questions)}**",
        f"**{questions[0].question}**",
    )


async def maybe_run_research(query: str, questions: list):
    """Runs research directly when no clarifying questions were generated."""
    if questions:
        yield gr.update(), gr.update(), gr.update(), gr.update()
        return

    status_lines = []
    yield gr.update(visible=False), "• Starting research...", gr.update(visible=False), ""

    async for update in manager.run(query):
        if len(update) > 300 or update.strip().startswith("#"):
            status_lines.append("• Research complete.")
            yield gr.update(), "\n".join(status_lines), gr.update(visible=True), update
        else:
            status_lines.append(f"• {update}")
            yield gr.update(), "\n".join(status_lines), gr.update(visible=False), ""


async def submit_answer(answer: str, query: str, questions: list, answers: list, idx: int):
    new_answers = answers + [answer]
    next_idx    = idx + 1

    if next_idx < len(questions):
        yield (
            new_answers, next_idx,
            f"**Question {next_idx + 1} of {len(questions)}**",
            f"**{questions[next_idx].question}**",
            "",
            gr.update(visible=True), "", gr.update(visible=False), "",
        )
    else:
        qa_context = "\n\n".join(
            f"Q: {q.question}\nReason: {q.reason}\nA: {a}" for q, a in zip(questions, new_answers) if a.strip()
        )
        enriched_query = f"{query}\n\nAdditional context:\n{qa_context}" if qa_context else query

        status_lines = []
        yield (
            new_answers, next_idx, "", "", "",
            gr.update(visible=True), "", gr.update(visible=False), "",
        )

        async for update in manager.run(enriched_query):
            if len(update) > 300 or update.strip().startswith("#"):
                status_lines.append("• Research complete.")
                yield (
                    new_answers, next_idx, "", "", "",
                    gr.update(), "\n".join(status_lines), gr.update(visible=True), update,
                )
            else:
                status_lines.append(f"• {update}")
                yield (
                    new_answers, next_idx, "", "", "",
                    gr.update(), "\n".join(status_lines), gr.update(visible=False), "",
                )


with gr.Blocks(title="Deep Research Assistant", theme=gr.themes.Soft()) as demo:

    # ── State ─────────────────────────────────────────────────────────────────
    questions_state = gr.State([])   # list of Question objects from the agent
    answers_state   = gr.State([])   # answers collected so far
    idx_state       = gr.State(0)    # index of the question currently shown

    gr.Markdown("# Deep Research Assistant")
    gr.Markdown(
        "Enter any research topic. The assistant will plan web searches, "
        "synthesize the results into a detailed report, and email it to you."
    )

    # ── Phase 1: Query input ───────────────────────────────────────────────────
    query_input = gr.Textbox(
        label="Research Query",
        placeholder="e.g. What are the latest advancements in quantum computing?",
        lines=3,
    )
    start_btn = gr.Button("Start Research", variant="primary", size="lg")

    # ── Phase 2: Clarifying questions (one at a time) ─────────────────────────
    with gr.Column(visible=False) as clarification_section:
        progress_md  = gr.Markdown()
        question_md  = gr.Markdown()
        answer_input = gr.Textbox(label="Your answer", lines=2)
        submit_btn   = gr.Button("Submit Answer →", variant="primary")

    # ── Phase 3: Research output ───────────────────────────────────────────────
    status_box = gr.Textbox(
        label="Progress",
        lines=5,
        interactive=False,
        placeholder="Status updates will appear here once you start research...",
    )

    with gr.Column(visible=False) as report_section:
        gr.Markdown("---")
        gr.Markdown("## Report")
        report_output = gr.Markdown()

    # ── Wiring ─────────────────────────────────────────────────────────────────
    start_btn.click(
        fn=start_clarification,
        inputs=[query_input],
        outputs=[clarification_section, questions_state, answers_state, idx_state,
                 progress_md, question_md],
    ).then(
        fn=maybe_run_research,
        inputs=[query_input, questions_state],
        outputs=[clarification_section, status_box, report_section, report_output],
    )

    submit_btn.click(
        fn=submit_answer,
        inputs=[answer_input, query_input, questions_state, answers_state, idx_state],
        outputs=[answers_state, idx_state, progress_md, question_md, answer_input,
                 clarification_section, status_box, report_section, report_output],
    )

if __name__ == "__main__":
    demo.launch()
