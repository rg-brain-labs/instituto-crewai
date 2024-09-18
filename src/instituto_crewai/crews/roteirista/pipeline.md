# Pipeline

**O que é um pipeline?**

Um pipeline no crewAI representa um fluxo de trabalho estruturado que permite a execução sequencial ou paralela de múltiplas equipes (crews). Ele fornece uma maneira de organizar processos complexos envolvendo vários estágios, onde a saída de um estágio pode servir como entrada para os estágios subsequentes.

**Terminologia principal:**

É crucial entender os seguintes termos para trabalhar efetivamente com pipelines:

* **Estágio (Stage):** Uma parte distinta do pipeline, que pode ser sequencial (uma única equipe) ou paralela (várias equipes executadas simultaneamente).
* **Execução (Run):** Uma execução específica do pipeline para um determinado conjunto de entradas, representando uma única instância de processamento através do pipeline.
* **Ramo (Branch):** Execuções paralelas dentro de um estágio (por exemplo, operações simultâneas de equipes).
* **Rastreamento (Trace):** A jornada de uma entrada individual por todo o pipeline, capturando o caminho e as transformações que ela sofre.

**Exemplo de estrutura de pipeline:**

```cmd
crew1 >> [crew2, crew3] >> crew4
```

Isso representa um pipeline com três estágios:

* Um estágio sequencial (crew1)
* Um estágio paralelo com duas ramificações (crew2 e crew3 executadas simultaneamente)
* Outro estágio sequencial (crew4)

Cada entrada cria sua própria execução, fluindo por todos os estágios do pipeline. Várias execuções podem ser processadas simultaneamente, cada uma seguindo a estrutura de pipeline definida.

**Atributos do Pipeline:**

| Atributo | Descrição |
|---|---|
| stages | Uma lista de **crews** ou **routers** representando os estágios a serem executados em sequência. |

**Criando um Pipeline:**

Ao criar um pipeline, você define uma série de estágios, cada um consistindo em uma única crew ou uma lista de crews para execução paralela. O pipeline garante que cada estágio seja executado em ordem, com a saída de um estágio sendo alimentada para o próximo.

**Exemplo: Montando um Pipeline**

```python
from crewai import Crew, Agent, Task, Pipeline

# Defina suas equipes
research_crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    process=Process.sequential
)

analysis_crew = Crew(
    agents=[analyst],
    tasks=[analysis_task],
    process=Process.sequential
)

writing_crew = Crew(
    agents=[writer],
    tasks=[writing_task],
    process=Process.sequential
)

# Monte o pipeline
my_pipeline = Pipeline(
    stages=[research_crew, analysis_crew, writing_crew]
)
```

**Métodos do Pipeline:**

| Método | Descrição |
|---|---|
| process_runs | Executa o pipeline, processando todos os estágios e retornando os resultados. Este método inicia uma ou mais execuções através do pipeline, manipulando o fluxo de dados entre os estágios. |

**Saída do Pipeline:**

**Entendendo as Saídas do Pipeline**

A saída de um pipeline no framework crewAI é encapsulada dentro da classe PipelineKickoffResult. Esta classe fornece uma maneira estruturada de acessar os resultados da execução do pipeline, incluindo vários formatos como strings brutas, JSON e modelos Pydantic.

**Atributos da Saída do Pipeline**

| Atributo | Descrição | Tipo |
|---|---|---|
| id | Um identificador único UUID4 para a saída do pipeline. | UUID4 |
| run_results | Uma lista de objetos PipelineRunResult, cada um representando a saída de uma única execução através do pipeline. | Lista[PipelineRunResult] |

**Métodos de Saída do Pipeline:**

| Método/Propriedade | Descrição |
|---|---|
| add_run_result | Adiciona um PipelineRunResult à lista de resultados de execução. |

**Atributos do Resultado da Execução do Pipeline**

| Atributo | Descrição | Tipo |
|---|---|---|
| id | Um identificador único UUID4 para o resultado da execução. | UUID4 |
| raw | A saída bruta do estágio final na execução do pipeline. | str |
| pydantic | Um objeto de modelo Pydantic representando a saída estruturada do estágio final, se aplicável. | Pydantic (opcional) |