class Config:
    AUDIO = {
        'sr': 22050,  
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
    
    LYRIC = {
        'max_length': 50,  # Máximo de caracteres por prompt
        'context_window': 2.0  # Segundos antes/después para contexto lírico
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