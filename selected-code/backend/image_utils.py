from io import BytesIO
from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from PIL import Image, ImageOps, UnidentifiedImageError

from .upload_paths import get_product_image_url, get_product_upload_directory


MAX_PRODUCT_IMAGE_BYTES = 2 * 1024 * 1024
PRODUCT_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
PRODUCT_IMAGE_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
PRODUCT_IMAGE_SIZE = (300, 300)


def _product_image_error(message: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


async def save_optimized_product_image(file: UploadFile, vendor_id: UUID) -> str:
    extension = Path(file.filename or "").suffix.lower()
    if extension not in PRODUCT_IMAGE_EXTENSIONS:
        raise _product_image_error("Product image must be a JPG, PNG, or WebP file")

    if file.content_type not in PRODUCT_IMAGE_CONTENT_TYPES:
        raise _product_image_error("Product image must be a JPG, PNG, or WebP file")

    contents = await file.read(MAX_PRODUCT_IMAGE_BYTES + 1)
    if len(contents) > MAX_PRODUCT_IMAGE_BYTES:
        raise _product_image_error("Product image must be 2 MB or smaller")

    if not contents:
        raise _product_image_error("Product image file is empty")

    try:
        image = Image.open(BytesIO(contents))
        image.verify()
        image = Image.open(BytesIO(contents))
    except (UnidentifiedImageError, OSError) as exc:
        raise _product_image_error("Product image file is invalid") from exc

    image = ImageOps.exif_transpose(image)
    if image.mode not in {"RGB", "RGBA"}:
        image = image.convert("RGBA" if "A" in image.getbands() else "RGB")

    image.thumbnail(PRODUCT_IMAGE_SIZE, Image.Resampling.LANCZOS)

    output = BytesIO()
    for quality in (75, 72, 70, 68, 65):
        output.seek(0)
        output.truncate()
        image.save(output, format="WEBP", quality=quality, method=6)
        if output.tell() <= 30 * 1024:
            break

    vendor_directory = get_product_upload_directory(vendor_id)
    vendor_directory.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}.webp"
    destination = vendor_directory / filename
    destination.write_bytes(output.getvalue())

    return get_product_image_url(vendor_id, filename)
