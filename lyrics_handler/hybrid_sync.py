import whisper
import re
import torch
from pydub import AudioSegment
import numpy as np
from config import Config
from typing import List, Dict, Tuple

class HybridLyricsSyncer:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'  # Corregido typo 'cuda'
        self.model = whisper.load_model(
            Config.WHISPER['MODEL_SIZE'],
            device=self.device
        )
    
    def sync_lyrics(self, audio_path: str, lyrics: str) -> List[Dict]:
        """Versión optimizada para GPU con todas las variables definidas"""
        # 1. Extraer frases clave de la letra
        key_phrases = self._extract_key_phrases(lyrics)
        if not key_phrases:
            return []

        # 2. Cargar y preparar audio
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(Config.AUDIO['WHISPER_SR']).set_channels(1)
        audio_array = np.array(audio.get_array_of_samples(), dtype=np.float32) / 32768.0
        duration = len(audio) / 1000  # Duración en segundos

        # 3. Transcribir con Whisper
        result = self.model.transcribe(
            audio_array,
            fp16=(self.device == 'cuda'),  # Usar FP16 solo en GPU
            language=Config.WHISPER['LANGUAGE'],
            word_timings=True
        )

        # 4. Alinear frases con segmentos de palabras
        aligned = self._align_phrases(key_phrases, result['segments'])

        # 5. Generar eventos sincronizados
        return self._generate_events(aligned, duration)

    def _extract_key_phrases(self, lyrics: str) -> List[str]:
        """Extrae las primeras palabras de cada línea significativa"""
        lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
        return [re.split(r'\W+', line)[0] for line in lines if line]
    
    def _align_phrases(self, phrases: List[str], segments: List[Dict]) -> List[Tuple[float, str]]:
        """Encuentra los tiempos de las palabras clave en el audio"""
        aligned = []
        phrase_idx = 0
        
        for segment in segments:
            for word in segment.get('words', []):
                if phrase_idx >= len(phrases):
                    break
                
                current_phrase = phrases[phrase_idx].lower()
                if current_phrase in word['word'].lower():
                    aligned.append((word['start'], phrases[phrase_idx]))
                    phrase_idx += 1
        
        return aligned
    
    def _generate_events(self, aligned_phrases: List[Tuple[float, str]], duration: float) -> List[Dict]:
        """Crea eventos distribuidos uniformemente entre palabras clave"""
        if not aligned_phrases:
            return []
            
        events = []
        
        # Agregar evento inicial si no comienza en 0
        if aligned_phrases[0][0] > 0.5:  # Margen de 500ms
            events.append({'time': 0.0, 'text': '♪'})

        # Generar eventos para cada frase alineada
        for i in range(len(aligned_phrases)):
            start_time, phrase = aligned_phrases[i]
            end_time = aligned_phrases[i+1][0] if i < len(aligned_phrases)-1 else duration
            
            # Evento principal con la frase
            events.append({'time': start_time, 'text': phrase})
            
            # Eventos intermedios (cada ~2.5 segundos)
            segment_duration = end_time - start_time
            num_intermediate = int(segment_duration // 2.5)
            
            for j in range(1, num_intermediate + 1):
                events.append({
                    'time': start_time + (j * segment_duration / (num_intermediate + 1)),
                    'text': '♪'
                })
        
        return sorted(events, key=lambda x: x['time'])