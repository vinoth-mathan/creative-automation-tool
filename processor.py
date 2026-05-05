from PIL import Image
import os
import io

def process_creative(bg_bytes, panel_path, logo_path, target_size):
    bg = Image.open(io.BytesIO(bg_bytes)).convert("RGBA")
    
    target_ratio = target_size[0] / target_size[1]
    bg_ratio = bg.width / bg.height
    
    if bg_ratio > target_ratio:
        new_height = target_size[1]
        new_width = int(new_height * bg_ratio)
    else:
        new_width = target_size[0]
        new_height = int(new_width / bg_ratio)
        
    bg = bg.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    left = (bg.width - target_size[0]) / 2
    top = (bg.height - target_size[1]) / 2
    right = (bg.width + target_size[0]) / 2
    bottom = (bg.height + target_size[1]) / 2
    bg = bg.crop((left, top, right, bottom))
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    panel_full_path = os.path.join(base_dir, panel_path)
    logo_full_path = os.path.join(base_dir, logo_path) if logo_path else None

    panel = Image.open(panel_full_path).convert("RGBA")
    # Scale panel to fit width of target
    panel_ratio = panel.height / panel.width
    new_panel_width = target_size[0]
    new_panel_height = int(new_panel_width * panel_ratio)
    panel = panel.resize((new_panel_width, new_panel_height), Image.Resampling.LANCZOS)
    
    bg.alpha_composite(panel, (0, target_size[1] - new_panel_height))
    
    if logo_full_path and os.path.exists(logo_full_path):
        logo = Image.open(logo_full_path).convert("RGBA")
        # Scale logo to be roughly 15% of width
        logo_w = int(target_size[0] * 0.15)
        logo_h = int(logo_w * (logo.height / logo.width))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        
        margin = int(target_size[0] * 0.05)
        bg.alpha_composite(logo, (target_size[0] - logo_w - margin, margin))
    
    out_io = io.BytesIO()
    bg.convert("RGB").save(out_io, "JPEG", quality=95)
    out_io.seek(0)
    return out_io.read()
