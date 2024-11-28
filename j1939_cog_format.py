# import csv
# from datetime import datetime
# from pgn_definitions import pgn_definitions

# class J1939Parser:
#     def __init__(self):
#         self.pgn_defs = pgn_definitions.pgn_defs

#     def extract_bits(self, data_bytes, start_bit, length):
#         try:
#             start_byte = (start_bit - 1) // 8
#             bit_offset = (start_bit - 1) % 8
            
#             value = 0
#             bits_remaining = length
            
#             while bits_remaining > 0 and start_byte < len(data_bytes):
#                 current_byte = data_bytes[start_byte]
#                 bits_from_byte = min(8 - bit_offset, bits_remaining)
                
#                 mask = ((1 << bits_from_byte) - 1) << bit_offset
#                 extracted = (current_byte & mask) >> bit_offset
                
#                 value |= extracted << (length - bits_remaining)
#                 bits_remaining -= bits_from_byte
#                 start_byte += 1
#                 bit_offset = 0
                
#             return value
#         except Exception as e:
#             return None

#     def decode_spn(self, data_bytes, spn_info):  
#         try:
           
#             if "start_byte" in spn_info:
#                 start_idx = spn_info["start_byte"] - 1
#                 length = spn_info["length"]
                
#                 raw_value = 0
#                 for i in range(length):
#                     if start_idx + i < len(data_bytes):
#                         raw_value |= data_bytes[start_idx + i] << (8 * i)
            
     
#             else:
#                 raw_value = self.extract_bits(data_bytes, spn_info["start_bit"], spn_info["length"])
                
#             if raw_value is None:
#                 return None

           
#             resolution = spn_info.get("resolution", 1)
#             offset = spn_info.get("offset", 0)
#             value = raw_value * resolution + offset

#             return value
#         except Exception:
#             return None

#     def create_formatted_output(self, input_file, output_file):
#         with open(output_file, 'w') as outfile:
           
#             outfile.write("ID,Timestamp,PGN (Hex),PGN Definition,SPN Definitions,SPN Values\n")
#             with open(input_file, 'r') as f:
#                 for _ in range(7):
#                     next(f)
                
#                 reader = csv.DictReader(f)
#                 for row in reader:
#                     try:
#                         msg_id = row["ID"].strip('"')
#                         timestamp = float(row["Time"].strip('"'))
#                         formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
                        
#                         pdu_f = int(row["PDU-F"].replace("0x", ""), 16)
#                         pdu_s = int(row["PDU-S"].replace("0x", ""), 16)
#                         pgn_decimal = (pdu_f << 8) | pdu_s
#                         pgn_hex = f"0x{pgn_decimal:04X}"
                        
#                         pgn_info = self.pgn_defs.get(pgn_decimal)
#                         if not pgn_info:
#                             continue
                            
#                         pgn_name = pgn_info["name"]
                        
#                         data_bytes = []
#                         for i in range(8):
#                             byte_val = row[f"Byte {i}"]
#                             if isinstance(byte_val, str):
#                                 if '0x' in byte_val:
#                                     byte_val = int(byte_val.strip('"'), 16)
#                                 else:
#                                     byte_val = int(byte_val)
#                             data_bytes.append(byte_val)
                        
#                         if not pgn_info["spns"]:
#                             outfile.write(f'"{msg_id}","{formatted_time}","{pgn_hex}","{pgn_name}","No SPNs defined","-"\n')
#                             continue
                        
#                         spn_definitions = []
#                         spn_values = []
                        
#                         for spn_id, spn_info in pgn_info["spns"].items():
#                             spn_value = self.decode_spn(data_bytes, spn_info)
#                             if spn_value is not None:
#                                 spn_definitions.append(spn_info['name'])
#                                 spn_values.append(f"{spn_value:.2f}")
                        
#                         if spn_definitions and spn_values:
#                             spn_defs_str = ', '.join(spn_definitions)
#                             spn_values_str = ', '.join(spn_values)
                    
#                             outfile.write(f'"{msg_id}","{formatted_time}","{pgn_hex}","{pgn_name}","{spn_defs_str}","{spn_values_str}"\n')
                                
#                     except Exception as e:
#                         print(f"Error processing message: {e}")
#                         continue

# def main():
#     parser = J1939Parser()
#     parser.create_formatted_output("BD-155_13869_RawCANLog.csv", "j1939_decoded_messages.txt")

# if __name__ == "__main__":
#     main()



import csv
from datetime import datetime
from pgn_definitions import pgn_definitions

