"""
    This a file contains available tuya data
    https://developer.tuya.com/en/docs/iot/standarddescription?id=K9i5ql6waswzq

    Credits: official HA Tuya integration.
    Modified by: xZetsubou
"""

from .base import DPCode, LocalTuyaEntity

CAT_LITTER_BOXES: dict[str, tuple[LocalTuyaEntity, ...]] = {
    # Cat Litter Box
    # https://developer.tuya.com/en/docs/iot/f?id=Kakg309qkmuit
    "msp": (
        LocalTuyaEntity(
            id=DPCode.START,
            name="Cat Litter Box",
            icon="mdi:cat",
        ),
    ),
}
