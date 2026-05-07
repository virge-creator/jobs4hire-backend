import uuid
from fastapi import APIRouter, Query, HTTPException
import boto3
from botocore.exceptions import ClientError

from app.config import settings

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.get("/presigned-url")
async def get_presigned_upload_url(
    filename: str = Query(..., description="Filename for the upload"),
    content_type: str = Query(..., description="MIME type of the file"),
):
    """
    Generate a presigned S3 URL for direct file upload.
    Used for avatars, CVs, and resume uploads.
    """
    # Validate content type
    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/gif",
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ]
    if content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Content type '{content_type}' not allowed. Allowed: {', '.join(allowed_types)}"
        )

    # Generate unique key
    file_extension = filename.rsplit(".", 1)[-1] if "." in filename else ""
    unique_filename = f"{uuid.uuid4()}.{file_extension}" if file_extension else str(uuid.uuid4())
    s3_key = f"uploads/{unique_filename}"

    try:
        # Create S3 client
        s3_client = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )

        # Generate presigned URL for PUT
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.aws_s3_bucket,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=3600,  # 1 hour
            HttpMethod="PUT",
        )

        # Public URL for accessing the file after upload
        public_url = f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{s3_key}"

        return {
            "presigned_url": presigned_url,
            "public_url": public_url,
            "s3_key": s3_key,
            "expires_in": 3600,
        }

    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")
