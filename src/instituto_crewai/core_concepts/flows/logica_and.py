import asyncio, time
from crewai.flow.flow import Flow, and_, listen, start, or_

class AndExampleFlow(Flow):

    @start()
    def start_method(self):
        time.sleep(2)
        self.state["greeting"] = "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        time.sleep(5)
        self.state["joke"] = "What do computers eat? Microchips."

    @listen(and_(start_method, second_method))
    def logger(self):
        print("---- Logger ----")
        print(self.state)


async def main():
    flow = AndExampleFlow()
    await flow.kickoff()


asyncio.run(main())
