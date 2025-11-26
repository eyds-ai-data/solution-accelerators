from src.repository.document_intelligence import DocumentIntelligenceRepository
from loguru import logger
from src.llm.llm_sk import LLMService
from src.domain.document_analyzer import KartuKeluargaResponse, KartuKeluargaBoundingBox
import numpy as np

class DocumentAnalyzer:
    def __init__(self, doc_intel_repo: DocumentIntelligenceRepository, llm_service: LLMService):
        self.doc_intel_repo = doc_intel_repo
        self.llm_service = llm_service
    
    def _extract_bounding_boxes(self, result):
        """Extract bounding boxes from paragraphs in the analysis result."""
        bounding_boxes = []
        
        if result.paragraphs:
            for paragraph in result.paragraphs:
                if hasattr(paragraph, 'bounding_regions') and paragraph.bounding_regions:
                    # Extract bounding regions which contain pageNumber and polygon
                    for region in paragraph.bounding_regions:
                        polygons = []
                        page_number = 1
                        
                        if hasattr(region, 'page_number'):
                            page_number = region.page_number
                        elif hasattr(region, 'pageNumber'):
                            page_number = region.pageNumber
                        
                        if hasattr(region, 'polygon'):
                            polygons = list(region.polygon) if isinstance(region.polygon, (list, tuple)) else []
                        
                        if polygons:
                            bounding_box = KartuKeluargaBoundingBox(
                                content=getattr(paragraph, 'content', ''),
                                page_number=page_number,
                                polygons=polygons
                            )
                            bounding_boxes.append(bounding_box)
        
        return bounding_boxes
    
    async def analyze_document_kk(self, document_path: str) -> KartuKeluargaResponse:
        try:
            result = self.doc_intel_repo.analyze_read(document_path=document_path)
            
            # Extract bounding boxes from paragraphs
            bounding_boxes = self._extract_bounding_boxes(result)
            
            kartu_keluarga_structured = await self.llm_service.kartu_keluarga_extractor(result.content)

            response = KartuKeluargaResponse(
                content=result.content,
                structured_data=kartu_keluarga_structured,
                bounding_boxes=bounding_boxes
            )

            return response
        except Exception as e:
            logger.error(f"Error in analyze_document use case: {e}")
            raise