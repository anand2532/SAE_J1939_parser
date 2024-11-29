import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from scipy import stats

class AnomalyDetectionSystem:
    def __init__(self):
        self.monitored_parameters = {
            "Engine Speed": {
                "window_size": 10,
                "min_data_points": 50,
                "pca_threshold": 2.0,
                "lstm_threshold": 3.0,
                "statistical_threshold": 3.0
            },
            "Engine Oil Pressure": {
                "window_size": 10,
                "min_data_points": 30,
                "pca_threshold": 2.5,
                "lstm_threshold": 3.5,
                "statistical_threshold": 3.0
            },
            "Engine Coolant Temperature": {
                "window_size": 15,
                "min_data_points": 40,
                "pca_threshold": 2.0,
                "lstm_threshold": 3.0,
                "statistical_threshold": 2.5
            },
            "Hydraulic Temperature": {
                "window_size": 15,
                "min_data_points": 40,
                "pca_threshold": 2.0,
                "lstm_threshold": 3.0,
                "statistical_threshold": 2.5
            }
        }
        
        # Initialize components
        self.historical_data = {}
        self.scalers = {}
        self.pca_models = {}
        self.lstm_models = {}
        
        # Initialize models for each parameter
        for param in self.monitored_parameters:
            self.historical_data[param] = []
            self.scalers[param] = StandardScaler()
            self.pca_models[param] = PCA(n_components=2)
            
            # Initialize LSTM model
            model = Sequential([
                LSTM(50, activation='relu', 
                     input_shape=(self.monitored_parameters[param]["window_size"], 1), 
                     return_sequences=True),
                LSTM(30, activation='relu'),
                Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            self.lstm_models[param] = model
    
    def check_anomaly(self, spn_name, value):
        if spn_name == "No SPNs defined" or value == "-":
            return None
            
        param_config = None
        for param_name, config in self.monitored_parameters.items():
            if param_name == spn_name:
                param_config = config
                break
                
        if param_config is None:
            return None
            
        try:
            value = float(str(value).split()[0])
            self.historical_data[spn_name].append(value)
            
            if len(self.historical_data[spn_name]) < param_config["min_data_points"]:
                return None
                
            recent_data = np.array(self.historical_data[spn_name][-param_config["min_data_points"]:])
            scaled_data = self.scalers[spn_name].fit_transform(recent_data.reshape(-1, 1))
            
            # Run all detection methods
            pca_score = self._pca_detection(spn_name, scaled_data, param_config["pca_threshold"])
            lstm_score = self._lstm_detection(spn_name, scaled_data, param_config)
            stat_score = self._statistical_detection(spn_name, recent_data, param_config["statistical_threshold"])
            
            # Combine results
            anomaly_scores = []
            detection_methods = []
            
            if pca_score:
                anomaly_scores.append(pca_score["confidence"])
                if pca_score["is_anomaly"]:
                    detection_methods.append("PCA")
                    
            if lstm_score:
                anomaly_scores.append(lstm_score["confidence"])
                if lstm_score["is_anomaly"]:
                    detection_methods.append("LSTM")
                    
            if stat_score:
                anomaly_scores.append(stat_score["confidence"])
                if stat_score["is_anomaly"]:
                    detection_methods.append("Statistical")
            
            if not anomaly_scores:
                return None
            
            # Calculate trend
            trend = "stable"
            if len(self.historical_data[spn_name]) > 1:
                recent_values = self.historical_data[spn_name][-5:]
                if all(y > x for x, y in zip(recent_values, recent_values[1:])):
                    trend = "increasing"
                elif all(y < x for x, y in zip(recent_values, recent_values[1:])):
                    trend = "decreasing"
            
            return {
                "is_anomaly": len(detection_methods) > 0,
                "confidence": float(max(anomaly_scores)) if anomaly_scores else 0.0,
                "detection_methods": detection_methods,
                "severity": "High" if len(detection_methods) >= 2 else "Medium" 
                          if len(detection_methods) == 1 else "Low",
                "trend": trend,
                "statistics": {
                    "current_value": float(value),
                    "mean": float(np.mean(recent_data)),
                    "std": float(np.std(recent_data)),
                    "min": float(np.min(recent_data)),
                    "max": float(np.max(recent_data))
                }
            }
            
        except Exception as e:
            print(f"Error in anomaly detection for {spn_name}: {e}")
            return None
    
    def _pca_detection(self, spn_name, scaled_data, threshold):
        try:
            pca_result = self.pca_models[spn_name].fit_transform(scaled_data)
            reconstruction = self.pca_models[spn_name].inverse_transform(pca_result)
            error = np.mean(np.square(scaled_data - reconstruction))
            
            is_anomaly = error > threshold
            confidence = float(error / threshold if error > threshold else error / (threshold * 2))
            
            return {"is_anomaly": is_anomaly, "confidence": confidence}
        except:
            return None
    
    def _lstm_detection(self, spn_name, scaled_data, config):
        try:
            # Prepare sequences
            sequences = []
            for i in range(len(scaled_data) - config["window_size"]):
                sequences.append(scaled_data[i:(i + config["window_size"])])
            
            sequences = np.array(sequences)
            if len(sequences) == 0:
                return None
            
            # Train model and predict
            self.lstm_models[spn_name].fit(sequences, scaled_data[config["window_size"]:], 
                                         epochs=1, verbose=0)
            last_sequence = scaled_data[-config["window_size"]:].reshape(1, config["window_size"], 1)
            prediction = self.lstm_models[spn_name].predict(last_sequence, verbose=0)
            
            # Calculate error
            actual = scaled_data[-1]
            error = abs(prediction - actual)[0][0]
            
            is_anomaly = error > config["lstm_threshold"]
            confidence = float(error / config["lstm_threshold"] if error > config["lstm_threshold"] 
                            else error / (config["lstm_threshold"] * 2))
            
            return {"is_anomaly": is_anomaly, "confidence": confidence}
        except:
            return None
    
    def _statistical_detection(self, spn_name, data, threshold):
        try:
            z_score = abs(stats.zscore(data)[-1])
            is_anomaly = z_score > threshold
            confidence = float(z_score / threshold if z_score > threshold 
                            else z_score / (threshold * 2))
            
            return {"is_anomaly": is_anomaly, "confidence": confidence}
        except:
            return None