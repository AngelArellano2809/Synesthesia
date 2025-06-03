class PromptBuilder:
    def __init__(self, style_preset, color_palette=None):
        self.style_preset = style_preset
        self.color_palette = color_palette
    
    def build_prompt(self, event_data):
        """Construye un prompt personalizado basado en el evento y configuración"""
        # Base del estilo
        prompt_parts = [self.style_preset["base_style"]]
        
        # Elemento basado en el tipo de evento
        if event_data["type"] == "beat":
            prompt_parts.append("rhythmic geometric composition")
        elif event_data["type"] == "onset":
            prompt_parts.append("dynamic transition effect")
        elif event_data["type"] == "lyric":
            prompt_parts.append("text-focused composition")
            
        # Textura y calidad
        prompt_parts.append(self.style_preset["texture"])
        prompt_parts.append(self.style_preset["quality_boost"])
        
        # Intensidad del evento
        intensity = event_data.get("intensity", 0.5)
        if intensity > 0.7:
            prompt_parts.append("high contrast, dramatic lighting")
        elif intensity < 0.3:
            prompt_parts.append("soft focus, muted tones")
        
        # Paleta de colores si está disponible
        if self.color_palette:
            color_part = f"color palette: {', '.join(self.color_palette['hex_colors'][:3])}"
            prompt_parts.append(color_part)
        
        # Texto de la letra si existe
        if event_data.get("lyric"):
            # Limitar la longitud del texto para no saturar
            lyric = event_data["lyric"][:50].replace('"', '').replace("'", "")
            prompt_parts.append(f"featuring text: '{lyric}'")
        
        return ", ".join(prompt_parts)