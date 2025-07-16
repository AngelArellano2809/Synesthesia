class Config:
    AUDIO = {
        'sr': 22050, 
        'WHISPER_SR': 16000, 
        'hop_length': 512, 
        'min_event_interval': 0.5,
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
    
    VIDEO = {
        'FPS': 24,  # Cuadros por segundo
        'RESOLUTION': (1920, 1080),  # 1080p
        'DEFAULT_OUTPUT': 'output_video.mp4'
    }