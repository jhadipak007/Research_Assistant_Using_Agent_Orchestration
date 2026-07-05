import gradio as gr
import asyncio
from research_manager import ResearchManager


async def run_research(query: str):
    if not query.strip():
        yield "Please enter a research query.", gr.update(visible=False), ""
        return

    manager = ResearchManager()
    status_lines = []

    async for update in manager.run(query):
        # The last yield is the full markdown report (long, starts with markdown)
        if len(update) > 300 or update.strip().startswith("#"):
            status_lines.append("Research complete.")
            yield "\n".join(status_lines), gr.update(visible=True), update
        else:
            status_lines.append(f"• {update}")
            yield "\n".join(status_lines), gr.update(visible=False), ""


with gr.Blocks(
    title="Deep Research Assistant",
    theme=gr.themes.Soft(),
    css=".report-box { border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; }",
) as demo:

    gr.Markdown("# Deep Research Assistant")
    gr.Markdown(
        "Enter any research topic. The assistant will plan web searches, "
        "synthesize the results into a detailed report, and email it to you."
    )

    with gr.Row():
        query_input = gr.Textbox(
            label="Research Query",
            placeholder="e.g. What are the latest advancements in quantum computing?",
            lines=3,
            scale=5,
        )

    submit_btn = gr.Button("Start Research", variant="primary", size="lg")

    status_box = gr.Textbox(
        label="Progress",
        lines=5,
        interactive=False,
        placeholder="Status updates will appear here once you start research...",
    )

    report_section = gr.Column(visible=False)
    with report_section:
        gr.Markdown("---")
        gr.Markdown("## Report")
        report_output = gr.Markdown(elem_classes=["report-box"])

    submit_btn.click(
        fn=run_research,
        inputs=[query_input],
        outputs=[status_box, report_section, report_output],
    )

if __name__ == "__main__":
    demo.launch()
