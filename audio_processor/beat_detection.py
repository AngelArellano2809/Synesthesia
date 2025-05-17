 
import librosa
from librosa.feature.rhythm import tempo as estimate_tempo
import numpy as np
from typing import List, Tuple
from config import Config

class AudioAnalyzer:
    def __init__(self):
        self.cfg = Config.AUDIO
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, float]:
        """Carga el audio con manejo de errores"""
        try:
            y, _ = librosa.load(file_path, sr=self.cfg['sr'], mono=True)
            tempo = self._validate_tempo(estimate_tempo(y=y, sr=self.cfg['sr'])[0])
            return y, tempo
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            raise
    
    def detect_events(self, y: np.ndarray) -> List[float]:
        """Detecta puntos de cambio importantes"""
        return self._combine_events(
            self._detect_beats(y),
            self._detect_onsets(y)
        )
    
    def _detect_beats(self, y: np.ndarray) -> np.ndarray:
        _, beats = librosa.beat.beat_track(y=y, sr=self.cfg['sr'], units='time')
        return beats
    
    def _detect_onsets(self, y: np.ndarray) -> np.ndarray:
        return librosa.onset.onset_detect(
            y=y, sr=self.cfg['sr'], units='time', **self.cfg['onset_params'])
    
    def _combine_events(self, beats: np.ndarray, onsets: np.ndarray) -> List[float]:
        """Combina beats y onsets asegurando evento inicial"""
        # Combinar y ordenar
        events = np.unique(np.concatenate([beats, onsets]))
        
        # Filtrado por intervalo mínimo
        mask = np.diff(events, prepend=-np.inf) >= self.cfg['min_event_interval']
        filtered = events[mask].tolist()
        
        # Garantizar evento en 0.0 (para inicio inmediato del video)
        if not filtered or filtered[0] > 0.1:  # Margen de 100ms
            filtered.insert(0, 0.0)
        
        return filtered
    
    def _validate_tempo(self, tempo: float) -> float:
        return tempo if 40 <= tempo <= 250 else 120.0
    