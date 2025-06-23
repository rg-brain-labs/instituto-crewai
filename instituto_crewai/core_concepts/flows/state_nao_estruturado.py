import asyncio

from crewai.flow.flow import Flow, listen, start

class UntructuredExampleFlow(Flow):

    @start()
    def first_method(self):
        self.state['message'] = "Hello from structured flow"
        self.state['counter'] = 0

    @listen(first_method)
    def second_method(self):
        self.state['counter'] += 1
        self.state['message'] += " - updated"

    @listen(second_method)
    def third_method(self):
        self.state['counter'] += 1
        self.state['message'] += " - updated again"

        print(f"State after third_method: {self.state}")


async def main():
    flow = UntructuredExampleFlow()
    await flow.kickoff()


asyncio.run(main())
