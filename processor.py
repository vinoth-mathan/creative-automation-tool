import io
import os
from PIL import Image


def process_creative(
    bg_bytes,
    panel_path,
    logo_path,
    target_size,
    additional_asset_path=None,
    additional_asset_bytes=None,
):
    bg = Image.open(io.BytesIO(bg_bytes)).convert('RGBA')

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
    additional_full_path = os.path.join(base_dir, additional_asset_path) if additional_asset_path else None

    panel = Image.open(panel_full_path).convert('RGBA')
    panel_ratio = panel.height / panel.width
    new_panel_width = target_size[0]
    new_panel_height = int(new_panel_width * panel_ratio)
    panel = panel.resize((new_panel_width, new_panel_height), Image.Resampling.LANCZOS)
    bg.alpha_composite(panel, (0, target_size[1] - new_panel_height))

    if logo_full_path and os.path.exists(logo_full_path):
        logo = Image.open(logo_full_path).convert('RGBA')
        logo_w = int(target_size[0] * 0.15)
        logo_h = int(logo_w * (logo.height / logo.width))
        logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

        margin = int(target_size[0] * 0.05)
        bg.alpha_composite(logo, (target_size[0] - logo_w - margin, margin))

    if additional_asset_bytes or (additional_full_path and os.path.exists(additional_full_path)):
        if additional_asset_bytes:
            extra = Image.open(io.BytesIO(additional_asset_bytes)).convert('RGBA')
        else:
            extra = Image.open(additional_full_path).convert('RGBA')

        extra_w = int(target_size[0] * 0.18)
        extra_h = int(extra_w * (extra.height / extra.width))
        extra = extra.resize((extra_w, extra_h), Image.Resampling.LANCZOS)

        margin = int(target_size[0] * 0.05)
        panel_top = target_size[1] - new_panel_height
        y_top = margin
        y_bottom_safe = panel_top - extra_h - margin

        y = y_top if y_bottom_safe < y_top else y_bottom_safe
        bg.alpha_composite(extra, (margin, y))

    out_io = io.BytesIO()
    bg.convert('RGB').save(out_io, 'JPEG', quality=95)
    out_io.seek(0)
    return out_io.read()
