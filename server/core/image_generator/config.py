class ImageGenConfig:
    # Configuraciones base
    DEFAULT_STEPS = 30
    DEFAULT_NEGATIVE_PROMPT = (        
        "worst quality, low quality, normal quality, text, signature, watermark, username, artist name, label, title, "
        "nsfw, nude, nudity, bare skin, erotic, sexual, sensual, sexy, lingerie, cleavage, breasts, nipples, genital, "
        "woman, women, female, girl, human figure, human body, person, portrait, face, facial features, head, torso, "
        "body, arms, legs, hands, fingers, limbs, silhouette, figure, model, actress, feminine form, curves, "
        "selfie, photo of person, realistic human, anatomy, skin texture, hair, eyes, nose, mouth, lips, "
        "multiple views, framing, frame, border, "
        "mecha, robot, furry, anthropomorphic, animal ears, tails, paws, "
        "comic, cartoon, graphic novel, anime, manga, sketch, draft, drawing, "
        "letters, alphabet, words, sentences, paragraphs, caption, subtitle, "
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
        },
        "ethereal_dream": {
            "base_style": "soft surrealism, translucent light forms, pastel haze",
            "composition": "floating composition, dreamlike depth",
            "quality_boost": "glow diffusion, cinematic softness"
        },
        "cosmic_ride": {
            "base_style": "retro-futurist cosmic art, star trails, galactic dust",
            "composition": "radial motion, space horizon perspective",
            "quality_boost": "neon glow, volumetric lighting"
        },
        "neo_tribal": {
            "base_style": "modern tribal patterns, symbolic abstraction, bold contrasts",
            "composition": "symmetrical rhythm, mask-like motifs",
            "quality_boost": "high detail texture, ink precision"
        },
        "candy_pop": {
            "base_style": "colorful pop surrealism, glossy plastic textures, bubblegum tones",
            "composition": "dynamic balance, playful repetition",
            "quality_boost": "hyper-saturation, smooth shading"
        },
        "pop_art": {
            "base_style": "pop art collage, halftone textures, comic contrast",
            "composition": "modular layout, graphic balance",
            "quality_boost": "vector clarity, high contrast edges"
        },
        "vaporwave": {
            "base_style": "retro vaporwave aesthetic, nostalgic synth tones, 80s digital decay",
            "composition": "symmetrical perspective, gradient sunset hues",
            "quality_boost": "CRT grain, neon bloom"
        },
        "virtual_angel": {
            "base_style": "digital ethereal being, chrome wings, holographic aura",
            "composition": "floating symmetry, luminous halo",
            "quality_boost": "ray tracing, iridescent detail"
        },
        "metaphysical_void": {
            "base_style": "conceptual abstraction, infinite negative space, surreal geometry",
            "composition": "central focus with vanishing depth",
            "quality_boost": "ultra clarity, cinematic contrast"
        },
        "glass_dreamscape": {
            "base_style": "abstract glass forms, refracted light, crystalline fluidity",
            "composition": "soft reflections, curved transparency",
            "quality_boost": "caustics render, photoreal refraction"
        },
        "chromatic_minimalism": {
            "base_style": "color-field minimalism, smooth gradients, digital purity",
            "composition": "balanced geometry, pure tonal harmony",
            "quality_boost": "8k clarity, noise-free render"
        },
        "data_bloom": {
            "base_style": "generative art, data-driven floral patterns, algorithmic growth",
            "composition": "organic symmetry, fractal expansion",
            "quality_boost": "fine detail, procedural sharpness"
        },
        "dream_plastic": {
            "base_style": "post-digital surrealism, glossy synthetic textures, pastel vapor tones",
            "composition": "floating organic forms, layered translucence",
            "quality_boost": "soft reflections, smooth HDR finish"
        },
        "neon_void": {
            "base_style": "dark minimal cyber aesthetic, neon traces, reflective surfaces",
            "composition": "isolated light geometry, void backdrop",
            "quality_boost": "ray-traced glow, sharp reflections"
        }
    }
    
    @classmethod
    def get_preset(cls, preset_name):
        return cls.STYLE_PRESETS.get(preset_name, cls.STYLE_PRESETS["minimal_geometric"])