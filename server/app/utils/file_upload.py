import os
import uuid
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file, upload_folder='uploads'):
    """Validate and save an uploaded file safely."""
    try:
        if not file or not file.filename:
            return None, "No file provided."

        if not allowed_file(file.filename):
            return None, "File type not allowed."

        # Check file size if content_length is available
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > MAX_FILE_SIZE:
            return None, "File exceeds maximum allowed size (5MB)."

        os.makedirs(upload_folder, exist_ok=True)

        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        safe_name = secure_filename(filename)
        file_path = os.path.join(upload_folder, safe_name)

        file.save(file_path)

        return {
            "filename": safe_name,
            "url": f"/uploads/{safe_name}",
            "size": file_size
        }, "File uploaded successfully."

    except Exception as e:
        return None, f"Upload failed: {str(e)}"
