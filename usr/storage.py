from django.core.files.storage import FileSystemStorage


class OverwriteStorage(FileSystemStorage):
    """
    Returns same name for existing file and override existing file on save.
    """
    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name):
        """
        Override FileSystemStorage default behavior of giving unique filename
        This will override previously uploaded file, given same filename.
        Important: Do not change this.
        """
        return name