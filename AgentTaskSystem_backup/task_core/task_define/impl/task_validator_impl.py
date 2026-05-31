from AgentTaskSystem.task_core.task_define.interfaces.i_task_validator import ITaskValidator


class TaskValidatorImpl(ITaskValidator):

    def __init__(self):
        self._type_whitelist = {
            "str", "int", "float", "bool", "list", "dict", "tuple", "set"
        }

    def validate_name(self, name: str) -> bool:
        if not name:
            return False
        return len(name) <= 64 and name.isalnum()

    def validate_params(self, params: list[dict]) -> tuple[bool, str]:
        if len(params) > 10:
            return False, "Too many parameters"
        for param in params:
            if "name" not in param:
                return False, "Missing parameter name"
        return True, ""

    def validate_type_hint(self, type_hint: str) -> bool:
        return type_hint in self._type_whitelist
