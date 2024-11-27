import csv
from datetime import datetime
from pgn_definitions import pgn_definitions

class J1939Parser:
    def __init__(self):
        self.pgn_defs = pgn_definitions.pgn_defs

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
            return None

    def decode_spn(self, data_bytes, spn_info):
        """Decode a single SPN value from the data bytes"""
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
                
            if raw_value is None:
                return None

            # Apply resolution and offset if defined
            resolution = spn_info.get("resolution", 1)
            offset = spn_info.get("offset", 0)
            value = raw_value * resolution + offset

            return value
        except Exception:
            return None

    def create_formatted_output(self, input_file, output_file):
        """Create formatted output file with decoded CAN messages"""
        with open(output_file, 'w') as outfile:
            # Write header
            header = "ID , Timestamp , PGN (Hex) , PGN Definition , SPN Definition , SPN Value\n"
            outfile.write(header)
            outfile.write("-" * 100 + "\n")
            
            # Process input file
            with open(input_file, 'r') as f:
                # Skip header lines
                for _ in range(7):
                    next(f)
                
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        # Extract message info
                        msg_id = row["ID"].strip('"')
                        timestamp = float(row["Time"].strip('"'))
                        formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
                        
                        # Calculate PGN from PDU Format and Specific
                        pdu_f = int(row["PDU-F"].replace("0x", ""), 16)
                        pdu_s = int(row["PDU-S"].replace("0x", ""), 16)
                        pgn_decimal = (pdu_f << 8) | pdu_s
                        pgn_hex = f"0x{pgn_decimal:04X}"
                        
                        # Get PGN definition
                        pgn_info = self.pgn_defs.get(pgn_decimal)
                        if not pgn_info:
                            continue
                            
                        pgn_name = pgn_info["name"]
                        
                        # Extract data bytes
                        data_bytes = []
                        for i in range(8):
                            byte_val = row[f"Byte {i}"]
                            if isinstance(byte_val, str):
                                if '0x' in byte_val :
                                    byte_val = int(byte_val.strip('"'), 16)
                                else:
                                    byte_val = int(byte_val)
                            data_bytes.append(byte_val)
                        
                        # Write base message info
                        base_info = f"{msg_id} | {formatted_time} | {pgn_hex} | {pgn_name}"
                        
                        # Process SPNs if present
                        if not pgn_info["spns"]:
                            outfile.write(f"{base_info} | No SPNs defined | -\n")
                            continue
                            
                        first_spn = True
                        for spn_id, spn_info in pgn_info["spns"].items():
                            spn_value = self.decode_spn(data_bytes, spn_info)
                            if spn_value is not None:
                                if first_spn:
                                    outfile.write(f"{base_info} | {spn_info['name']} | {spn_value:.2f}\n")
                                    first_spn = False
                                else:
                                    outfile.write(f"{' ' * len(base_info)} | {spn_info['name']} | {spn_value:.2f}\n")
                                    
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        continue

def main():
    parser = J1939Parser()
    parser.create_formatted_output("BD-155_13869_RawCANLog.csv", "j1939_decoded_messages.txt")

if __name__ == "__main__":
    main()