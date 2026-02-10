from src.config.env import AppConfig
from semantic_kernel.connectors.ai.open_ai import AzureTextEmbedding
from loguru import logger

class EmbeddingRepository:
    def __init__(self, config: AppConfig):
        self.config = config
        self.embedding_service = AzureTextEmbedding(
            deployment_name=config.AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME,
            endpoint=config.AZURE_OPENAI_API_BASE,
            api_key=config.AZURE_OPENAI_API_KEY
        )

    async def get_embedding_result(self, text: str) -> list[float]:
        """
        Generate embeddings for the given text using Azure OpenAI embedding service.
        
        Args:
            text: The text to generate embeddings for
            
        Returns:
            A list of floats representing the embedding vector
        """
        try:
            vector = await self.embedding_service.generate_embeddings([text])
            
            # Handle different return types
            if hasattr(vector, 'tolist'):
                vector = vector.tolist()
            
            # If the result is a list of lists, extract the first one
            if isinstance(vector, list) and len(vector) > 0:
                if isinstance(vector[0], list):
                    vector = vector[0]
            
            logger.info(f"Successfully generated embedding with dimension: {len(vector)}")
            return vector
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise

