# First file: parameter_ranges.py

class ParameterRanges:
    def __init__(self):
        self.parameter_ranges = {
            "ENGINE_RPM": {
                "ranges": [
                    {"min": 0, "max": 1850, "color": "GREEN", "warning": False},
                    {"min": 1850, "max": 2000, "color": "AMBER", "warning": False},
                    {"min": 2000, "max": 3000, "color": "RED", "warning": True}
                ],
                "warning_message": "OVERSPEED",
                "warning_buzzer": False,
                "unit": "rpm"
            },
            "ENGINE_COOLANT_TEMP": {
                "ranges": [
                    {"min": 40, "max": 95, "color": "GREEN", "warning": False},
                    {"min": 95, "max": 120, "color": "RED", "warning": True}
                ],
                "warning_message": "HIGH COOLANT TEMPERATURE",
                "warning_buzzer": True,
                "unit": "°C"
            },
            "ENGINE_OIL_PRESSURE": {
                "ranges": [
                    {"min": 0, "max": 0.8, "color": "RED", "warning": True},
                    {"min": 0.8, "max": 10, "color": "GREEN", "warning": False}
                ],
                "warning_message": "LOW OIL PRESSURE",
                "warning_buzzer": True,
                "unit": "bar"
            },
            "BATTERY_VOLTAGE": {
                "ranges": [
                    {"min": 8, "max": 22, "color": "RED", "warning": True},
                    {"min": 22, "max": 30, "color": "GREEN", "warning": False},
                    {"min": 30, "max": 36, "color": "RED", "warning": True}
                ],
                "warning_message": "BATTERY VOLTAGE ERROR",
                "warning_buzzer": False,
                "unit": "V"
            },
            "FUEL_LEVEL": {
                "ranges": [
                    {"min": 0, "max": 0.1, "color": "RED", "warning": True},
                    {"min": 0.1, "max": 0.25, "color": "AMBER", "warning": False},
                    {"min": 0.25, "max": 1.0, "color": "GREEN", "warning": False}
                ],
                "warning_message": "LOW FUEL LEVEL",
                "warning_buzzer": False,
                "unit": "%"
            },
            "HYDRAULIC_OIL_TEMP": {
                "ranges": [
                    {"min": 40, "max": 105, "color": "GREEN", "warning": False},
                    {"min": 105, "max": 120, "color": "RED", "warning": True}
                ],
                "warning_message": "HIGH HYDRAULIC OIL TEMPERATURE",
                "warning_buzzer": True,
                "unit": "°C"
            }
        }

    def get_parameter_status(self, parameter, value):
        param_def = self.parameter_ranges.get(parameter)
        if not param_def:
            return None

        for range_def in param_def["ranges"]:
            if range_def["min"] <= value <= range_def["max"]:
                return {
                    "value": value,
                    "unit": param_def["unit"],
                    "color": range_def["color"],
                    "warning": range_def["warning"],
                    "warning_message": param_def["warning_message"] if range_def["warning"] else None,
                    "warning_buzzer": param_def["warning_buzzer"] if range_def["warning"] else False
                }
        return None

parameter_ranges = ParameterRanges()

