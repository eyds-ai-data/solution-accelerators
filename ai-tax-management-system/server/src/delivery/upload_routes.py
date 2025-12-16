from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from typing import Dict, Any, Optional
from loguru import logger
import uuid

from src.config.dependencies import FileUploadDep

router = APIRouter(prefix="/api/v1/upload", tags=["upload"])


@router.post("/file")
async def upload_file(
    file: UploadFile = File(..., description="The document file to upload and analyze"),
    activity_id: Optional[str] = Form(None, description="Activity ID to associate with the upload. If not provided, a new UUID will be generated."),
    file_upload_service: FileUploadDep = None
) -> Dict[str, Any]:
    """
    Upload and process a document file
    
    This endpoint accepts a document file upload along with an optional activity ID.
    The file will be stored and processed for content extraction.
    
    Args:
        file: The document file to upload and analyze
        activity_id: Optional activity ID. If omitted, a UUID will be auto-generated.
        file_upload_service: Injected FileUpload service
        
    Returns:
        Dictionary containing status, file_id, file metadata, and processing status
        
    Raises:
        HTTPException: 500 if file upload or processing fails
    """
    try:
        # Generate unique file ID
        file_id = str(uuid.uuid4())

        activity_id = activity_id if activity_id else str(uuid.uuid4())
        
        logger.info(f"Received file upload: {file.filename} with file_id {file_id} and activity_id {activity_id}")
        
        # Extract content using the injected service
        result = file_upload_service.upload(
            file=file.file,
            file_id=file_id,
            activity_id=activity_id,
            original_filename=file.filename
        )
        
        logger.info(f"Successfully processed file upload for file_id {file_id} and activity_id {activity_id}")
        
        return {
            "status": "success",
            "data": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
