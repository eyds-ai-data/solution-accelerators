from src.domain.gl_transaction import GLTransaction, GLReconItem
from src.domain.tax_invoice import TaxInvoice
from src.domain.invoice import Invoice
from typing import List, Tuple, Optional
from loguru import logger
from src.repository.database import AzureCosmosDBRepository

class TaxManagementUseCase:
    def __init__(self, azure_cosmos_repo: AzureCosmosDBRepository):
        self.azure_cosmos_repo = azure_cosmos_repo

    def get_gl_transactions(self, urn: str = None, page: int = 1, page_size: int = 10) -> Tuple[List[dict], int]:
        try:
            query_filter = f"c.urn = '{urn}'" if urn else None
            
            # Get total count
            total = self.azure_cosmos_repo.count_documents(
                container_id="gl-transactions",
                query_filter=query_filter
            )
            
            # Get paginated results
            offset = (page - 1) * page_size
            result = self.azure_cosmos_repo.query_documents(
                container_id="gl-transactions",
                query_filter=query_filter,
                offset=offset,
                limit=page_size
            )
            
            gl_transactions = [GLTransaction(**item) for item in result]
            
            # Enrich each GL transaction with related invoice and tax invoice
            enriched = []
            for gl in gl_transactions:
                gl_dict = gl.model_dump(by_alias=True)
                
                # Look up related invoice by URN
                invoice_results = self.azure_cosmos_repo.query_documents(
                    container_id="invoices",
                    query_filter=f"c.urn = '{gl.urn}'",
                    limit=1
                )
                if invoice_results:
                    inv = Invoice(**invoice_results[0])
                    gl_dict["relatedInvoice"] = {
                        "invoiceId": inv.invoice_id,
                        "invoiceNumber": inv.invoice_number,
                    }
                else:
                    gl_dict["relatedInvoice"] = None
                
                # Look up related tax invoice by URN
                tax_invoice_results = self.azure_cosmos_repo.query_documents(
                    container_id="tax-invoices",
                    query_filter=f"c.urn = '{gl.urn}'",
                    limit=1
                )
                if tax_invoice_results:
                    tax_inv = TaxInvoice(**tax_invoice_results[0])
                    gl_dict["relatedTaxInvoice"] = {
                        "taxInvoiceId": tax_inv.tax_invoice_id,
                        "taxInvoiceNumber": tax_inv.tax_invoice_number,
                    }
                else:
                    gl_dict["relatedTaxInvoice"] = None
                
                enriched.append(gl_dict)
            
            return enriched, total
        except Exception as e:
            logger.error(f"Error retrieving G/L transactions: {e}")
            raise e
    
    def get_gl_transaction_by_urn(self, urn: str) -> Optional[GLTransaction]:
        try:
            result = self.azure_cosmos_repo.query_documents(
                container_id="gl-transactions",
                query_filter=f"c.urn = '{urn}'",
                limit=1
            )
            if result:
                return GLTransaction(**result[0])
            return None
        except Exception as e:
            logger.error(f"Error retrieving G/L transaction by URN: {e}")
            raise e

    def get_tax_invoices(self, urn: str = None) -> List[TaxInvoice]:
        try:
            if urn:
                result = self.azure_cosmos_repo.query_documents(
                    container_id="tax-invoices",
                    query_filter=f"c.urn = '{urn}'"
                )
            else:
                result = self.azure_cosmos_repo.query_documents(container_id="tax-invoices")
            return [TaxInvoice(**item) for item in result]
        except Exception as e:
            logger.error(f"Error retrieving tax invoices: {e}")
            raise e

    def get_invoices(self, urn: str = None) -> List[Invoice]:
        try:
            if urn:
                result = self.azure_cosmos_repo.query_documents(
                    container_id="invoices",
                    query_filter=f"c.urn = '{urn}'"
                )
            else:
                result = self.azure_cosmos_repo.query_documents(container_id="invoices")
            return [Invoice(**item) for item in result]
        except Exception as e:
            logger.error(f"Error retrieving invoices: {e}")
            raise e

    def get_dashboard_stats(self) -> dict:
        try:
            gl_count = self.azure_cosmos_repo.count_documents(container_id="gl-transactions")
            tax_invoices_count = self.azure_cosmos_repo.count_documents(container_id="tax-invoices")
            invoices_count = self.azure_cosmos_repo.count_documents(container_id="invoices")
            
            return {
                "total_gl_transactions": gl_count,
                "total_tax_invoices": tax_invoices_count,
                "total_invoices": invoices_count
            }
        except Exception as e:
            logger.error(f"Error retrieving dashboard stats: {e}")
            raise e