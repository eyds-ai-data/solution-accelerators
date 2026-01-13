from src.config.env import AppConfig

class EmbeddingRepository:
    def __init__(self, config: AppConfig):
        self.config = config

    def get_embedding_result(self, text: str) -> list[float]:
        # TODO: Implement embedding logic here
        pass

