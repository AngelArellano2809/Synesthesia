class ImageGenConfig:
    # Configuraciones base
    DEFAULT_STEPS = 30
    DEFAULT_NEGATIVE_PROMPT = (        
        "worst quality, low quality, normal quality, text, signature, watermark, nude, nsfw, mecha, robot, "
        "username, artist name, trademark, label, title, multiple views, "
        "comic, cartoon, graphic novel, anime, manga, furry, anthropomorphic, "
        "animal ears, tail, paws, sketch, drawing, draft, frame, border, human, "
        "person, face, body, hands, fingers, limbs, portrait, selfie, "
        "letters, alphabet, words, sentences, paragraphs, "
        "ugly, disfigured, deformed, blurry, noisy"
    )
    
    # Presets de estilo
    STYLE_PRESETS = {
        "minimal_geometric": {
            "base_style": "minimalist vector art, geometric patterns",
            "composition": "smooth gradients",
            "quality_boost": "sharp focus, high detail"
        },
        "organic_abstract": {
            "base_style": "watercolor painting, organic flowing shapes",
            "composition": "paper texture visible",
            "quality_boost": "textured brushstrokes"
        },
        "digital_futuristic": {
            "base_style": "cyberpunk digital art, glowing circuit patterns",
            "composition": "metallic sheen",
            "quality_boost": "ray tracing, unreal engine"
        },
        "vibrant_abstract": {
            "base_style": "vibrant abstract expressionism, bold brushstrokes, textured surface",
            "composition": "dynamic asymmetric composition, high contrast",
            "quality_boost": "high detail, sharp focus, gallery quality"
        },
        "digital_minimalism": {
            "base_style": "minimalist digital art, flat design, vector illustration",
            "composition": "clean geometric composition, ample negative space",
            "quality_boost": "4k resolution, sharp edges"
        },
        "liquid_motion": {
            "base_style": "fluid dynamics, liquid motion, organic forms",
            "composition": "flowing composition with directional movement",
            "quality_boost": "photorealistic render, subsurface scattering"
        }
    }
    
    @classmethod
    def get_preset(cls, preset_name):
        return cls.STYLE_PRESETS.get(preset_name, cls.STYLE_PRESETS["minimal_geometric"])