from dependency_injector import containers, providers

from lean.components.api_client import APIClient
from lean.components.cli_config_manager import CLIConfigManager
from lean.components.docker_manager import DockerManager
from lean.components.lean_config_manager import LeanConfigManager
from lean.components.lean_runner import LeanRunner
from lean.components.logger import Logger
from lean.components.project_manager import ProjectManager
from lean.components.storage import Storage
from lean.config import Config


class Container(containers.DeclarativeContainer):
    """The Container class contains providers for all components used by the CLI."""
    logger = providers.Singleton(Logger)

    general_storage = providers.Singleton(Storage, file=Config.general_config_file)
    credentials_storage = providers.Singleton(Storage, file=Config.credentials_config_file)

    cli_config_manager = providers.Singleton(CLIConfigManager,
                                             general_storage=general_storage,
                                             credentials_storage=credentials_storage)
    lean_config_manager = providers.Singleton(LeanConfigManager,
                                              cli_config_manager=cli_config_manager,
                                              default_file_name=Config.default_lean_config_file_name)

    api_client = providers.Factory(APIClient,
                                   logger=logger,
                                   base_url=Config.api_base_url,
                                   user_id=cli_config_manager.provided.user_id.get_value(),
                                   api_token=cli_config_manager.provided.api_token.get_value())

    project_manager = providers.Singleton(ProjectManager)

    docker_manager = providers.Singleton(DockerManager, logger=logger)

    lean_runner = providers.Singleton(LeanRunner,
                                      logger=logger,
                                      lean_config_manager=lean_config_manager,
                                      docker_manager=docker_manager,
                                      docker_image=Config.lean_engine_docker_image)


container = Container()
