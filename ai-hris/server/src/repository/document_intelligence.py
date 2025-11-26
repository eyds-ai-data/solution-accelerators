from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.ai.documentintelligence.models import AnalyzeResult
import numpy as np
from config.env import AppConfig

class DocumentIntelligenceRepository:
    def __init__(self, config: AppConfig):
        self.document_intelligence_endpoint = config.DOCUMENT_INTELLIGENCE_ENDPOINT
        self.document_intelligence_key = config.DOCUMENT_INTELLIGENCE_KEY
        self.document_intelligence_client  = DocumentIntelligenceClient(
            endpoint=self.document_intelligence_endpoint, credential=AzureKeyCredential(self.document_intelligence_key)
        )

    def _format_bounding_box(self, bounding_box):
        if not bounding_box:
            return "N/A"
        reshaped_bounding_box = np.array(bounding_box).reshape(-1, 2)
        return ", ".join(["[{}, {}]".format(x, y) for x, y in reshaped_bounding_box])

    def analyze_read(self, document):
        document_path = "assets/kartu_keluarga_siti_nurhaliza.png"

        document_intelligence_client  = DocumentIntelligenceClient(
            endpoint=endpoint, credential=AzureKeyCredential(key)
        )
        
        with open(document_path, "rb") as f:
            poller = document_intelligence_client.begin_analyze_document(
                "prebuilt-read", AnalyzeDocumentRequest(bytes_source=f.read())
            )
        result: AnalyzeResult = poller.result()

        for page in result.pages:
            print("----Analyzing Read from page #{}----".format(page.page_number))
            print(
                "Page has width: {} and height: {}, measured with unit: {}".format(
                    page.width, page.height, page.unit
                )
            )

            for line_idx, line in enumerate(page.lines):
                print(
                    "...Line # {} has text content '{}' within bounding box '{}'".format(
                        line_idx,
                        line.content,
                        format_bounding_box(line.polygon),
                    )
                )

            for word in page.words:
                print(
                    "...Word '{}' has a confidence of {}".format(
                        word.content, word.confidence
                    )
                )

if __name__ == "__main__":
    analyze_read()

