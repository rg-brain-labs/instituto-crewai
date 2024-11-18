from crewai_tools import BaseTool
import requests, os, json

class CapturaDadosCartaoTool(BaseTool):
  name: str = "Captura de Dados de Cartão Trello"
  description: str = "Extrai dados detalhados de cartões de um quadro Trello."

  api_key: str = os.environ['TRELLO_API_KEY']
  api_token: str = os.environ['TRELLO_API_TOKEN']

  def _run(self, card_id: str) -> dict:
    url = f"{os.getenv('DLAI_TRELLO_BASE_URL', 'https://api.trello.com')}/1/cards/{card_id}"
    query = {
      'key': self.api_key,
      'token': self.api_token
    }
    response = requests.get(url, params=query)

    if response.status_code == 200:
      return response.json()
    else:
      # Fallback in case of timeouts or other issues
      return json.dumps({"error": "Não foi possível recuperar informações do cartão. Pare de tentar obter dados do Trello."})
