class Config:
    AUDIO = {
        'sr': 22050,  #librosa
        'WHISPER_SR': 16000,  # Sample rate óptimo para Whisper
        'hop_length': 512, 
        'min_event_interval': 0.5,
        'onset_params': {
            'pre_max': 20,
            'post_max': 20,
            'pre_avg': 100,
            'post_avg': 100,
            'delta': 0.2,
            'wait': 10
        }
    }
    RENDERING = {
        'fps': 24,
        'transition_duration': 0.5  # Duración de transiciones entre imágenes
    }
    STYLE = {
        'color_scheme': ['dominant', 'complementary', 'random'],
        'shapes': ['circles', 'squares', 'triangles'],
        'transitions': ['fade', 'slide', 'zoom']
    }
    GENIUS = {
        'ENABLED': True,
        'ACCESS_TOKEN': '9RXMs5KrjbQrRFlfNzKspC3EVgeBaxJZN3YkGcPCNd-R367PoLABwQsmK_N_SABT',
        'TIMEOUT': 10  # segundos
    }
    WHISPER = {
        'MODEL_SIZE': 'small', 
        'DEVICE': 'cuda', 
        'LANGUAGE': None 
    }