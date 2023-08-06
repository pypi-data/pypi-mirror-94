import os
import tempfile
import uuid


def get_tempfile(extension):
    """Get full path to a temporary file with extension."""
    file_name = str(uuid.uuid4())[:6]
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, '%s.%s' % (file_name, extension))
    return file_path
