from decimal import Decimal
from typing import Union

from homeassistant.helpers.template import Template


async def evaluate_power(power: Union[Template, Decimal]) -> Decimal:
    """When power is a template render it."""

    return power.async_render() if isinstance(power, Template) else Decimal(power)
