import uuid
from imghdr import what as whatImg

from re import sub as reg_sub
from os import makedirs as makeDirectory
from os.path import join as pathJoin

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

from main.extensions import db
from main.logger import event_logger, error_logger

def util_set_params(**kwargs) -> dict:
    """
    Creates and returns a dictionary from provided keyword arguments.

    Returns:
        dict: A dictionary containing all the keyword arguments.
    """
    event_logger.info(f"Set params called with keys: {list(kwargs.keys())}")
    return {key: value for key, value in kwargs.items()}


def util_normalize_string(string: str) -> dict | None:
    """
    Normalizes a string into multiple common naming conventions.

    Args:
        string (str): The input string to normalize.

    Returns:
        dict | None: A dictionary with normalized string formats, or None if input is empty.
    """
    if not string:
        event_logger.warning("util_normalize_string called with empty input")
        return None

    string = reg_sub(r'\s+', ' ', string.strip())
    unified = reg_sub(r'[-_]', ' ', string)

    words = unified.split()
    title = ' '.join(word.capitalize() for word in words)
    cleaned = '-'.join(word.lower() for word in words)
    snake = '_'.join(word.lower() for word in words)
    camel = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    pascal = ''.join(word.capitalize() for word in words)

    event_logger.info(f"Normalized string '{string}' to multiple cases")
    return {
        "original": string,
        "title": title,
        "cleaned": cleaned,
        "snake_case": snake,
        "camel_case": camel,
        "pascal_case": pascal
    }


def util_upload_image(image_file: FileStorage, filename: str, upload_folder: str, allowed_extensions: set[str] = None) -> dict:
    """
    Uploads an image to a specified folder after validating type and securing the filename.

    Args:
        image_file (FileStorage): The uploaded image file from the request.
        filename (str): Desired base filename (without extension).
        upload_folder (str): Directory to upload the image to.
        allowed_extensions (set[str], optional): Set of allowed file extensions.

    Returns:
        dict: Result status with success flag, message, and saved filename & path.
    """
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'webp'}

    def is_allowed(filename: str, stream) -> bool:
        ext = filename.rsplit('.', 1)[-1].lower()
        valid_ext = ext in allowed_extensions
        valid_mime = whatImg(stream) in allowed_extensions
        return valid_ext and valid_mime

    try:
        if not image_file or not image_file.filename:
            error_logger.error("No image file provided for upload")
            return {'success': False, 'error': 'No image file provided'}

        file_ext = image_file.filename.rsplit('.', 1)[-1].lower()
        safe_filename = secure_filename(filename.replace(" ", "-"))
        unique_suffix = uuid.uuid4().hex[:8]
        final_filename = f"{safe_filename}_{unique_suffix}.{file_ext}"
        filepath = pathJoin(upload_folder, final_filename)

        makeDirectory(upload_folder, exist_ok=True)

        event_logger.info(f"Uploading image: {final_filename} to {upload_folder}")

        image_file.seek(0)
        if not is_allowed(image_file.filename, image_file.stream):
            error_logger.error(f"Invalid image file type: {image_file.filename}")
            return {'success': False, 'error': 'Invalid image file type'}

        image_file.seek(0)
        image_file.save(filepath)

        event_logger.info(f"Image uploaded successfully: {final_filename}")
        return {
            'success': True,
            'message': 'Image uploaded successfully',
            'filename': final_filename,
            'filepath': filepath
        }

    except Exception as e:
        error_logger.error(f"Image upload failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def util_db_add(obj) -> dict:
    """
    Adds an object to the database and commits the session.

    Args:
        obj: SQLAlchemy model instance to be added.

    Returns:
        dict: Status message with success flag.
    """
    try:
        db.session.add(obj)
        db.session.commit()
        event_logger.info(f"Added to DB: {obj}")
        return {'success': True, 'message': 'Added successfully'}
    except Exception as e:
        error_logger.error(f"DB add failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def util_db_delete(obj) -> dict:
    """
    Deletes an object from the database and commits the session.

    Args:
        obj: SQLAlchemy model instance to be deleted.

    Returns:
        dict: Status message with success flag.
    """
    try:
        db.session.delete(obj)
        db.session.commit()
        event_logger.info(f"Deleted from DB: {obj}")
        return {'success': True, 'message': 'Deleted successfully'}
    except Exception as e:
        error_logger.error(f"DB delete failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}


def util_db_update() -> dict:
    """
    Commits any pending changes to the database session.

    Returns:
        dict: Status message with success flag.
    """
    try:
        db.session.commit()
        event_logger.info(f"Database session updated successfully")
        return {'success': True, 'message': 'Updated successfully'}
    except Exception as e:
        error_logger.error(f"DB update failed: {e}", exc_info=True)
        return {'success': False, 'error': str(e)}