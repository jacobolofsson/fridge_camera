from unittest.mock import MagicMock, patch

# Patch HW-specific modules
patch.dict(
    "sys.modules",
    {
        "board": MagicMock(),
        "busio": MagicMock(),
        "adafruit_ads1x15": MagicMock(),
        "adafruit_ads1x15.ads1115": MagicMock(),
        "adafruit_ads1x15.analog_in": MagicMock(),
    }
).start()
