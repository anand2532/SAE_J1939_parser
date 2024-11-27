class PgnDefinitions:
    def __init__(self):
        self.pgn_defs = {
            65257: {
                "name": "Fuel Consumption (Liquid) - LFC",
                "spns": {
                    182: {"name": "Trip Fuel", "start_byte": 1, "length": 4,"resolution": 0.5, "offset": 0},
                    250: {"name": "Total Fuel Used", "start_byte": 5, "length": 4,"resolution": 0.5, "offset": 0}
                }
            },
            65271: {
                "name": "Vehicle Electrical Power - VEP",
                "spns": { 
                    114: {"name": "Net Battery Current", "start_byte": 1, "length": 1},
                    115: {"name": "Alternator Current", "start_byte": 2, "length": 1},  
                    167: {"name": "Battery Voltage", "start_byte": 3, "length": 2},
                    168: {"name": "Battery Potential / Voltage", "start_byte": 5, "length": 2},
                    158: {"name": "Battery Current", "start_byte": 7, "length": 2},
                }   
                        },
            61441: {
                "name": "Electronic Brake Controller 1 - EBC1",
                "spns": {
                    561: {"name": "ASR Engine Control Active", "start_bit": 1, "length": 2},
                    562: {"name": "ASR Brake Control Active", "start_bit": 3, "length": 2},
                    563: {"name": "Anti-Lock Braking (ABS) Active", "start_bit": 5, "length": 2},
                    1121: {"name": "EBS Brake Switch", "start_bit": 7, "length": 2},
                    521: {"name": "Brake Pedal Position", "start_byte": 2, "length": 1},
                    575: {"name": "ABS Off-road Switch", "start_bit": 17, "length": 2},
                    576: {"name": "ASR Off-road Switch", "start_bit": 19, "length": 2},
                    577: {"name": "ASR Hill Holder Switch", "start_bit": 21, "length": 2},
                    1238: {"name": "Traction Control Override Switch", "start_bit": 23, "length": 2},
                    972: {"name": "Accelerator Interlock Switch", "start_bit": 25, "length": 2},
                    971: {"name": "Engine Derate Switch", "start_bit": 27, "length": 2},
                    970: {"name": "Auxiliary Engine Shutdown Switch", "start_bit": 29, "length": 2},
                    969: {"name": "Remote Accelerator Enable Switch", "start_bit": 31, "length": 2},
                    973: {"name": "Engine Retarder Selection", "start_byte": 5, "length": 1},
                    1243: {"name": "ABS Fully Operational", "start_bit": 41, "length": 2},
                    1439: {"name": "EBS Red Warning Signal", "start_bit": 43, "length": 2},
                    1438: {"name": "ABS/EBS Amber Warning Signal", "start_bit": 45, "length": 2},
                    1793: {"name": "ATC/ASR Information Signal", "start_bit": 47, "length": 2},
                    1481: {"name": "Source Address of Controlling Device for Brake Control", "start_byte": 7, "length": 1},
                    1836: {"name": "Trailer ABS Status", "start_bit": 61, "length": 2},
                    1792: {"name": "Tractor-Mounted Trailer ABS Warning Signal", "start_bit": 63, "length": 2}
                }
            },
            65266: {
                "name": "Fuel Economy (Liquid) - LFE",
                "spns": {
                    183: {"name": "Fuel Rate", "start_byte": 1, "length": 2},
                    184: {"name": "Instantaneous Fuel Economy1", "start_byte": 3, "length": 2},
                    185: {"name": "Average Fuel Economy", "start_byte": 5, "length": 2},
                    51: {"name": "Throttle Position", "start_byte": 7, "length": 2},
                }

            },
            65247: {
                "name": "Electronic Engine Controller 3 - EEC3",
                "spns": {
                    514: {"name": "Engine Torque Mode", "start_byte": 1, "length": 1},
                    515: {"name": "Driver's Demand Engine - Percent Torque", "start_byte": 2, "length": 2},
                }
            },
            61444: {
                "name" : "Electronic Engine Controller 1 - EEC1",
                "spns" : {
                    899: {"name": "Engine Torque Mode", "start_byte": 1, "length": 4},
                    512: {"name": "Driver's Demand Engine - Percent Torque", "start_byte": 2, "length": 1},
                    513: {"name": "Actual Engine - Percent Torque", "start_byte": 3, "length": 1},
                    190: {"name": "Engine Speed", "start_byte": 4, "length": 2},
                    1483: {"name": "Source Address of Controlling Device for Engine Control", "start_byte": 6, "length": 1},
                    1675: {"name": "Engine Starter Mode", "start_bit": 7, "length": 4},
                }
            },

            65270: {
                "name": "Inlet/Exhaust Conditions 1 - IC1",
                "spns": {
                    81: {"name": "Particulate Trap Inlet Pressure", "start_byte": 1, "length": 1},
                    102: {"name": "Boost Pressure", "start_byte": 2, "length": 1},
                    105: {"name": "Intake Manifold 1 Temperature", "start_byte": 3, "length": 1},
                    106: {"name": "Air Inlet Pressure", "start_byte": 4, "length": 1},
                    107: {"name": "Air Filter 1 Differential Pressure", "start_byte": 5, "length": 1},
                    173: {"name": "Exhaust Gas Temperature", "start_byte": 6, "length": 2},
                    112: {"name": "Coolant Filter Differential Pressure", "start_byte": 8, "length": 1}
                }
            },
            65253: {
                "name": "Engine Hours, Revolutions - HOURS",
                "spns": {
                    247: {"name": "Total Engine Hours", "start_byte": 1, "length": 4},
                    249: {"name": "Total Engine Revolutions", "start_byte": 5, "length": 4}
                }
            },
            65271: {
                "name": "Vehicle Electrical Power - VEP",
                "spns": {
                    114: {"name": "Net Battery Current", "start_byte": 1, "length": 1},
                    115: {"name": "Alternator Current", "start_byte": 2, "length": 1},  
                    167: {"name": "Battery Voltage", "start_byte": 3, "length": 2},
                    168: {"name": "Battery Potential / Voltage", "start_byte": 5, "length": 2},
                    158: {"name": "Battery Current", "start_byte": 7, "length": 2},
                }
            },
            65128: {
                "name": "Vehicle Fluids - VF",
                "spns": {
                    1638: {"name": "Hydraulic Temperature", "start_byte": 1, "length": 1},
                }
            },
            65108: {
                "name": "Engine Continious Torque / Speed Limit - ECT/RPM",
                "spns": {
                    1768: {"name": "Low Limit Threshhold for Maximum RPM from Engine", "start_byte": 1, "length": 1},
                    1769: {"name": "High Limit Threshhold for Minimum Continuous Engine RPM", "start_byte": 2, "length": 1},
                    1770: {"name": "Low Limit Threshold for Maximum Torque from Engine", "start_byte": 3, "length": 1},
                    1771: {"name": "High Limit Threshhold for Minimum Continuous Torque from Engine", "start_byte": 4, "length": 1},
                    1772: {"name": "Maximum Continuous Engine RPM", "start_byte": 5, "length": 1},
                    1773: {"name": "Minimum Continuous Engine RPM", "start_byte": 6, "length": 1},
                    1774: {"name": "Maximum Continuous Engine Torque", "start_byte": 7, "length": 1},
                    1775: {"name": "Minimum Continuous Engine Torque", "start_byte": 8, "length": 1},
                }
            },
            65262: {
                "name": "Engine Temperature 1 - ET1",
                "spns": {
                    110: {"name": "Engine Coolant Temperature", "start_byte": 1, "length": 1},
                    174: {"name": "Fuel Temperature", "start_byte": 2, "length": 1},
                    175: {"name": "Engine Oil Temperature 1", "start_byte": 3, "length": 2},
                    176: {"name": "Turbo Oil Temperature", "start_byte": 5, "length": 2},
                    52: {"name": "Engine Intercooler Temperature", "start_byte": 7, "length": 1},
                    1134: {"name": "Engine Intercooler Thermostat Opening", "start_byte": 8, "length": 1},

                }
            },
            65276: {
                "name" : "Dash Display",
                "spns": {
                    80: {"name": "Washer Fluid Level", "start_byte": 1, "length": 1},
                    96: {"name": "Fluid Level", "start_byte": 2, "length": 1},
                    95: {"name": "Fuel Filter Differential Pressure", "start_byte": 3, "length": 1},
                    99: {"name": "Engine Oil Filter Differential Pressure", "start_byte": 4, "length": 1},
                    169:{"name": "Cargo Ambient Temperature", "start_byte": 5, "length": 2},
                }
            },
            65263: {
                "name" : "Engine Fluid Level/Pressure 1 - EFL/P1",
                "spns": {
                    94: {"name": "Fuel Delivery Pressure", "start_byte": 1, "length": 1},
                    22: {"name": "Extended Crankcase Blow-by Pressure", "start_byte": 2, "length": 1},
                    98: {"name": "Engine Oil Level", "start_byte": 3, "length": 1},
                    100: {"name": "Engine Oil Pressure", "start_byte": 4, "length": 1},
                    101: {"name": "Crakecase Pressure", "start_byte": 5, "length": 2},
                    109: {"name": "Coolant Pressure", "start_byte": 7, "length": 1},
                    111: {"name": "Coolant Level", "start_byte": 8, "length": 1},
                }
            },
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
                    899: {"name": "Engine Torque Mode", "start_bit": 1, "length": 4},
                    512: {"name": "Driver's Demand Engine - Percent Torque", "start_byte": 2, "length": 1},
                    513: {"name": "Actual Engine - Percent Torque", "start_byte": 3, "length": 1},
                    190: {"name": "Engine Speed", "start_byte": 4, "length": 2, "resolution": 0.125, "offset": 0},
                    1483: {"name": "Source Address of Controlling Device for Engine Control", "start_byte": 6, "length": 1},
                    1675: {"name": "Engine Starter Mode", "start_bit": 49, "length": 4},
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
                    94: {"name": "Fuel Delivery Pressure", "start_byte": 1, "length": 1, "resolution": 4},
                    22: {"name": "Extended Crankcase Blow-by Pressure", "start_byte": 2, "length": 1, "resolution": 0.05},
                    98: {"name": "Engine Oil Level", "start_byte": 3, "length": 1, "resolution": 0.4},
                    100: {"name": "Engine Oil Pressure", "start_byte": 4, "length": 1, "resolution": 4},
                    101: {"name": "Crankcase Pressure", "start_byte": 5, "length": 2, "resolution": 0.03125, "offset": -250},
                    109: {"name": "Coolant Pressure", "start_byte": 7, "length": 1, "resolution": 2},
                    111: {"name": "Coolant Level", "start_byte": 8, "length": 1, "resolution": 0.4}
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
            },
            65170: {
                "name": "Engine Information - EI",
                "spns": {
                    1208: {"name": "Pre-filter Oil Pressurer", "start_byte": 1, "length": 1},
                    1209: {"name": "Exhaust Gas Pressure", "start_byte": 2, "length": 2},
                    1210: {"name": "Fuel Rack Position", "start_byte": 4, "length": 1},
                    1241: {"name": "Mass Flow (Gaseous)", "start_byte": 5, "length": 2},
                    1242: {"name": "Instantaneous Estimated Brake Power", "start_byte": 7, "length": 2}
                }
            },
            60415: {
                "name": "Definition not Present in SAE J1939 Standard",
                "spns": {
                    
                }
            },
            60671: {
                "name": "Definition not Present in SAE J1939 Standard",
                "spns": {
                    
                }
            },

            59647: {
                "name": "Definition not Present in SAE J1939 Standard",
                "spns": {
                    
                }
            },
            65226: {
                "name": "Definition not Present in SAE J1939 Standard",
                "spns": {
                    
                }
            },
            65284: {
                "name": "A value of 0xFF00 to 0xFFFF indicates that no transmission torque limit is desired",
                "spns": {

                }
            },
            65285: {
                "name": "A value of 0xFF00 to 0xFFFF indicates that no transmission torque limit is desired",
                "spns": {

                }
            },
            65282: {
                "name": "A value of 0xFF00 to 0xFFFF indicates that no transmission torque limit is desired",
                "spns": {

                }
            },
            65281: {
                "name": "A value of 0xFF00 to 0xFFFF indicates that no transmission torque limit is desired",
                "spns": {

                }
            },
            65280: {
                "name": "A value of 0xFF00 to 0xFFFF indicates that no transmission torque limit is desired",
                "spns": {

                }
            },
            65283: {
                "name": "A value of 0xFF00 to 0xFFFF indicates that no transmission torque limit is desired",
                "spns": {
                    
                }
            }
        }

    def get_pgn_info(self, pgn):
        return self.pgn_defs.get(pgn)

pgn_definitions = PgnDefinitions()