class J1939Parser:
    def __init__(self):
        self.pgn_defs = pgn_definitions.pgn_defs

    def extract_bits(self, data_bytes, start_bit, length):
        try:
            # Convert 1-based bit position to 0-based
            start_bit = start_bit - 1
            
            # Calculate start byte and bit offset
            start_byte = start_bit // 8
            bit_offset = start_bit % 8
            
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
            print(f"Error extracting bits: {e}")
            return None

    def decode_spn(self, data_bytes, spn_info):
        try:
            raw_value = None
            
            # Handle bit-based SPNs
            if "start_bit" in spn_info:
                raw_value = self.extract_bits(data_bytes, spn_info["start_bit"], spn_info["length"])
            
            # Handle byte-based SPNs
            elif "start_byte" in spn_info:
                start_idx = spn_info["start_byte"] - 1  # Convert to 0-based index
                length = spn_info["length"]
                
                raw_value = 0
                for i in range(length):
                    if start_idx + i < len(data_bytes):
                        raw_value |= data_bytes[start_idx + i] << (8 * i)
            
            if raw_value is None:
                return None
            
            # Apply resolution and offset if provided
            resolution = spn_info.get("resolution", 1)
            offset = spn_info.get("offset", 0)
            value = raw_value * resolution + offset
            
            return value
            
        except Exception as e:
            print(f"Error decoding SPN: {e}")
            return None

    def decode_eec1(self, data_bytes):
        """
        Specific decoder for PGN 61444 (EEC1)
        """
        pgn_info = self.pgn_defs[61444]
        results = {}
        
        for spn_id, spn_info in pgn_info["spns"].items():
            value = self.decode_spn(data_bytes, spn_info)
            if value is not None:
                results[spn_info["name"]] = value
        
        return results

    def create_formatted_output(self, input_file, output_file):
        with open(output_file, 'w', newline='') as outfile:
            outfile.write("ID,Timestamp,PGN (Hex),PGN Definition,SPN Definitions,SPN Values\n")
            
            with open(input_file, 'r') as f:
                # Skip header rows
                for _ in range(7):
                    next(f)
                
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        msg_id = row["ID"].strip('"')
                        timestamp = float(row["Time"].strip('"'))
                        formatted_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
                        
                        # Calculate PGN
                        pdu_f = int(row["PDU-F"].replace("0x", ""), 16)
                        pdu_s = int(row["PDU-S"].replace("0x", ""), 16)
                        pgn_decimal = (pdu_f << 8) | pdu_s
                        pgn_hex = f"0x{pgn_decimal:04X}"
                        
                        # Get PGN info
                        pgn_info = self.pgn_defs.get(pgn_decimal)
                        if not pgn_info:
                            continue
                        
                        pgn_name = pgn_info["name"]
                        
                        # Parse data bytes
                        data_bytes = []
                        for i in range(8):
                            byte_val = row[f"Byte {i}"]
                            if isinstance(byte_val, str):
                                if '0x' in byte_val:
                                    byte_val = int(byte_val.strip('"'), 16)
                                else:
                                    byte_val = int(byte_val)
                            data_bytes.append(byte_val)
                        
                        # Special handling for EEC1 (PGN 61444)
                        if pgn_decimal == 61444:
                            results = self.decode_eec1(data_bytes)
                            if results:
                                spn_definitions = list(results.keys())
                                spn_values = [f"{v:.2f}" for v in results.values()]
                                spn_defs_str = ', '.join(spn_definitions)
                                spn_values_str = ', '.join(spn_values)
                                outfile.write(f'"{msg_id}","{formatted_time}","{pgn_hex}","{pgn_name}","{spn_defs_str}","{spn_values_str}"\n')
                        else:
                            # Handle other PGNs as before
                            if not pgn_info["spns"]:
                                outfile.write(f'"{msg_id}","{formatted_time}","{pgn_hex}","{pgn_name}","No SPNs defined","-"\n')
                                continue
                            
                            spn_definitions = []
                            spn_values = []
                            
                            for spn_id, spn_info in pgn_info["spns"].items():
                                spn_value = self.decode_spn(data_bytes, spn_info)
                                if spn_value is not None:
                                    spn_definitions.append(spn_info['name'])
                                    spn_values.append(f"{spn_value:.2f}")
                            
                            if spn_definitions and spn_values:
                                spn_defs_str = ', '.join(spn_definitions)
                                spn_values_str = ', '.join(spn_values)
                                outfile.write(f'"{msg_id}","{formatted_time}","{pgn_hex}","{pgn_name}","{spn_defs_str}","{spn_values_str}"\n')
                                
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        continue

def main():
    parser = J1939Parser()
    parser.create_formatted_output("BD-155_13869_RawCANLog.csv", "j1939_decoded_messages.txt")

if __name__ == "__main__":
    main()