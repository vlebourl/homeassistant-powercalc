from __future__ import annotations

from .const import MAX_MIRED, MIN_MIRED


class LightInfo:
    model_id: str

    def __init__(self, model_id: str, min_mired: int = MIN_MIRED, max_mired: int = MAX_MIRED):
        self.model_id = model_id
        self._min_mired = min_mired
        self._max_mired = max_mired

    def get_min_mired(self) -> int:
        return self._min_mired

    def set_min_mired(self, value: int):
        value = max(value, MIN_MIRED)
        self._min_mired = value

    def get_max_mired(self) -> int:
        return self._max_mired

    def set_max_mired(self, value: int):
        value = min(value, MAX_MIRED)
        self._max_mired = value

    min_mired = property(get_min_mired, set_min_mired)
    max_mired = property(get_max_mired, set_max_mired)


class LightController:
    def change_light_state(self, color_mode: str, on: bool = True, **kwargs):
        pass

    def get_light_info(self) -> LightInfo:
        return LightInfo()

    def get_questions(self) -> list[dict]:
        return []

    def process_answers(self, answers):
        pass
