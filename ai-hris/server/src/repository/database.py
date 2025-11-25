from src.config.env import AppConfig
from azure.cosmos import CosmosClient
import uuid
from datetime import datetime
from loguru import logger
from typing import Optional, List, Type, TypeVar, Dict, Any

T = TypeVar('T')

class CosmosDB:
    def __init__(self, config: AppConfig):
        self.config = config
        self.client = CosmosClient.from_connection_string(self.config.COSMOSDB_CONNECTION_STRING)
        self.database = self.client.get_database_client(self.config.COSMOSDB_DATABASE)
        self.container = self.database.get_container_client(self.config.COSMOSDB_CONTAINER)

    def insert_items(self, vector, candidate_id, name, skills, work_history, education_history):
        chat_item = {
            'id': str(uuid.uuid4()),
            'candidateId': candidate_id,
            'name': name,
            'embeddings': vector,
            'skills': skills,
            'workHistory': work_history,
            'educationHistory': education_history,
            'timestamp': datetime.utcnow().isoformat(),
        }
        response = self.container.create_item(body=chat_item)
        return response

    def query_items(self, query_vector, num_results: int = 5):
        try:
            query = f"""
            SELECT TOP @num_results c.id, c.candidateId, c.name,
            VectorDistance(c.embeddings, @embedding) AS SimilarityScore 
            FROM c 
            ORDER BY VectorDistance(c.embeddings, @embedding)
            """
            items = self.container.query_items(
                query=query,
                parameters=[
                    {"name": "@num_results", "value": num_results},
                    {"name": "@embedding", "value": query_vector}
                ],
                enable_cross_partition_query=True
            )

            recommendations = []
            for item in items:
                recommendations.append({
                    "id": item.get("id"),
                    "candidate_id": item.get("candidateId"),
                    "name": item.get("name"),
                    "similarity_score": item.get("SimilarityScore")
                })

            return recommendations
        except Exception as e:
            logger.error(f"Error querying items: {e}")
            raise ValueError(f"Error querying items: {e}")
        
    def get_by_id(self, item_id: str, id_field: str = "id") -> Optional[T]:
        """
        Retrieve an item from CosmosDB by ID.
        
        Args:
            item_id: The item ID to search for
            id_field: The field name to search in (default: "id")
            
        Returns:
            Model instance if found, None otherwise
        """
        try:
            query = f"SELECT * FROM c WHERE c.{id_field} = @item_id"
            items = list(self.container.query_items(
                query=query,
                parameters=[{"name": "@item_id", "value": item_id}],
                enable_cross_partition_query=True
            ))
            
            if items and len(items) > 0:
                return self.model_class(**items[0])
            return None
        except Exception as e:
            logger.error(f"Error retrieving item by ID: {e}")
            raise

    def get_all(self, limit: int = 100) -> List[T]:
        """
        Retrieve all items from CosmosDB.
        
        Args:
            limit: Maximum number of items to retrieve
            
        Returns:
            List of model instances
        """
        try:
            query = f"SELECT * FROM c OFFSET 0 LIMIT {limit}"
            items = list(self.container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            
            return [self.model_class(**item) for item in items]
        except Exception as e:
            logger.error(f"Error retrieving all items: {e}")
            raise

    def get_by_field(self, field_name: str, field_value: Any, limit: int = 100) -> List[T]:
        """
        Retrieve items filtered by a specific field.
        
        Args:
            field_name: The field name to filter by
            field_value: The value to filter for
            limit: Maximum number of items to retrieve
            
        Returns:
            List of model instances matching the filter
        """
        try:
            query = f"SELECT * FROM c WHERE c.{field_name} = @field_value OFFSET 0 LIMIT {limit}"
            items = list(self.container.query_items(
                query=query,
                parameters=[{"name": "@field_value", "value": field_value}],
                enable_cross_partition_query=True
            ))
            
            return [self.model_class(**item) for item in items]
        except Exception as e:
            logger.error(f"Error retrieving items by field {field_name}: {e}")
            raise

    def get_by_multiple_fields(self, filters: Dict[str, Any], limit: int = 100) -> List[T]:
        """
        Retrieve items filtered by multiple fields.
        
        Args:
            filters: Dictionary of field names and values to filter by
            limit: Maximum number of items to retrieve
            
        Returns:
            List of model instances matching all filters
        """
        try:
            # Build WHERE clause
            where_clauses = [f"c.{field} = @{field}" for field in filters.keys()]
            where_clause = " AND ".join(where_clauses)
            
            query = f"SELECT * FROM c WHERE {where_clause} OFFSET 0 LIMIT {limit}"
            
            # Build parameters
            parameters = [{"name": f"@{field}", "value": value} for field, value in filters.items()]
            
            items = list(self.container.query_items(
                query=query,
                parameters=parameters,
                enable_cross_partition_query=True
            ))
            
            return [self.model_class(**item) for item in items]
        except Exception as e:
            logger.error(f"Error retrieving items by multiple fields: {e}")
            raise

    def insert(self, item: T) -> Dict[str, Any]:
        """
        Insert an item into CosmosDB.
        
        Args:
            item: The model instance to insert
            
        Returns:
            The response from CosmosDB
        """
        try:
            item_dict = item.model_dump() if hasattr(item, 'model_dump') else item.__dict__
            response = self.container.create_item(body=item_dict)
            return response
        except Exception as e:
            logger.error(f"Error inserting item: {e}")
            raise

    def update(self, item_id: str, item: T, id_field: str = "id") -> Dict[str, Any]:
        """
        Update an item in CosmosDB.
        
        Args:
            item_id: The ID of the item to update
            item: The updated model instance
            id_field: The field name that contains the ID
            
        Returns:
            The response from CosmosDB
        """
        try:
            item_dict = item.model_dump() if hasattr(item, 'model_dump') else item.__dict__
            response = self.container.replace_item(item=item_dict)
            return response
        except Exception as e:
            logger.error(f"Error updating item: {e}")
            raise

    def delete(self, item_id: str, id_field: str = "id") -> None:
        """
        Delete an item from CosmosDB.
        
        Args:
            item_id: The ID of the item to delete
            id_field: The field name that contains the ID
        """
        try:
            # First, get the item to find its document ID
            item = self.get_by_id(item_id, id_field)
            if item:
                item_dict = item.model_dump() if hasattr(item, 'model_dump') else item.__dict__
                self.container.delete_item(item=item_dict)
            else:
                logger.warning(f"Item with {id_field}={item_id} not found for deletion")
        except Exception as e:
            logger.error(f"Error deleting item: {e}")
            raise

    def query(self, query_string: str, parameters: List[Dict[str, Any]] = None) -> List[T]:
        """
        Execute a custom query against CosmosDB.
        
        Args:
            query_string: The SQL query string
            parameters: List of query parameters
            
        Returns:
            List of model instances matching the query
        """
        try:
            items = list(self.container.query_items(
                query=query_string,
                parameters=parameters or [],
                enable_cross_partition_query=True
            ))
            
            return [self.model_class(**item) for item in items]
        except Exception as e:
            logger.error(f"Error executing custom query: {e}")
            raise