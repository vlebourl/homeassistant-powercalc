from __future__ import annotations

from homeassistant_api import Client

from .const import MAX_MIRED, MIN_MIRED, MODE_COLOR_TEMP, MODE_HS
from .controller import LightController, LightInfo
from .errors import LightControllerError

NAME = "hass"


class HassLightController(LightController):
    def __init__(self, api_url: str, token: str):
        try:
            self.client = Client(api_url, token)
        except Exception as e:
            raise LightControllerError(f"Failed to connect to HA API: {e}")

    def change_light_state(self, color_mode: str, on: bool = True, **kwargs):
        if not on:
            self.client.trigger_service('light', 'turn_off', entity_id=self._entity_id)
            return

        if color_mode == MODE_HS:
            json = self.build_hs_json_body(**kwargs)
        elif color_mode == MODE_COLOR_TEMP:
            json = self.build_ct_json_body(**kwargs)
        else:
            json = self.build_bri_json_body(**kwargs)

        self.client.trigger_service('light', 'turn_on', **json)

    def get_light_info(self) -> LightInfo:
        state = self.client.get_state(self._entity_id)
        min_mired = state.attributes.get("min_mireds") or MIN_MIRED
        max_mired = state.attributes.get("max_mireds") or MAX_MIRED
        return LightInfo(self._model_id, min_mired, max_mired)

    def get_questions(self) -> list[dict]:
        entities = self.client.get_entities()
        lights = entities["light"].entities.values()
        light_list = sorted([entity.entity_id for entity in lights])

        return [
            {
                "type": "list",
                "name": "light_entity_id",
                "message": "Select the light?",
                "choices": light_list,
            },
            {
                "type": "input",
                "name": "light_model_id",
                "message": "What model is your light? Ex: LED1837R5",
                "validate": lambda val: len(val) > 0 or "This is required",
            },
        ]

    def process_answers(self, answers):
        self._entity_id = answers["light_entity_id"]
        self._model_id = answers["light_model_id"]

    def build_hs_json_body(self, bri: int, hue: int, sat: int) -> dict:
        return {
            "entity_id": self._entity_id,
            "brightness": bri,
            "hs_color": [hue / 65535 * 360, sat / 255 * 100],
        }

    def build_ct_json_body(self, bri: int, ct: int) -> dict:
        return {"entity_id": self._entity_id, "brightness": bri, "color_temp": ct}

    def build_bri_json_body(self, bri: int) -> dict:
        return {"entity_id": self._entity_id, "brightness": bri}
