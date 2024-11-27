# can_decoder.py
import csv
import logging
from datetime import datetime
import json
from pgn_definitions import pgn_definitions

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='can_decoder.log'
)

class CANDecoder:
    def __init__(self):
        self.stats = {
            "total_messages": 0,
            "decoded_messages": 0,
            "unknown_pgns": 0,
            "error_messages": 0
        }
        self.pgn_defs = pgn_definitions
        self.unknown_pgn_list = set()  # Track unknown PGNs

    def extract_bits(self, data_bytes, start_bit, length):
        """Extract specific bits from byte array"""
        try:
            start_byte = (start_bit - 1) // 8
            bit_offset = (start_bit - 1) % 8
            
            value = 0
            bits_remaining = length
            
            while bits_remaining > 0 and start_byte < len(data_bytes):
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

    def decode_spn(self, data_bytes, spn_info):
        """Decode a single SPN from the data bytes"""
        try:
            # Handle byte-based SPN
            if "start_byte" in spn_info:
                start_idx = spn_info["start_byte"] - 1
                length = spn_info["length"]
                
                raw_value = 0
                for i in range(length):
                    if start_idx + i < len(data_bytes):
                        raw_value |= data_bytes[start_idx + i] << (8 * i)
            
            # Handle bit-based SPN
            else:
                raw_value = self.extract_bits(data_bytes, spn_info["start_bit"], spn_info["length"])

            # Apply resolution and offset if defined
            resolution = spn_info.get("resolution", 1)
            offset = spn_info.get("offset", 0)
            value = raw_value * resolution + offset

            return value, raw_value
            
        except Exception as e:
            raise ValueError(f"SPN decoding error: {str(e)}")

    def decode_pgn_data(self, pgn, data_bytes):
        """Decode PGN data using SPN definitions"""
        pgn_info = self.pgn_defs.get_pgn_info(pgn)
        if not pgn_info:
            self.unknown_pgn_list.add(pgn)  # Add to unknown PGNs
            return None

        result = {
            "pgn_name": pgn_info["name"],
            "spns": {}
        }

        # If PGN is defined but has no SPNs, still consider it decoded
        if not pgn_info["spns"]:
            return result

        # Decode SPNs if present
        for spn_id, spn_info in pgn_info["spns"].items():
            try:
                value, raw_value = self.decode_spn(data_bytes, spn_info)
                result["spns"][spn_info["name"]] = {
                    "value": value,
                    "raw_value": raw_value
                }
            except Exception as e:
                result["spns"][spn_info["name"]] = {
                    "error": str(e)
                }

        return result

    def decode_message(self, message_data):
        """Decode a single CAN message"""
        try:
            # Extract base message information
            decoded = {
                "id": message_data["ID"].strip('"'),
                "timestamp": float(message_data["Time"].strip('"')),
                "type": message_data["Type"].strip('"'),
                "priority": int(message_data["Priority"].strip('"')),
                "data_page": int(message_data["Data Page"].strip('"')),
                "pdu_format": message_data["PDU-F"].strip('"'),
                "pdu_specific": message_data["PDU-S"].strip('"'),
                "source_address": message_data["Source Address"].strip('"'),
                "pgn": message_data["PGN"].strip('"'),
                "pid": message_data["PID"].strip('"')
            }

            # Extract data bytes
            data_bytes = []
            for i in range(8):
                byte_val = message_data[f"Byte {i}"]
                if isinstance(byte_val, str):
                    if '0x' in byte_val:
                        byte_val = int(byte_val.strip('"'), 16)
                    else:
                        byte_val = int(byte_val)
                data_bytes.append(byte_val)
            decoded["data_bytes"] = [f"0x{b:02X}" for b in data_bytes]

            # Calculate PGN from PDU Format and Specific
            pdu_f = int(decoded["pdu_format"].replace("0x", ""), 16)
            pdu_s = int(decoded["pdu_specific"].replace("0x", ""), 16)
            pgn_decimal = (pdu_f << 8) | pdu_s

            # Decode PGN data
            pgn_data = self.decode_pgn_data(pgn_decimal, data_bytes)
            if pgn_data:
                decoded.update(pgn_data)
                self.stats["decoded_messages"] += 1
            else:
                self.stats["unknown_pgns"] += 1

            return decoded

        except Exception as e:
            self.stats["error_messages"] += 1
            return {
                "error": str(e),
                "raw_message": message_data
            }

    def decode_can_log(self, filename):
        """Process entire CAN log file"""
        decoded_messages = []
        try:
            with open(filename, 'r') as f:
                # Skip first 7 lines (header info)
                for _ in range(7):
                    next(f)
                
                reader = csv.DictReader(f)
                for row in reader:
                    self.stats["total_messages"] += 1
                    decoded = self.decode_message(row)
                    decoded_messages.append(decoded)
                    
                    if self.stats["total_messages"] % 1000 == 0:
                        logging.info(f"Processed {self.stats['total_messages']} messages")
            
            return decoded_messages
        except Exception as e:
            logging.error(f"Error processing file: {str(e)}")
            raise

    def save_decoded_data(self, decoded_data, output_file):
        """Save decoded data to output files"""
        try:
            # Save human-readable text output
            with open(output_file, 'w') as f:
                # Write vehicle info header
                f.write("BEML BD-155 CAN Message Decoder Output\n")
                f.write("=" * 50 + "\n")
                f.write("VIN: 13869\n")
                f.write("Make: BEML LTD\n")
                f.write("Model: BD-155\n\n")
                
                # Write statistics
                f.write("Statistics:\n")
                f.write("-" * 20 + "\n")
                for stat, value in self.stats.items():
                    f.write(f"{stat.replace('_', ' ').title()}: {value}\n")
                f.write("\n")

                # Write list of unknown PGNs
                if self.unknown_pgn_list:
                    f.write("Unknown PGNs:\n")
                    f.write("-" * 20 + "\n")
                    for pgn in sorted(self.unknown_pgn_list):
                        f.write(f"0x{pgn:04X}\n")
                    f.write("\n")
                
                # Write decoded messages
                f.write("Decoded Messages:\n")
                f.write("-" * 20 + "\n")
                
                for message in decoded_data:
                    if "error" in message:
                        f.write(f"\nError: {message['error']}\n")
                        continue

                    f.write(f"\nTimestamp: {datetime.fromtimestamp(message['timestamp'])}\n")
                    f.write(f"ID: {message['id']}\n")
                    f.write(f"Type: {message['type']}\n")
                    f.write(f"PGN: {message['pgn']}\n")
                    
                    if "pgn_name" in message:
                        f.write(f"PGN Name: {message['pgn_name']}\n")
                        if message.get("spns"):
                            f.write("Decoded Values:\n")
                            for spn_name, spn_data in message["spns"].items():
                                if "error" in spn_data:
                                    f.write(f"  {spn_name}: Error - {spn_data['error']}\n")
                                else:
                                    f.write(f"  {spn_name}: {spn_data['value']} (raw: {spn_data['raw_value']})\n")
                    
                    f.write(f"Raw Data: {', '.join(message['data_bytes'])}\n")
                    f.write("-" * 50 + "\n")

            # Save JSON output
            json_file = output_file.replace('.txt', '.json')
            with open(json_file, 'w') as f:
                json.dump({
                    "vehicle_info": {
                        "vin": "13869",
                        "make": "BEML LTD",
                        "model": "BD-155"
                    },
                    "statistics": self.stats,
                    "unknown_pgns": [f"0x{pgn:04X}" for pgn in sorted(self.unknown_pgn_list)],
                    "messages": decoded_data
                }, f, indent=2)

        except Exception as e:
            logging.error(f"Error saving output: {str(e)}")
            raise

def main():
    decoder = CANDecoder()
    input_file = "BD-155_13869_RawCANLog.csv"
    output_file = "decoded_messages.txt"
    
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
        """)
        
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()