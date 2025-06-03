class ImageGenConfig:
    # Configuraciones base
    DEFAULT_MODEL = "jru_model_full"
    DEFAULT_STEPS = 30
    DEFAULT_NEGATIVE_PROMPT = (
        "worst aesthetic, good quality, normal quality, low quality, bad quality, "
        "worst quality, mid, early, old, adversarial noise, ai-generated, ai-assisted, "
        "stable diffusion, lowres, low res, monochrome,"
    )
    
    # Presets de estilo
    STYLE_PRESETS = {
        "minimal_geometric": {
            "base_style": "minimalist vector art, geometric patterns",
            "texture": "smooth gradients",
            "abstraction": 0.8,
            "quality_boost": "sharp focus, high detail"
        },
        "organic_abstract": {
            "base_style": "watercolor painting, organic flowing shapes",
            "texture": "paper texture visible",
            "abstraction": 0.6,
            "quality_boost": "textured brushstrokes"
        },
        "digital_futuristic": {
            "base_style": "cyberpunk digital art, glowing circuit patterns",
            "texture": "metallic sheen",
            "abstraction": 0.9,
            "quality_boost": "ray tracing, unreal engine"
        }
    }
    
    @classmethod
    def get_preset(cls, preset_name):
        return cls.STYLE_PRESETS.get(preset_name, cls.STYLE_PRESETS["minimal_geometric"])