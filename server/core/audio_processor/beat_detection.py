import librosa
from librosa.feature.rhythm import tempo as estimate_tempo
import numpy as np
from typing import List, Tuple
from ..config import Config

class AudioAnalyzer:
    def __init__(self):
        self.cfg = Config.AUDIO
    
    def load_audio(self, file_path: str) -> Tuple[np.ndarray, float]:
        # Carga el audio 
        try:
            y, _ = librosa.load(file_path, sr=self.cfg['sr'], mono=True)
            tempo = self._validate_tempo(estimate_tempo(y=y, sr=self.cfg['sr'])[0])
            return y, tempo
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            raise
    
    def detect_events(self, y: np.ndarray) -> List[float]:
        # Detecta eventos de beat
        beat_times = self._detect_beats(y)
        print('Beats: ',len(beat_times))
        # Detecta eventos de onset
        onset_times = self._detect_onsets(y)
        print('Onset: ',len(onset_times))
        # Detecta donde coinciden ambos eventos
        events = self._combine_events(beat_times, onset_times)
        print('Eventos: ',len(events))
        return events
    
    def _detect_beats(self, y: np.ndarray) -> np.ndarray:
        _, beats = librosa.beat.beat_track(y=y, sr=self.cfg['sr'], units='time')
        return beats
    
    def _detect_onsets(self, y: np.ndarray) -> np.ndarray:
        results = []

        sensitivity_levels = [
            {'pre_max': 20, 'post_max': 20, 'pre_avg': 100, 'post_avg': 100, 'delta': 0.2, 'wait': 10},
            {'pre_max': 30, 'post_max': 30, 'pre_avg': 100, 'post_avg': 100,'delta': 0.1, 'wait': 5},
            {'pre_max': 40, 'post_max': 40, 'pre_avg': 100, 'post_avg': 100,'delta': 0.08, 'wait': 4},
            {'pre_max': 50, 'post_max': 50, 'pre_avg': 100, 'post_avg': 100,'delta': 0.05, 'wait': 3}
        ]

        for params in sensitivity_levels:
            onset_times = librosa.onset.onset_detect(
                y=y, sr=self.cfg['sr'], units='time', **params)
            results.append(onset_times)

        onset = max(results, key=len)
        
        return onset

    
    def _combine_events(self, beats: np.ndarray, onsets: np.ndarray) -> List[float]:
        """Combina beats y onsets inteligentemente"""
        # 1. Combinar todos los eventos
        all_events = np.concatenate([beats, onsets])
        
        # 2. Ordenar y eliminar duplicados
        sorted_events = np.sort(np.unique(all_events))
        
        # 3. Filtrar eventos demasiado cercanos
        filtered = []
        prev_event = -np.inf  # Inicializar con un valor muy pequeño
        
        for event in sorted_events:
            if event - prev_event >= self.cfg['min_event_interval']:
                filtered.append(event)
                prev_event = event
        
        # 4. Asegurar evento inicial
        if not filtered or filtered[0] > 0.1:
            filtered.insert(0, 0.0)
        
        return filtered
    
    def _validate_tempo(self, tempo: float) -> float:
        return tempo if 40 <= tempo <= 250 else 120.0