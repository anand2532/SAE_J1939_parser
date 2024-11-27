import socket
import json
import logging
import time
from datetime import datetime
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
        self.unknown_pgn_list = set()

    def parse_can_frame(self, frame_data):

        try:
            # CAN frame format parsing
            can_id = (frame_data[0] << 24) | (frame_data[1] << 16) | (frame_data[2] << 8) | frame_data[3]
            
            # extract J1939 fields from can id
            priority = (can_id >> 26) & 0x7
            data_page = (can_id >> 24) & 0x1
            pdu_format = (can_id >> 16) & 0xFF
            pdu_specific = (can_id >> 8) & 0xFF
            source_address = can_id & 0xFF
            
            pgn = (pdu_format << 8) | pdu_specific
            
            data_bytes = frame_data[4:12]  # 8 data bytes
            
            return {
                "timestamp": time.time(),
                "priority": priority,
                "data_page": data_page,
                "pdu_format": f"0x{pdu_format:02X}",
                "pdu_specific": f"0x{pdu_specific:02X}",
                "source_address": f"0x{source_address:02X}",
                "pgn": f"0x{pgn:04X}",
                "data_bytes": data_bytes
            }
            
        except Exception as e:
            raise ValueError(f"Error parsing CAN frame: {str(e)}")

    def decode_message(self, message_data):
 
        try:
            # calculate PGN decimal value
            pdu_f = int(message_data["pdu_format"].replace("0x", ""), 16)
            pdu_s = int(message_data["pdu_specific"].replace("0x", ""), 16)
            pgn_decimal = (pdu_f << 8) | pdu_s

            # decode PGN data
            pgn_data = self.decode_pgn_data(pgn_decimal, message_data["data_bytes"])
            if pgn_data:
                message_data.update(pgn_data)
                self.stats["decoded_messages"] += 1
            else:
                self.stats["unknown_pgns"] += 1
                self.unknown_pgn_list.add(pgn_decimal)

            return message_data

        except Exception as e:
            self.stats["error_messages"] += 1
            return {
                "error": str(e),
                "raw_data": message_data
            }

    def listen_for_data(self, host='0.0.0.0', port=8080):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"Listening on {host}:{port}")
            
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    buffer = bytearray()
                    
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                            
                        buffer.extend(data)
                        
                        while len(buffer) >= 12:
                            frame = buffer[:12]
                            buffer = buffer[12:]
                            
                            try:
                                parsed_frame = self.parse_can_frame(frame)
                                decoded_data = self.decode_message(parsed_frame)
                                self.stats["total_messages"] += 1
                                
                                with open('raw_data.log', 'ab') as f:
                                    f.write(frame)
                                
                                with open('decoded_data.json', 'a') as f:
                                    json.dump(decoded_data, f)
                                    f.write('\n')
                                
                                print(f"\nDecoded Frame:")
                                print(f"PGN: {decoded_data.get('pgn')}")
                                if 'pgn_name' in decoded_data:
                                    print(f"PGN Name: {decoded_data['pgn_name']}")
                                    if decoded_data.get('spns'):
                                        print("Decoded Values:")
                                        for spn_name, spn_data in decoded_data['spns'].items():
                                            if 'error' in spn_data:
                                                print(f"  {spn_name}: Error - {spn_data['error']}")
                                            else:
                                                print(f"  {spn_name}: {spn_data['value']} (raw: {spn_data['raw_value']})")
                                
                            except Exception as e:
                                logging.error(f"Error processing frame: {str(e)}")
                                print(f"Error processing frame: {str(e)}")

def main():
    decoder = CANDecoder()
    try:
        decoder.listen_for_data()
    except Exception as e:
        logging.error(f"Fatal error: {str(e)}")
        raise

if __name__ == "__main__":
    main()