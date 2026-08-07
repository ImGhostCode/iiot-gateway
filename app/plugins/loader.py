import importlib
import logging

from pathlib import Path

from app.plugins.registry import PluginRegistry


logger = logging.getLogger(__name__)


class PluginLoader:

    def __init__(
        self,
        registry: PluginRegistry,
    ):
        self.registry = registry

    def load(
        self,
        plugin_root: Path,
    ):

        if not plugin_root.exists():

            logger.warning(
                "Plugin directory does not exist: %s",
                plugin_root,
            )

            return

        for folder in sorted(
            plugin_root.iterdir()
        ):

            if (
                not folder.is_dir()
                or folder.name.startswith("_")
            ):
                continue

            module_name = (
                f"app.protocols."
                f"{folder.name}.plugin"
            )

            try:

                module = importlib.import_module(
                    module_name
                )

            except ModuleNotFoundError as exc:

                if exc.name == module_name:
                    continue

                logger.exception(
                    "Dependency error while loading %s",
                    module_name,
                )

                continue

            except Exception:

                logger.exception(
                    "Failed to import plugin module %s",
                    module_name,
                )

                continue

            try:

                plugin_class = getattr(
                    module,
                    "Plugin",
                )

                plugin = plugin_class()

                self.registry.register(
                    plugin
                )

                logger.info(
                    "Loaded plugin '%s' version %s",
                    plugin.info.name,
                    plugin.info.version,
                )

            except Exception:

                logger.exception(
                    "Failed to register plugin from %s",
                    module_name,
                )