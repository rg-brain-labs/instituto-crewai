class LLM:
    def __init__(self, modelo):
        self.modelo = modelo

    def create_instance(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def generate_text(self):
        raise NotImplementedError("Subclasses must implement this method")

    def __str__(self):
        return f"{self.__class__.__name__} model named {self.modelo.value}"
