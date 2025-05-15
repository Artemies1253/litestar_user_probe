from advanced_alchemy.extensions.litestar import service, repository

from src.users.models import UserModel


class UserRepositoryService(service.SQLAlchemyAsyncRepositoryService[UserModel]):
    class Repo(repository.SQLAlchemyAsyncRepository[UserModel]):
        model_type = UserModel

    repository_type = Repo
