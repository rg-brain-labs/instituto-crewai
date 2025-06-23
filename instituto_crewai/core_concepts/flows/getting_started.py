import asyncio

from crewai.flow.flow import Flow, listen, start
from litellm import completion


class ExampleFlow(Flow):
    model = "groq/llama-3.2-1b-preview"

    @start()
    def generate_city(self):
        print("Iniciando flow")

        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": "Retorne o nome de uma cidade aleatória do Brasil.",
                },
            ],
        )

        random_city = response["choices"][0]["message"]["content"]
        print(f"Cidade Aleatória: {random_city}")

        return random_city

    @listen(generate_city)
    def generate_fun_fact(self, random_city):
        response = completion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Me conte um fato engraçado sobre {random_city}",
                },
            ],
        )

        fun_fact = response["choices"][0]["message"]["content"]
        return fun_fact


async def main():
    flow = ExampleFlow()
    result = await flow.kickoff()

    print(f"Fato engraçado gerado: {result}")

asyncio.run(main())
