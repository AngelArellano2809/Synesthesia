import torch
from diffusers import StableDiffusionXLPipeline
from .config import ImageGenConfig
from .prompt_builder import PromptBuilder
import os
from tqdm import tqdm

class ImageGenerator:
    def __init__(self, model_path=None, device="cuda", torch_dtype=torch.float16):
        self.model_path = model_path or ImageGenConfig.DEFAULT_MODEL
        self.device = device
        self.torch_dtype = torch_dtype
        self.pipe = self._load_model()
    
    def _load_model(self):
        """Carga el modelo de Stable Diffusion"""
        print(f"Loading model from: {self.model_path}")
        pipe = StableDiffusionXLPipeline.from_pretrained(
            self.model_path,
            torch_dtype=self.torch_dtype,
            use_safetensors=True
        ).to(self.device)
        
        # Optimizaciones para ahorrar memoria
        pipe.enable_model_cpu_offload()
        pipe.enable_vae_slicing()
        
        return pipe
    
    def generate_images(self, events, output_dir, style_preset="minimal_geometric", color_palette=None):
        """Genera imágenes para todos los eventos"""
        os.makedirs(output_dir, exist_ok=True)
        preset = ImageGenConfig.get_preset(style_preset)
        prompt_builder = PromptBuilder(preset, color_palette)
        
        # Generar semilla base basada en el primer evento
        base_seed = hash(events[0]["start_time"]) % 1000000


        max_images = 500                                                                 #50 primeros eventos
        print(f"Generando imágenes para {len(events)} eventos (límite: {max_images})")   
        
        # Contador para imágenes generadas
        generated_count = 0


        
        # print(f"Generating {len(events)} images with style: {style_preset}")
        # for i, event in enumerate(tqdm(events, desc="Generating images")):
        #     # Construir prompt específico para el evento
        #     prompt = prompt_builder.build_prompt(event)
            
        #     # Crear semilla única para este evento
        #     seed = base_seed + i
            
        #     # Generar la imagen
        #     image = self.pipe(
        #         prompt=prompt,
        #         negative_prompt=ImageGenConfig.DEFAULT_NEGATIVE_PROMPT,
        #         num_inference_steps=ImageGenConfig.DEFAULT_STEPS,
        #         generator=torch.Generator(device=self.device).manual_seed(seed)
        #     ).images[0]
            
        #     # Guardar con nombre basado en el tiempo del evento
        #     filename = f"{event['start_time']:.2f}s.png"
        #     image.save(os.path.join(output_dir, filename))
        
        # print(f"Images saved to: {output_dir}")


        
        for i, event in enumerate(tqdm(events, desc="Generando imágenes")):
            # Verificar límite de imágenes
            if max_images is not None and generated_count >= max_images:
                print(f"Se alcanzó el límite de {max_images} imágenes")
                break
                
            # Construir nombre de archivo
            filename = f"{event['start_time']:.2f}s.png"
            filepath = os.path.join(output_dir, filename)
            
            # Saltar si el archivo ya existe
            if os.path.exists(filepath):
                continue
                
            # Construir prompt específico para el evento
            prompt = prompt_builder.build_prompt(event)
            
            # Crear semilla única para este evento
            seed = base_seed + i
            
            # Generar la imagen
            image = self.pipe(
                prompt=prompt,
                negative_prompt=ImageGenConfig.DEFAULT_NEGATIVE_PROMPT,
                num_inference_steps=ImageGenConfig.DEFAULT_STEPS,
                generator=torch.Generator(device=self.device).manual_seed(seed)
            ).images[0]
            
            # Guardar la imagen
            image.save(filepath)
            generated_count += 1
        
        print(f"Imágenes generadas: {generated_count}/{len(events)}")
        print(f"Imágenes guardadas en: {output_dir}")
        return generated_count
