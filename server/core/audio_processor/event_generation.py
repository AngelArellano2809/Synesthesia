import numpy as np
from typing import List, Dict, Any
from ..config import Config
from .beat_detection import AudioAnalyzer
import librosa

class EventGenerator:
    def __init__(self):
        self.cfg = Config.AUDIO
        self.analyzer = AudioAnalyzer()
    
    def generate_events(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Procesa el audio y genera eventos estructurados
        
        Returns:
            Lista de diccionarios con:
            - 'start_time': tiempo de inicio (segundos)
            - 'end_time': tiempo de fin (segundos)
            - 'type': tipo de evento ('beat' u 'onset')
        """
        y, tempo = self.analyzer.load_audio(audio_path)
        event_times = self.analyzer.detect_events(y)
        
        # Clasificar eventos y calcular duraciones
        events = self._structure_events(event_times, y)
        
        return {
            'metadata': {
                'tempo': tempo,
                'total_events': len(events),
                'duration': len(y)/self.cfg['sr']
            },
            'events': events
        }
    
    def _structure_events(self, event_times: List[float], y: np.ndarray) -> List[Dict[str, Any]]:
        """Organiza los tiempos en eventos estructurados"""
        sr = self.cfg['sr']
        events = []
        
        # Asegurar que el último evento llegue hasta el final del audio
        event_times.append(len(y)/sr)
        
        for i in range(len(event_times)-1):
            start = event_times[i]
            end = event_times[i+1]
            
            # Determinar tipo de evento basado en características del segmento
            segment = y[int(start*sr):int(end*sr)]
            event_type = self._classify_event(segment, sr)
            
            events.append({
                'start_time': start,
                'end_time': end,
                'duration': end - start,
                'type': event_type,
                'intensity': self._calculate_intensity(segment)
            })
        
        return events
    
    def _classify_event(self, segment: np.ndarray, sr: int) -> str:
        """Clasifica el evento como 'beat' u 'onset' basado en características"""
        rms = np.sqrt(np.mean(segment**2))
        spectral_centroid = librosa.feature.spectral_centroid(y=segment, sr=sr)[0, 0]
        
        return 'onset' if spectral_centroid > 2000 and rms > 0.05 else 'beat'
    
    def _calculate_intensity(self, segment: np.ndarray) -> float:
        """Calcula la intensidad relativa del evento (0-1)"""
        return float(np.clip(np.sqrt(np.mean(segment**2)) * 2, 0, 1))