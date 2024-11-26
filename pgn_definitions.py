class PgnDefinitions:
    def __init__(self):
        self.pgn_defs = {
            61441: {
                "name": "Electronic Brake Controller 1 - EBC1",
                "spns": {
                    561: {"name": "ASR Engine Control", "start_bit": 1, "length": 2},
                    562: {"name": "ASR Brake Control", "start_bit": 3, "length": 2},
                    563: {"name": "Anti-Lock Braking (ABS)", "start_bit": 5, "length": 2},
                    1121: {"name": "EBS Brake Switch", "start_bit": 7, "length": 2},
                    521: {"name": "Brake Pedal Position", "start_bit": 2, "length": 1},
                    575: {"name": "ABS Off-road Switch", "start_bit": 5, "length": 2},
                    576: {"name": "ASR Engine Control", "start_bit": 1, "length": 2},
                    577: {"name": "ASR Brake Control", "start_bit": 3, "length": 2},
                    1238: {"name": "ASR Clutch Control", "start_bit": 5, "length": 2},
                    972: {"name": "ASR Engine Control", "start_bit": 1, "length": 2},
                    971: {"name": "ASR Brake Control", "start_bit": 3, "length": 2},
                    970: {"name": "ASR Clutch Control", "start_bit": 5, "length": 2},
                    969: {"name": "ASR Engine Control", "start_bit": 1, "length": 2},
                    973: {"name": "ASR Brake Control", "start_bit": 3, "length": 2},
                    1243: {"name": "ASR Clutch Control", "start_bit": 5, "length": 2},
                    1439: {"name": "ASR Engine Control", "start_bit": 1, "length": 2},
                    1438: {"name": "ASR Brake Control", "start_bit": 3, "length": 2},
                    1793: {"name": "ASR Clutch Control", "start_bit": 5, "length": 2},
                    1481: {"name": "ASR Engine Control", "start_bit": 1, "length": 2},
                    1836: {"name": "ASR Brake Control", "start_bit": 3, "length": 2},
                    1792: {"name": "ASR Clutch Control", "start_bit": 5, "length": 2}
                }
            },
            0: {
                "name": "Torque/Speed Control 1 - TSC1",
                "spns": {
                    695: {"name": "Override Control Mode", "start_bit": 1, "length": 2},
                    696: {"name": "Requested Speed Control Conditions", "start_bit": 3, "length": 2},
                    897: {"name": "Override Control Mode Priority", "start_bit": 5, "length": 2},
                    898: {"name": "Requested Speed/Speed Limit", "start_bit": 2, "length": 2},
                    518: {"name": "Requested Torque/Torque Limit", "start_bit": 4, "length": 1}
                }
            },
            61444: {
                "name": "Electronic Engine Controller 1 - EEC1",
                "spns": {
                    899: {"name": "Engine Torque Mode", "start_byte": 1, "length": 4},
                    512: {"name": "Driver's Demand Engine - Percent Torque", "start_byte": 2, "length": 1},
                    513: {"name": "Actual Engine - Percent Torque", "start_byte": 3, "length": 1},
                    190: {"name": "Engine Speed", "start_byte": 4, "length": 2},
                    1483: {"name": "Source Address of Controlling Device for Engine Control", "start_byte": 6, "length": 1},
                    1675: {"name": "Engine Starter Mode", "start_bit": 7, "length": 4},
                    2432: {"name": "Engine Demand - Percent Torque", "start_byte": 8, "length": 1}
                }
            },
            65262: {
                "name": "Engine Temperature 1 - ET1",
                "spns": {
                    110: {"name": "Engine Coolant Temperature", "start_byte": 1, "length": 1},
                    174: {"name": "Fuel Temperature", "start_byte": 2, "length": 1},
                    175: {"name": "Engine Oil Temperature", "start_byte": 3, "length": 2}
                }
            },
            65263: {
                "name": "Engine Fluid Level/Pressure 1 - EFL/P1",
                "spns": {
                    100: {"name": "Engine Oil Pressure", "start_byte": 4, "length": 1},
                    94: {"name": "Fuel Delivery Pressure", "start_byte": 1, "length": 1},
                    22: {"name": "Extended Crankcase Blow-by Pressure", "start_byte": 2, "length": 1}
                }
            },
            65265: {
                "name": "Cruise Control/Vehicle Speed - CCVS",  
                "spns": {
                    595: {"name": "Cruise Control Active", "start_bit": 4, "length": 2},
                    596: {"name": "Cruise Control Enable Switch", "start_bit": 4, "length": 2},
                    597: {"name": "Brake Switch", "start_bit": 4, "length": 2},
                    598: {"name": "Clutch Switch", "start_bit": 4, "length": 2},
                    599: {"name": "Cruise Control Set Switch", "start_bit": 5, "length": 2},
                    600: {"name": "Cruise Control Coast Switch", "start_bit": 5, "length": 2},
                    601: {"name": "Cruise Control Resume Switch", "start_bit": 5, "length": 2},
                    602: {"name": "Cruise Control Accelerate Switch", "start_bit": 5, "length": 2},
                    86: {"name": "Cruise Control Set Speed", "start_byte": 6, "length": 1},
                    976: {"name": "PTO State", "start_bit": 7, "length": 5},
                    527: {"name": "Cruise Control States", "start_bit": 7, "length": 3},
                    968: {"name": "Engine Idle Increment Switch", "start_bit": 8, "length": 2},
                    967: {"name": "Engine Idle Decrement Switch", "start_bit": 8, "length": 2},
                    966: {"name": "Engine Test Mode Switch", "start_bit": 8, "length": 2},
                    1237: {"name": "Engine Shutdown Override Switch", "start_bit": 8, "length": 2}
                }
            },
            65269: {
                "name": "Ambient Conditions - AMB",
                "spns": {
                    108: {"name": "Barometric Pressure", "start_byte": 1, "length": 1},
                    170: {"name": "Cab Interior Temperature", "start_byte": 2, "length": 2},
                    171: {"name": "Ambient Air Temperature", "start_byte": 4, "length": 2}
                }
            },
            65270: {
                "name": "Inlet/Exhaust Conditions 1 - IC1",
                "spns": {
                    102: {"name": "Boost Pressure", "start_byte": 2, "length": 1},
                    105: {"name": "Intake Manifold 1 Temperature", "start_byte": 3, "length": 1},
                    106: {"name": "Air Inlet Pressure", "start_byte": 4, "length": 1},
                    107: {"name": "Air Filter 1 Differential Pressure", "start_byte": 5, "length": 1},
                    173: {"name": "Exhaust Gas Temperature", "start_byte": 6, "length": 2}
                }
            },
            65271: {
                "name": "Vehicle Electrical Power - VEP", 
                "spns": {
                    114: {"name": "Net Battery Current", "start_byte": 1, "length": 1},
                    115: {"name": "Alternator Current", "start_byte": 2, "length": 1},
                    168: {"name": "Battery Potential / Voltage", "start_byte": 5, "length": 2}
                }
            },
            65272: {
                "name": "Transmission Fluids - TF",
                "spns": {
                    124: {"name": "Transmission Oil Level", "start_byte": 2, "length": 1},
                    127: {"name": "Transmission Oil Pressure", "start_byte": 4, "length": 1},
                    177: {"name": "Transmission Oil Temperature", "start_byte": 5, "length": 2}
                }    
            }
        }

    def get_pgn_info(self, pgn):
        return self.pgn_defs.get(pgn)

pgn_definitions = PgnDefinitions()