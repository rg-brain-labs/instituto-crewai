import asyncio
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

class ExampleState(BaseModel):
    counter: int = 0
    message: str = ""

class StateExampleFlow(Flow[ExampleState]):
   
    @start()
    def first_method(self):
        self.state.message = "Olá"
        self.state.counter += 1

    @listen(first_method)
    def second_method(self):
        self.state.message += " - Mundo !!!"
        self.state.counter += 1
        return self.state.message

async def main():
    flow = StateExampleFlow()
    final_output = await flow.kickoff()
    print(f"Resposta Final: {final_output}")
    print("State Final:")
    print(flow.state)

asyncio.run(main())
