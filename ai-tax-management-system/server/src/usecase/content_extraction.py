from typing import Dict, Any, Optional
from src.repository.content_understanding import ContentUnderstandingRepository
from src.repository.storage import MinioStorageRepository
from src.repository.storage import AzureBlobStorageRepository
from src.repository.messaging import RabbitMQRepository
from loguru import logger

class ContentExtraction:
    def __init__(
        self, 
        content_understanding_repo: ContentUnderstandingRepository,
        azure_blob_storage_repo: AzureBlobStorageRepository,
        rabbitmq_repo: Optional[RabbitMQRepository] = None,
        minio_storage_repo: Optional[MinioStorageRepository] = None
    ):
        
        self.content_understanding_repo = content_understanding_repo
        self.azure_blob_storage_repo = azure_blob_storage_repo
        self.rabbitmq_repo = rabbitmq_repo
        self.minio_storage_repo = minio_storage_repo

    def extract_content(self, file, upload_id: str, original_filename: str) -> Dict[str, Any]:

        try:
            file_info = self.minio_storage_repo.upload_file(
                file=file, case_id=upload_id, original_filename=original_filename
            )

            return None
        
        except Exception as e:
            logger.error(f"Error extracting content from {original_filename}: {e}")
            raise