from azure.cosmos import CosmosClient, exceptions
from loguru import logger
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

class AzureCosmosDBRepository:
    
    def __init__(self, connection_string: str, database_id: str, container_id: str):
        """
        Initialize Cosmos DB repository
        
        Args:
            connection_string: Cosmos DB connection string
            database_id: Database name
            container_id: Container name
        """
        try:
            self.client = CosmosClient.from_connection_string(connection_string)
            self.database = self.client.get_database_client(database_id)
            self.container = self.database.get_container_client(container_id)
            logger.info(f"Connected to Cosmos DB database '{database_id}', container '{container_id}'")
        except Exception as e:
            logger.error(f"Failed to connect to Cosmos DB: {e}")
            raise

    def create_document(self, document_data: Dict[str, Any], partition_key: Optional[str] = None, container_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new document in Cosmos DB
        
        Args:
            document_data: Document data to store
            document_type: Type identifier for the document
            partition_key: Optional partition key value. If not provided, uses document id
            
        Returns:
            Created document with id and timestamps
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container

            doc_id = document_data.get("id") or str(uuid.uuid4())
            now = datetime.utcnow().isoformat()
            
            document = {
                **document_data,
                "id": doc_id,
                "created_at": document_data.get("created_at", now),
                "updated_at": now
            }
            
            # Add partition key field if specified and different from id
            if partition_key and partition_key != doc_id:
                document[partition_key] = document.get(partition_key, doc_id)
            
            created = container.create_item(body=document)
            return created
        except exceptions.CosmosHttpResponseError as e:
            raise
        except Exception as e:
            raise

    def get_document_by_id(self, document_id: str, partition_key: Optional[str] = None, container_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a specific document by ID
        
        Args:
            document_id: Document ID to retrieve
            partition_key: Partition key value. If not provided, uses document_id
            
        Returns:
            Retrieved document
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container
            pk = partition_key if partition_key else document_id
            item = container.read_item(item=document_id, partition_key=pk)
            logger.info(f"Retrieved document: {document_id}")
            return item
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Document not found: {document_id}")
            raise
        except Exception as e:
            logger.error(f"Error retrieving document {document_id}: {e}")
            raise

    def query_documents(
        self, 
        document_type: Optional[str] = None,
        query_filter: Optional[str] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
        order_by: str = "created_at DESC",
        max_items: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        container_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Query documents with optional filters
        
        Args:
            document_type: Filter by document type
            query_filter: Additional SQL WHERE clause (without WHERE keyword)
            parameters: Query parameters for parameterized queries
            order_by: ORDER BY clause (without ORDER BY keyword)
            max_items: Maximum number of items to return (SDK hint)
            offset: Number of items to skip
            limit: Maximum number of items to return (SQL LIMIT)
            
        Returns:
            List of matching documents
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container
            
            # Build query
            query = "SELECT * FROM c"
            
            conditions = []
            if document_type:
                conditions.append(f"c.type = '{document_type}'")
            if query_filter:
                conditions.append(query_filter)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            if order_by:
                query += f" ORDER BY c.{order_by}"
            
            if offset is not None and limit is not None:
                query += f" OFFSET {offset} LIMIT {limit}"
            
            items = list(container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True,
                max_item_count=max_items
            ))
            
            logger.info(f"Retrieved {len(items)} documents (type: {document_type or 'all'})")
            return items
        except Exception as e:
            logger.error(f"Error querying documents: {e}")
            raise

    def count_documents(
        self, 
        document_type: Optional[str] = None,
        query_filter: Optional[str] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
        container_id: Optional[str] = None
    ) -> int:
        """
        Count documents with optional filters
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container
            
            query = "SELECT VALUE COUNT(1) FROM c"
            
            conditions = []
            if document_type:
                conditions.append(f"c.type = '{document_type}'")
            if query_filter:
                conditions.append(query_filter)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                
            items = list(container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            return items[0] if items else 0
        except Exception as e:
            logger.error(f"Error counting documents: {e}")
            raise

    def delete_document(self, document_id: str, partition_key: Optional[str] = None) -> bool:
        """
        Delete a document from Cosmos DB
        
        Args:
            document_id: Document ID to delete
            partition_key: Partition key value. If not provided, uses document_id
            
        Returns:
            True if deletion was successful
        """
        try:
            pk = partition_key if partition_key else document_id
            self.container.delete_item(item=document_id, partition_key=pk)
            logger.info(f"Deleted document: {document_id}")
            return True
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Document not found for deletion: {document_id}")
            raise
        except Exception as e:
            logger.error(f"Error deleting document {document_id}: {e}")
            raise

    def update_document(
        self, 
        document_id: str, 
        update_data: Dict[str, Any],
        partition_key: Optional[str] = None,
        partial_update: bool = True,
        container_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing document
        
        Args:
            document_id: Document ID to update
            update_data: Data to update (merged with existing if partial_update=True)
            partition_key: Partition key value. If not provided, uses document_id
            partial_update: If True, merge with existing data. If False, replace entire document.
            
        Returns:
            Updated document
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container
            pk = partition_key if partition_key else document_id
            
            if partial_update:
                # Get existing document and merge
                existing = self.get_document_by_id(document_id, partition_key, container_id)
                
                # Update fields (preserve id and created_at)
                for key, value in update_data.items():
                    if key not in ["id", "created_at"]:
                        existing[key] = value
                
                document = existing
            else:
                # Replace entire document
                document = {
                    **update_data,
                    "id": document_id
                }
            
            # Update timestamp
            document["updated_at"] = datetime.utcnow().isoformat()
            
            updated = container.upsert_item(body=document)
            logger.info(f"Updated document: {document_id}")
            return updated
        except Exception as e:
            logger.error(f"Error updating document {document_id}: {e}")
            raise
    
    def upsert_document(self, document_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update a document (upsert operation)
        
        Args:
            document_data: Complete document data including id
            
        Returns:
            Upserted document
        """
        try:
            document_data["updated_at"] = datetime.utcnow().isoformat()
            
            if "created_at" not in document_data:
                document_data["created_at"] = document_data["updated_at"]
            
            upserted = self.container.upsert_item(body=document_data)
            logger.info(f"Upserted document: {document_data.get('id')}")
            return upserted
        except Exception as e:
            logger.error(f"Error upserting document: {e}")
            raise

    def vector_search(
        self,
        vector: List[float],
        vector_field: str = "embedding",
        top_k: int = 10,
        similarity_score_threshold: Optional[float] = None,
        document_type: Optional[str] = None,
        additional_filters: Optional[str] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
        return_similarity_score: bool = True,
        container_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search in Cosmos DB using VectorDistance function
        
        Args:
            vector: Query vector (embedding) to search for similar documents
            vector_field: Name of the field containing the vector embeddings (default: "embedding")
            top_k: Number of most similar documents to return (default: 10)
            similarity_score_threshold: Optional minimum similarity score filter
            document_type: Optional filter by document type
            additional_filters: Additional SQL WHERE conditions (without WHERE keyword)
            parameters: Query parameters for parameterized queries
            return_similarity_score: If True, include similarity score in results
            container_id: Optional different container ID to query
            
        Returns:
            List of documents ordered by similarity (most similar first)
            Each document includes a 'similarity_score' field if return_similarity_score=True
            
        Note:
            - The container must have a vector index policy configured on the vector_field
            - Similarity score ranges from 0 (least similar) to 1 (most similar) for cosine similarity
            - Lower values indicate less similarity, higher values indicate more similarity
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container
            
            # Build the vector distance calculation in SELECT
            if return_similarity_score:
                select_clause = f"SELECT c.*, VectorDistance(c.{vector_field}, @embedding) AS similarity_score FROM c"
            else:
                select_clause = f"SELECT c.* FROM c"
            
            # Build WHERE conditions
            conditions = []
            
            if document_type:
                conditions.append(f"c.type = '{document_type}'")
            
            if additional_filters:
                conditions.append(additional_filters)
            
            # Build the complete query
            query = select_clause
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            # Order by similarity (VectorDistance returns lower values for more similar vectors in some metrics)
            # For cosine similarity, lower distance = more similar
            query += f" ORDER BY VectorDistance(c.{vector_field}, @embedding)"
            
            # Prepare parameters
            query_params = parameters or []
            query_params.append({"name": "@embedding", "value": vector})
            
            # Execute the query
            items = list(container.query_items(
                query=query,
                parameters=query_params,
                enable_cross_partition_query=True,
                max_item_count=top_k
            ))
            
            # Apply similarity threshold filter if specified
            if similarity_score_threshold is not None and return_similarity_score:
                items = [
                    item for item in items 
                    if item.get("similarity_score", 0) >= similarity_score_threshold
                ]
            
            # Limit to top_k results
            items = items[:top_k]
            
            logger.info(f"Vector search returned {len(items)} documents (top_k={top_k})")
            return items
            
        except Exception as e:
            logger.error(f"Error performing vector search: {e}")
            raise

    def hybrid_search(
        self,
        vector: List[float],
        text_query: Optional[str] = None,
        vector_field: str = "embedding",
        text_search_fields: Optional[List[str]] = None,
        top_k: int = 10,
        vector_weight: float = 0.5,
        document_type: Optional[str] = None,
        additional_filters: Optional[str] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
        container_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining vector similarity and text search
        
        Args:
            vector: Query vector (embedding) for semantic search
            text_query: Text query for keyword matching
            vector_field: Name of the field containing the vector embeddings
            text_search_fields: Fields to search for text (e.g., ["content", "title"])
            top_k: Number of results to return
            vector_weight: Weight for vector similarity (0-1), text weight = 1 - vector_weight
            document_type: Optional filter by document type
            additional_filters: Additional SQL WHERE conditions
            parameters: Query parameters for parameterized queries
            container_id: Optional different container ID to query
            
        Returns:
            List of documents ranked by combined score
        """
        try:
            container = self.database.get_container_client(container_id) if container_id else self.container
            
            # Build the query with both vector and text relevance
            text_conditions = []
            if text_query and text_search_fields:
                # Build text search conditions (contains check for each field)
                for field in text_search_fields:
                    text_conditions.append(f"CONTAINS(LOWER(c.{field}), LOWER(@textQuery))")
            
            # Build WHERE conditions
            conditions = []
            if document_type:
                conditions.append(f"c.type = '{document_type}'")
            
            if text_conditions:
                conditions.append(f"({' OR '.join(text_conditions)})")
            
            if additional_filters:
                conditions.append(additional_filters)
            
            # Calculate hybrid score
            vector_score = f"VectorDistance(c.{vector_field}, @embedding)"
            
            # Build query
            select_clause = f"""SELECT c.*, 
                {vector_score} AS vector_score,
                {vector_score} AS hybrid_score 
                FROM c"""
            
            query = select_clause
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += f" ORDER BY {vector_score}"
            
            # Prepare parameters
            query_params = parameters or []
            query_params.append({"name": "@embedding", "value": vector})
            if text_query:
                query_params.append({"name": "@textQuery", "value": text_query})
            
            # Execute query
            items = list(container.query_items(
                query=query,
                parameters=query_params,
                enable_cross_partition_query=True,
                max_item_count=top_k * 2  # Get more items for re-ranking
            ))
            
            # Re-rank if text query is provided
            if text_query and text_search_fields:
                for item in items:
                    # Simple text relevance score (count of matches)
                    text_score = 0
                    for field in text_search_fields:
                        field_value = str(item.get(field, "")).lower()
                        if text_query.lower() in field_value:
                            text_score += field_value.count(text_query.lower())
                    
                    # Normalize text score
                    text_score = min(text_score / 10.0, 1.0)  # Cap at 1.0
                    
                    # Combine scores (invert vector score since lower is better)
                    vector_sim = 1.0 - min(item.get("vector_score", 1.0), 1.0)
                    item["hybrid_score"] = (vector_weight * vector_sim) + ((1 - vector_weight) * text_score)
                
                # Sort by hybrid score (descending)
                items.sort(key=lambda x: x.get("hybrid_score", 0), reverse=True)
            
            # Return top_k results
            results = items[:top_k]
            logger.info(f"Hybrid search returned {len(results)} documents (top_k={top_k})")
            return results
            
        except Exception as e:
            logger.error(f"Error performing hybrid search: {e}")
            raise
