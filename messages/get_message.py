from django.utils import translation
from messages.module_names import MESSAGES, MODULE_NAMES, LANG_INDEX


def get_message(code: str, module: str = None) -> str:
    lang = translation.get_language() or "uz"

    message_template = MESSAGES[lang].get(code, "")

    if "{name}" in message_template and module:
        names_list = MODULE_NAMES.get(module)
        if names_list and isinstance(names_list, (list, tuple)):
            module_name = names_list[LANG_INDEX[lang]]
        else:
            module_name = module
        return message_template.format(name=module_name)

    return message_template