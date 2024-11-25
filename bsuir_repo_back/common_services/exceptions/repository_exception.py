class RepositoryException(Exception):
    pass


class RepositoryNotFoundException(RepositoryException):
    def __init__(self, repository_id):
        self.repository_id = repository_id
        self.message = f"Repository with {repository_id} not found!"
        super().__init__(self.message)
