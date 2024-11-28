class AlertSystem:
    def __init__(self):
        self.alert_definitions = {
            "Engine Speed": {
                "ranges": [
                    {"min": 0, "max": 1850, "color": "GREEN", "alert": None},
                    {"min": 1850, "max": 2000, "color": "AMBER", "alert": "WARNING: Engine Speed Near Limit"},
                    {"min": 2000, "max": 9999, "color": "RED", "alert": "CRITICAL: Engine Overspeed"}
                ],
                "spn_name": "Engine Speed"
            },
            "Engine Oil Pressure": {
                "ranges": [
                    {"min": 0, "max": 0.8, "color": "RED", "alert": "CRITICAL: Low Oil Pressure"},
                    {"min": 0.8, "max": 999, "color": "GREEN", "alert": None}
                ],
                "spn_name": "Engine Oil Pressure"
            },
            "Engine Coolant Temperature": {
                "ranges": [
                    {"min": 0, "max": 95, "color": "GREEN", "alert": None},
                    {"min": 95, "max": 999, "color": "RED", "alert": "CRITICAL: High Coolant Temperature"}
                ],
                "spn_name": "Engine Coolant Temperature"
            },
            "Hydraulic Oil Temperature": {
                "ranges": [
                    {"min": 0, "max": 105, "color": "GREEN", "alert": None},
                    {"min": 105, "max": 999, "color": "RED", "alert": "CRITICAL: High Hydraulic Oil Temperature"}
                ],
                "spn_name": "Hydraulic Temperature"
            }
        }
        
    def check_alert(self, spn_name, value):
        # Skip alert check for "No SPNs defined" or "-" values
        if spn_name == "No SPNs defined" or value == "-":
            return {
                "alert": None,
                "color": None,
                "has_buzzer": False
            }
            
        try:
            # Convert value to float and remove any unit symbols
            value = float(str(value).split()[0])
            
            # Find the matching parameter definition
            param_def = None
            for param_name, definition in self.alert_definitions.items():
                if definition["spn_name"] == spn_name:
                    param_def = definition
                    break
            
            if param_def is None:
                return None
                
            # Check each range
            for range_def in param_def["ranges"]:
                if range_def["min"] <= value <= range_def["max"]:
                    return {
                        "alert": range_def["alert"],
                        "color": range_def["color"],
                        "has_buzzer": True if range_def["color"] == "RED" else False
                    }
            
            # If value is outside all defined ranges, return critical alert
            return {
                "alert": f"CRITICAL: {spn_name} Out of Range",
                "color": "RED",
                "has_buzzer": True
            }
            
        except (ValueError, TypeError) as e:
            return None