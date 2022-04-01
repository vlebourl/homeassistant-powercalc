from __future__ import annotations

import os

from phue import Bridge, PhueRegistrationException
from PyInquirer import Separator

from .controller import LightController, LightInfo
from .errors import LightControllerError, ModelNotDiscoveredError

NAME = "hue"
TYPE_LIGHT = "light"
TYPE_GROUP = "group"

class HueLightController(LightController):
    def __init__(self, bridge_ip: str):
        self.bridge = self.initialize_hue_bridge(bridge_ip)

    def change_light_state(self, color_mode: str, on: bool = True, **kwargs):
        kwargs["on"] = on
        if self.is_group:
            self.bridge.set_group(self.light_id, kwargs)
        else:
            self.bridge.set_light(self.light_id, kwargs)

    def get_light_info(self) -> LightInfo:
        if self.is_group:
            model_id = self.find_group_model(self.light_id)
            return LightInfo(
                model_id=model_id,
            )
        
        # Individual light information
        light = self.bridge.get_light(self.light_id)
        lightinfo = LightInfo(
            model_id=light["modelid"],
        )

        if "ct" in light["capabilities"]["control"]:
            lightinfo.min_mired = light["capabilities"]["control"]["ct"]["min"]
            lightinfo.max_mired = light["capabilities"]["control"]["ct"]["max"]

        return lightinfo

    def find_group_model(self, group_id: str) -> str:
        model_ids = set()
        for light_id in self.bridge.get_group(group_id, "lights"):
            light = self.bridge.get_light(int(light_id))
            model_id = light["modelid"]
            model_ids.add(model_id)

        if not model_ids:
            raise ModelNotDiscoveredError("Could not find a model id for the group")

        if len(model_ids) > 1:
            raise LightControllerError("The Hue group contains lights of multiple models, this is not supported")

        return model_ids.pop()


    def initialize_hue_bridge(self, bridge_ip: str) -> Bridge:
        config_file_path = os.path.join(os.path.dirname(__file__), "../.persistent/.python_hue")
        try:
            bridge = Bridge(ip=bridge_ip, config_file_path=config_file_path)
        except PhueRegistrationException as err:
            print("Please click the link button on the bridge, than hit enter..")
            input()
            bridge = Bridge(ip=bridge_ip, config_file_path=config_file_path)

        return bridge

    def get_questions(self) -> list[dict]:

        def get_light_list(answers):
            light_list = [
                {"value": f"{TYPE_LIGHT}:{light.light_id}", "name": light.name}
                for light in self.bridge.lights
            ]

            if answers["multiple_lights"]:
                light_list.append(Separator())
                light_list.extend(
                    {"value": f"{TYPE_GROUP}:{group.group_id}", "name": group.name}
                    for group in self.bridge.groups
                )

            return light_list

        return [
            {
                "type": "list",
                "name": "light",
                "message": "Select the light?",
                "choices": get_light_list,
            },
        ]

    def process_answers(self, answers):
        light_type, light_id = answers["light"].split(":")
        self.is_group = light_type == TYPE_GROUP
        self.light_id = int(light_id)
