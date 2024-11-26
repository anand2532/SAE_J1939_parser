# j1939_decoder.py

import csv
import logging
from datetime import datetime
import json
from parameter_ranges import parameter_ranges
from pgn_definitions import pgn_definitions

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='j1939_decoder.log'
)

class J1939Decoder:
    def __init__(self):
        self.pgn_defs = pgn_definitions
        self.param_ranges = parameter_ranges
        self.reset_statistics()

    def reset_statistics(self):
        """Reset decoder statistics"""
        self.stats = {
            "total_messages": 0,
            "decoded_messages": 0,
            "unknown_pgns": 0,
            "error_messages": 0,
            "active_warnings": set()
        }

    def extract_bits(self, data_bytes, start_bit, length):
        """Extract specific bits from byte array"""
        try:
            if not isinstance(start_bit, int) or not isinstance(length, int):
                raise ValueError(f"Start bit and length must be integers: {start_bit}, {length}")

            start_byte = (start_bit - 1) // 8
            bit_offset = (start_bit - 1) % 8
            
            if start_byte >= len(data_bytes):
                raise ValueError(f"Start byte {start_byte} exceeds data length {len(data_bytes)}")
                
            value = 0
            bits_remaining = length
            
            while bits_remaining > 0:
                if start_byte >= len(data_bytes):
                    break
                    
                current_byte = data_bytes[start_byte]
                bits_from_byte = min(8 - bit_offset, bits_remaining)
                
                mask = ((1 << bits_from_byte) - 1) << bit_offset
                extracted = (current_byte & mask) >> bit_offset
                
                value |= extracted << (length - bits_remaining)
                bits_remaining -= bits_from_byte
                start_byte += 1
                bit_offset = 0
                
            return value
        except Exception as e:
            raise ValueError(f"Bit extraction error: {str(e)}")

    def decode_spn(self, data_bytes, spn_info, spn_number):
        """Decode a single SPN from the data bytes"""
        try:
            # Get raw value based on byte or bit position
            if "start_byte" in spn_info:
                start_idx = spn_info["start_byte"] - 1
                length = spn_info["length"]
                
                if start_idx + length > len(data_bytes):
                    raise ValueError(f"Data too short for SPN {spn_number}")
                    
                raw_value = 0
                for i in range(length):
                    raw_value |= data_bytes[start_idx + i] << (8 * i)
            else:
                raw_value = self.extract_bits(data_bytes, spn_info["start_bit"], spn_info["length"])

            # Apply resolution and offset
            resolution = spn_info.get("resolution", 1)
            offset = spn_info.get("offset", 0)
            value = raw_value * resolution + offset

            return value, raw_value
        except Exception as e:
            raise ValueError(f"SPN decoding error: {str(e)}")

    def get_parameter_from_spn(self, spn_name):
        """Map SPN names to parameter names"""
        mapping = {
            "Engine Speed": "ENGINE_RPM",
            "Engine Coolant Temperature": "ENGINE_COOLANT_TEMP",
            "Engine Oil Pressure": "ENGINE_OIL_PRESSURE",
            "Battery Potential (Voltage)": "BATTERY_VOLTAGE",
            "Fuel Level": "FUEL_LEVEL",
            "Hydraulic Oil Temperature": "HYDRAULIC_OIL_TEMP"
        }
        return mapping.get(spn_name)

    def decode_message(self, message_data):
        """Decode a single CAN message"""
        try:
            # Extract base message information
            timestamp = float(message_data.get('Time', 0))
            pdu_f = int(message_data.get('PDU-F', '0'), 16)
            pdu_s = int(message_data.get('PDU-S', '0'), 16)
            pgn = (pdu_f << 8) | pdu_s
            
            # Get PGN definition
            pgn_info = self.pgn_defs.get_pgn_info(pgn)
            if not pgn_info:
                self.stats["unknown_pgns"] += 1
                return {
                    "timestamp": timestamp,
                    "pgn": pgn,
                    "pgn_hex": f"0x{pgn:04X}",
                    "status": "unknown_pgn",
                    "raw_data": [message_data.get(f'Byte {i}', '0') for i in range(8)]
                }
            
            # Extract data bytes
            data_bytes = []
            for i in range(8):
                byte_str = message_data.get(f'Byte {i}', '0')
                if isinstance(byte_str, str):
                    byte_val = int(byte_str, 16) if '0x' in byte_str else int(byte_str)
                else:
                    byte_val = int(byte_str)
                data_bytes.append(byte_val)
            
            # Initialize decoded message
            decoded_values = {}
            spn_errors = []
            
            # Decode each SPN
            for spn, spn_info in pgn_info["spns"].items():
                try:
                    value, raw_value = self.decode_spn(data_bytes, spn_info, spn)
                    
                    # Get parameter status if available
                    param_name = self.get_parameter_from_spn(spn_info["name"])
                    status = {}
                    
                    if param_name:
                        status = self.param_ranges.get_parameter_status(param_name, value)
                        if status and status.get("warning"):
                            self.stats["active_warnings"].add(status["warning_message"])
                    
                    decoded_values[spn_info["name"]] = {
                        "value": value,
                        "raw_value": raw_value,
                        **status
                    }
                    
                except Exception as e:
                    error_msg = f"Error decoding SPN {spn} ({spn_info['name']}): {str(e)}"
                    spn_errors.append(error_msg)
                    logging.warning(error_msg)
            
            self.stats["decoded_messages"] += 1
            return {
                "timestamp": timestamp,
                "pgn": pgn,
                "pgn_hex": f"0x{pgn:04X}",
                "pgn_name": pgn_info["name"],
                "status": "success",
                "values": decoded_values,
                "spn_errors": spn_errors,
                "raw_data": [f"0x{b:02X}" for b in data_bytes]
            }
            
        except Exception as e:
            self.stats["error_messages"] += 1
            error_msg = f"Message decoding failed: {str(e)}"
            logging.error(error_msg)
            return {
                "timestamp": timestamp if 'timestamp' in locals() else 0,
                "status": "error",
                "error": error_msg
            }

    def decode_can_log(self, filename):
        """Process entire CAN log file"""
        self.reset_statistics()
        decoded_messages = []
        
        try:
            with open(filename, 'r') as csvfile:
                # Skip header lines
                for _ in range(7):
                    next(csvfile)
                    
                reader = csv.DictReader(csvfile)
                for row in reader:
                    self.stats["total_messages"] += 1
                    decoded = self.decode_message(row)
                    decoded_messages.append(decoded)
                    
                    if self.stats["total_messages"] % 1000 == 0:
                        logging.info(f"Processed {self.stats['total_messages']} messages...")
                        
            return decoded_messages
            
        except Exception as e:
            logging.error(f"Error processing file {filename}: {str(e)}")
            raise

    def save_decoded_data(self, decoded_data, output_file):
        """Save decoded data to output files"""
        try:
            # # Save detailed JSON output
            # json_file = output_file.replace('.txt', '.json')
            # with open(json_file, 'w') as f:
            #     json.dump({
            #         "statistics": self.stats,
            #         "messages": decoded_data
            #     }, f, indent=2)

            json_file = output_file.replace('.txt', '.json')
            with open(json_file, 'w') as f:
                stats_json = self.stats.copy()
                stats_json["active_warnings"] = list(stats_json["active_warnings"])  # Convert set to list
                json.dump({
                    "statistics": stats_json,
                    "messages": decoded_data
                }, f, indent=2)

            # Save human-readable text output
            with open(output_file, 'w') as f:
                # Write header
                f.write("J1939 CAN Message Decoder Output\n")
                f.write("=" * 50 + "\n\n")
                
                # Write statistics
                f.write("Statistics:\n")
                f.write("-" * 20 + "\n")
                for stat, value in self.stats.items():
                    if stat != "active_warnings":
                        f.write(f"{stat.replace('_', ' ').title()}: {value}\n")
                f.write("\n")
                
                # Write active warnings
                if self.stats["active_warnings"]:
                    f.write("Active Warnings:\n")
                    f.write("-" * 20 + "\n")
                    for warning in sorted(self.stats["active_warnings"]):
                        f.write(f"- {warning}\n")
                    f.write("\n")
                
                # Write parameter ranges
                f.write("Parameter Ranges:\n")
                f.write("-" * 20 + "\n")
                for param, ranges in self.param_ranges.parameter_ranges.items():
                    f.write(f"\n{param} ({ranges['unit']}):\n")
                    for range_def in ranges["ranges"]:
                        f.write(f"  {range_def['min']} to {range_def['max']}: {range_def['color']}")
                        if range_def["warning"]:
                            f.write(f" (Warning: {ranges['warning_message']})")
                            if ranges['warning_buzzer']:
                                f.write(" [WITH BUZZER]")
                        f.write("\n")
                f.write("\n")
                
                # Write decoded messages
                f.write("Decoded Messages:\n")
                f.write("-" * 20 + "\n")
                
                for message in decoded_data:
                    f.write(f"\nTimestamp: {datetime.fromtimestamp(message['timestamp'])}\n")
                    
                    if message["status"] == "success":
                        f.write(f"PGN: {message['pgn_name']} ({message['pgn_hex']})\n")
                        f.write("Values:\n")
                        for name, value_info in message["values"].items():
                            value_str = f"{value_info['value']}"
                            if "unit" in value_info:
                                value_str += f" {value_info['unit']}"
                            if "color" in value_info:
                                value_str += f" ({value_info['color']})"
                            f.write(f"  {name}: {value_str}\n")
                            
                            if value_info.get("warning"):
                                f.write(f"    ** WARNING: {value_info['warning_message']}")
                                if value_info.get("warning_buzzer"):
                                    f.write(" [BUZZER]")
                                f.write(" **\n")
                                
                        if message["spn_errors"]:
                            f.write("Errors:\n")
                            for error in message["spn_errors"]:
                                f.write(f"  {error}\n")
                                
                    elif message["status"] == "unknown_pgn":
                        f.write(f"Unknown PGN: {message['pgn_hex']}\n")
                    else:
                        f.write(f"Error: {message.get('error', 'Unknown error')}\n")
                    
                    f.write(f"Raw Data: {', '.join(message.get('raw_data', []))}\n")

        except Exception as e:
            logging.error(f"Error saving output: {str(e)}")
            raise

def main():
    decoder = J1939Decoder()
    input_file = "BD-155_13869_RawCANLog.csv"
    output_file = "decoded_can_messages.txt"
    
    try:
        logging.info("Starting CAN message decoding...")
        decoded_data = decoder.decode_can_log(input_file)
        
        logging.info("Saving decoded data...")
        decoder.save_decoded_data(decoded_data, output_file)
        
        logging.info(f"""
        Decoding completed:
        - Total messages: {decoder.stats['total_messages']}
        - Successfully decoded: {decoder.stats['decoded_messages']}
        - Unknown PGNs: {decoder.stats['unknown_pgns']}
        - Errors: {decoder.stats['error_messages']}
        - Active warnings: {len(decoder.stats['active_warnings'])}
        """)
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
