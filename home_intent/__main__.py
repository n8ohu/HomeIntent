"""Start up HomeIntent"""
import importlib
import logging
import sys

from home_intent import HomeIntent
from settings import Settings


class HomeIntentImportException(Exception):
    pass


def main():
    _setup_logging()
    settings = Settings()
    home_intent = HomeIntent(settings)
    _load_integrations(settings, home_intent)
    home_intent.initialize()


def _setup_logging():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s", level=logging.INFO,
    )


def _load_integrations(settings: Settings, home_intent: HomeIntent):
    components = _get_components(settings)
    loaded_builtin_components = _load_builtin_components(components, home_intent)
    custom_components = components.difference(loaded_builtin_components)
    if custom_components:
        _load_custom_components(custom_components, home_intent)


def _get_components(settings: Settings):
    components = set()
    for component in settings.dict():
        component_settings = getattr(settings, component)
        if isinstance(component_settings, dict) or component_settings is None:
            components.add(component)

    return components


def _load_builtin_components(components: set, home_intent: HomeIntent):
    loaded_components = set()
    for component in components:
        try:
            integration = importlib.import_module(f"components.{component}")
        except ModuleNotFoundError:  # these are the custom components
            pass
        else:
            loaded_components.add(component)
            integration.setup(home_intent)

    return loaded_components


def _load_custom_components(custom_components: set, home_intent: HomeIntent):
    sys.path.append("/config/custom_components")
    for custom_component in custom_components:
        try:
            integration = importlib.import_module(custom_component)
        except ModuleNotFoundError:
            raise HomeIntentImportException(
                f"Unable to load custom component '{custom_component}' from /config/custom_components"
            )
        else:
            integration.setup(home_intent)


if __name__ == "__main__":
    main()
