from planner_agent import WebSearchPlan, planner_agent, WebSearchItem
from search_agent import search_agent
from writer_agent import writer_agent, ReportData
from agents import Runner, trace, gen_trace_id
from email_agent import email_agent
import asyncio
from clarification_question_generator_agent import question_generator_agent, ClarifyingQuestions

class ResearchManager:
    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()

        with trace("Research trace", trace_id=trace_id):
            yield f"Starting research." 
            










            search_plan = await self.plan_searches(query=query)
            #yield f"Searches planned, starting {len(search_plan.searches)} searches"
            search_results = await self.perform_searches(search_plan=search_plan)
            yield f"Searches complete. Writing report..."
            report = await self.write_report(query=query, search_results=search_results)
            yield f"Report written. Sending email...."
            await self.send_email(report=report)
            yield f"Email sent, research complete"
            yield report.markdown_report


    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan the searches to perform for the query"""

        result = await Runner.run(starting_agent=planner_agent, input=f"Query: {query}")
        return result.final_output
    
    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        tasks = [self.search(item=item) for item in search_plan.searches ]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str|None:
        """ Perform a search for the query """
        input_message = f"Search item: {item.query} \n Reason for searching: {item.reason}"
        search_response = await Runner.run(starting_agent=search_agent, input=input_message)
        return search_response.final_output
    
    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """"Write the report for the query"""

        input_message = f"Original query: {query}\n Summerized search results: {search_results}"
        result = await Runner.run(writer_agent, input_message)
        return result.final_output
    
    async def send_email(self, report: ReportData) -> None:
        await Runner.run(starting_agent=email_agent, input=report.markdown_report)

    async def get_clarifications(self, query: str) -> ClarifyingQuestions:
        response = await Runner.run(starting_agent=question_generator_agent, input=query)
        return response.final_output