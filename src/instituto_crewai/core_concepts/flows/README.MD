# Flows

## Introdução

CrewAI Flows é um recurso poderoso projetado para simplificar a criação e o gerenciamento de fluxos de trabalho de IA. Os Flows permitem que desenvolvedores combinem e coordenem tarefas de codificação e equipes de forma eficiente, oferecendo uma estrutura robusta para construir automações de IA sofisticadas.

Os Flows possibilitam a criação de fluxos de trabalho estruturados e orientados a eventos. Eles proporcionam uma forma integrada de conectar múltiplas tarefas, gerenciar estados e controlar o fluxo de execução em suas aplicações de IA. Com os Flows, você pode facilmente projetar e implementar processos de múltiplas etapas que aproveitam ao máximo as capacidades do CrewAI.

- **Criação Simplificada de Fluxos de Trabalho**: Conecte facilmente várias equipes e tarefas para criar fluxos de trabalho de IA complexos.

- **Gerenciamento de Estado**: Os Flows tornam extremamente fácil gerenciar e compartilhar estados entre diferentes tarefas em seu fluxo de trabalho.

- **Arquitetura Orientada a Eventos**: Construída em um modelo orientado a eventos, permitindo fluxos de trabalho dinâmicos e responsivos.

- **Fluxo de Controle Flexível**: Implemente lógica condicional, loops e ramificações dentro de seus fluxos de trabalho.

## Começando

### @start()

O decorador `@start()` é usado para marcar um método como o ponto de partida de um Flow. Quando um Flow é iniciado, todos os métodos decorados com `@start()` são executados em paralelo. Você pode ter múltiplos métodos de início em um Flow, e todos serão executados quando o Flow for iniciado.

### @listen()

O decorador `@listen()` é usado para marcar um método como um ouvinte da saída de outra tarefa no Flow. O método decorado com `@listen()` será executado quando a tarefa especificada emitir uma saída. O método pode acessar a saída da tarefa à qual está ouvindo como um argumento.

#### Uso

O decorador `@listen()` pode ser usado de várias formas:

1. **Ouvindo um Método por Nome**: Você pode passar o nome do método que deseja ouvir como uma string. Quando esse método for concluído, o método ouvinte será acionado.

    ```python
    @listen("generate_city")
    def generate_fun_fact(self, random_city):
        # Implementation
    ```

2. **Ouvindo um método diretamente:** Você pode passar o próprio método. Quando esse método for concluído, o método ouvinte será acionado.

    ```python
    @listen(generate_city)
    def generate_fun_fact(self, random_city):
        # Implementation
    ```

## Retorno do Flow

Acessar e manipular a saída de um Flow é essencial para integrar seus fluxos de trabalho de IA em aplicativos ou sistemas maiores. Os Flows do CrewAI fornecem mecanismos diretos para recuperar a saída final, acessar resultados intermediários e gerenciar o estado geral do seu Fluxo.

### Recuperando a Saída Final

Quando você executa um Flow, a saída final é determinada pelo último método que é concluído. O método `kickoff()` retorna a saída desse método final.

Aqui está como você pode acessar a saída final:

```python
flow = ExampleFlow()
result = await flow.kickoff()

print(f"Fato engraçado gerado: {result}")
```

### Acessando e Atualizando o Estado

Além de recuperar a saída final, você também pode acessar e atualizar o estado dentro do seu Flow. O estado pode ser usado para armazenar e compartilhar dados entre diferentes métodos no Flow. Após a execução do Flow, você pode acessar o estado para recuperar qualquer informação que tenha sido adicionada ou atualizada durante a execução.

Aqui está um exemplo de como atualizar e acessar o estado:

```python
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
```

Neste exemplo, o estado é atualizado tanto pelo `first_method` quanto pelo `second_method`. Após a execução do Flow, você pode acessar o estado final para ver as atualizações feitas por esses métodos.

Garantindo que a saída do método final seja retornada e fornecendo acesso ao estado, os Flows do CrewAI facilitam a integração dos resultados dos seus fluxos de trabalho de IA em aplicações ou sistemas maiores, além de manter e acessar o estado ao longo da execução do Flow.

## Gerenciamento de Estado do Flow

Gerenciar o estado de forma eficaz é crucial para construir fluxos de trabalho de IA confiáveis e fáceis de manter. Os Flows do CrewAI fornecem mecanismos robustos para o gerenciamento de estado tanto de forma não estruturada quanto estruturada, permitindo que os desenvolvedores escolham a abordagem que melhor se adapta às necessidades de sua aplicação.

### Gerenciamento de Estado Não Estruturado  

No gerenciamento de estado não estruturado, todo o estado é armazenado no atributo `state` da classe Flow. Esta abordagem oferece flexibilidade, permitindo que os desenvolvedores adicionem ou modifiquem atributos de estado conforme necessário, sem a necessidade de definir um esquema rígido.

**Pontos Chave:**

- **Flexibilidade**: Você pode adicionar atributos dinamicamente a `self.state` sem restrições predefinidas.
- **Simplicidade**: Ideal para fluxos de trabalho simples, onde a estrutura do estado é mínima ou varia significativamente.

### Gerenciamento de Estado Estruturado

O gerenciamento de estado estruturado utiliza esquemas predefinidos para garantir consistência e segurança de tipos ao longo do fluxo de trabalho. Ao usar modelos como o `BaseModel` do Pydantic, os desenvolvedores podem definir a forma exata do estado, permitindo melhor validação e autocompletação em ambientes de desenvolvimento.

Pontos Chave:

- **Esquema Definido:** `ExampleState` define claramente a estrutura do estado, melhorando a legibilidade e a manutenção do código.
- **Segurança de Tipos:** Utilizar o Pydantic garante que os atributos do estado estejam de acordo com os tipos especificados, reduzindo erros em tempo de execução.
- **Autocompletação:** IDEs podem fornecer melhor autocompletação e verificação de erros com base no modelo de estado definido.

### Escolhendo Entre Gerenciamento de Estado Não Estruturado e Estruturado

- **Use o Gerenciamento de Estado Não Estruturado quando**:

  - O estado do fluxo de trabalho é simples ou altamente dinâmico.
  - A flexibilidade é priorizada em vez de definições de estado rigorosas.
  - É necessário criar protótipos rapidamente, sem a complexidade de definir esquemas.
  
- **Use o Gerenciamento de Estado Estruturado quando**:

  - O fluxo de trabalho requer uma estrutura de estado bem definida e consistente.
  - A segurança de tipos e a validação são importantes para a confiabilidade da sua aplicação.
  - Você deseja aproveitar recursos de IDE, como autocompletação e verificação de tipos, para uma melhor experiência de desenvolvimento.

Ao oferecer opções de gerenciamento de estado não estruturado e estruturado, os Flows do CrewAI permitem que os desenvolvedores criem fluxos de trabalho de IA que sejam tanto flexíveis quanto robustos, atendendo a uma ampla gama de requisitos de aplicação.

## Controle de Fluxo

### Lógica Condicional: `or`

A função `or_` nos Flows permite que você escute múltiplos métodos e acione o método ouvinte quando qualquer um dos métodos especificados emitir uma saída.

### Lógica Condicional: `and`

A função `and_` nos Flows permite que você escute múltiplos métodos e acione o método ouvinte apenas quando todos os métodos especificados emitirem uma saída.

### Router

O decorador `@router()` nos Flows permite que você defina a lógica de roteamento condicional com base na saída de um método. Você pode especificar diferentes rotas com base na saída do método, permitindo controlar o fluxo de execução de forma dinâmica.
