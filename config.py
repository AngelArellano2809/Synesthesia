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
    
    TEXT_RENDERING = {
        'DEFAULT_FONT': 'assets/fonts/Montserrat/Montserrat-VariableFont_wght.ttf', 
        'BOTTOM_MARGIN': 30,
        'PADDING': 15,
        'BACKGROUND_COLOR': (0, 0, 0, 128),  # Negro semitransparente
        'TEXT_COLOR': (255, 255, 255, 255)    # Blanco sólido
    }
