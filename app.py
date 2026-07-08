import gradio as gr
from agents import Runner, trace, gen_trace_id
from orchestrator_agent import orchestrator_agent, OrchestratorOutput

conversation: list = []
pending_questions: list[str] = []
answered_qa: list[tuple[str, str]] = []
original_query: str = ""
trace_id = gen_trace_id()


async def chat(message: str, history: list) -> str:
    global conversation, pending_questions, answered_qa, original_query, trace_id

    if pending_questions:
        # User is answering a clarifying question
        current_q = pending_questions.pop(0)
        answered_qa.append((current_q, message))

        if pending_questions:
            # More questions remaining — show the next one
            return f"**{pending_questions[0]}**"

        # All questions answered — build enriched context and run orchestrator
        qa_context = "\n\n".join(f"Q: {q}\nA: {a}" for q, a in answered_qa)
        enriched = f"{original_query}\n\nClarifications provided by user:\n{qa_context}"
        input_data = conversation + [{"role": "user", "content": enriched}] if conversation else enriched
    else:
        # New query
        original_query = message
        answered_qa = []
        input_data = conversation + [{"role": "user", "content": message}] if conversation else message

    with trace("Research Assistant Run", trace_id=trace_id):
        result = await Runner.run(orchestrator_agent, input=input_data)

    conversation = result.to_input_list()
    output: OrchestratorOutput = result.final_output

    if output.status == "needs_clarification" and output.questions:
        answered_qa.clear()  # prior answers are already in conversation history
        pending_questions[:] = output.questions
        return f"{output.message}\n\n**{pending_questions[0]}**"

    return output.message


def reset() -> list:
    global conversation, pending_questions, answered_qa, original_query
    conversation = []
    pending_questions.clear()
    answered_qa.clear()
    original_query = ""
    return []


with gr.Blocks(title="Deep Research Assistant") as demo:
    gr.Markdown("# Deep Research Assistant")
    gr.Markdown(
        "Enter any research topic. The assistant will clarify your query, "
        "plan web searches, synthesize the results into a detailed report, and email it to you."
    )

    chatbot = gr.ChatInterface(fn=chat)
    gr.Button("New Research", variant="secondary").click(fn=reset, outputs=[chatbot.chatbot])

if __name__ == "__main__":
    demo.launch(theme=gr.themes.Soft())
