import csv
import json
from datetime import datetime
from pgn_definitions import pgn_definitions
from alert_system import AlertSystem
from anomaly_detection import AnomalyDetectionSystem

class J1939Parser:
    def __init__(self):
        self.pgn_defs = pgn_definitions.pgn_defs
        self.serial_number = 1
        self.messages = []
        self.alert_system = AlertSystem()
        self.anomaly_system = AnomalyDetectionSystem()

    def decode_spn(self, data_bytes, spn_info):
        try:
            raw_value = None
            
            if "start_bit" in spn_info:
                raw_value = self.extract_bits(data_bytes, spn_info["start_bit"], spn_info["length"])
            elif "start_byte" in spn_info:
                start_idx = spn_info["start_byte"] - 1
                length = spn_info["length"]
                
                raw_value = 0
                for i in range(length):
                    if start_idx + i < len(data_bytes):
                        raw_value |= data_bytes[start_idx + i] << (8 * i)
            
            if raw_value is None:
                return None
            
            resolution = spn_info.get("resolution", 1)
            offset = spn_info.get("offset", 0)
            value = raw_value * resolution + offset
            
            return value
            
        except Exception as e:
            print(f"Error decoding SPN: {e}")
            return None

    def extract_bits(self, data_bytes, start_bit, length):
        try:
            start_bit = start_bit - 1
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

    def add_message_entry(self, msg_id, serial_number, timestamp, pgn_hex, pgn_name, spn_name, spn_value):
        # Check for alerts
        alert_info = self.alert_system.check_alert(spn_name, spn_value)
        
        # Check for anomalies
        anomaly_info = self.anomaly_system.check_anomaly(spn_name, spn_value)

        message = {
            "ID": msg_id,
            "serial_number": serial_number,
            "timestamp": timestamp,
            "pgn_hex": pgn_hex,
            "pgn_definition": pgn_name,
            "spn_definition": spn_name,
            "spn_value": spn_value,
            "alert": alert_info["alert"] if alert_info else None,
            "alert_color": alert_info["color"] if alert_info else None,
            "has_buzzer": alert_info["has_buzzer"] if alert_info else False,
            "anomaly": {
                "detected": anomaly_info["is_anomaly"] if anomaly_info else False,
                "confidence": anomaly_info["confidence"] if anomaly_info else None,
                "methods": anomaly_info["detection_methods"] if anomaly_info else [],
                "severity": anomaly_info["severity"] if anomaly_info else None,
                "trend": anomaly_info["trend"] if anomaly_info else None,
                "statistics": anomaly_info["statistics"] if anomaly_info else None
            }
        }
        self.messages.append(message)

    def create_formatted_output(self, input_file, output_file):
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
                    
                    pdu_f = int(row["PDU-F"].replace("0x", ""), 16)
                    pdu_s = int(row["PDU-S"].replace("0x", ""), 16)
                    pgn_decimal = (pdu_f << 8) | pdu_s
                    pgn_hex = f"0x{pgn_decimal:04X}"
                    
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
                    
                    if not pgn_info["spns"]:
                        self.add_message_entry(
                            msg_id, self.serial_number, formatted_time,
                            pgn_hex, pgn_name, "No SPNs defined", "-"
                        )
                        self.serial_number += 1
                    else:
                        for spn_id, spn_info in pgn_info["spns"].items():
                            spn_value = self.decode_spn(data_bytes, spn_info)
                            if spn_value is not None:
                                self.add_message_entry(
                                    msg_id, self.serial_number, formatted_time,
                                    pgn_hex, pgn_name, spn_info['name'], f"{spn_value:.2f}"
                                )
                                self.serial_number += 1
                                
                except Exception as e:
                    print(f"Error processing message: {e}")
                    continue

        # Write all messages to JSON file
        with open(output_file, 'w') as outfile:
            json.dump({"messages": self.messages}, outfile, indent=2)

def main():
    parser = J1939Parser()
    parser.create_formatted_output("BD-155_13869_RawCANLog.csv", "j1939_decoded_messages.json")

if __name__ == "__main__":
    main()