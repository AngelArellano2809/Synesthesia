def apply_style(frame, palette):
    primary, secondary, _ = palette
    # Usar primary[1] (RGB) para fondos
    # Usar secondary[1] para elementos
    # Usar get_contrast_color() para texto