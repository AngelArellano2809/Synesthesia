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
            prompt_parts.append("rhythmic geometric, pulsating forms")
        elif event_data["type"] == "onset":
            prompt_parts.append("dynamic transition, energy burst")
            
        # Textura y calidad
        prompt_parts.append(self.style_preset["composition"])
        prompt_parts.append(self.style_preset["quality_boost"])
        
        # Intensidad del evento
        intensity = event_data.get("intensity", 0.5)
        if intensity > 0.7:
            prompt_parts.append("high contrast, dramatic lighting")
        elif intensity < 0.3:
            prompt_parts.append("soft focus, minimalistic") #
        
        # Paleta de colores
        if self.color_palette and self.color_palette.get("prompt_description"):
            prompt_parts.append(self.color_palette["prompt_description"])

        # Añadir énfasis a elementos clave
        if event_data.get("lyric"):
            lyric = event_data["lyric"][:30]
            prompt_parts.append(f"interpretation of phrase: '{lyric}'")

        # Usar ponderación para elementos importantes
        prompt = ", ".join(prompt_parts)
        # prompt += ", abstract"

        # print(prompt)        
        return prompt