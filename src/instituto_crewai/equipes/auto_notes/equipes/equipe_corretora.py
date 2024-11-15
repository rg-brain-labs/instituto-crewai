import os
from datetime import datetime
from pathlib import Path

# Definir pasta padrão na pasta Documents
pasta_padrao = os.path.join(str(Path(__file__).parent), "arquivos")

print(pasta_padrao)