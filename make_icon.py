"""
Icon uretici: Pillow ile modern, mavi gradient arka planli, beyaz "R->R" metinli icon.
Coklu cozunurlukluk .ico dosyasi olusturur (Windows exe icin).
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os


def make_base(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Yuvarlak kenarli arka plan (mavi->mor gradient)
    radius = int(size * 0.22)

    # Gradient: ustte #4f7cff, altta #7a4fff
    grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(grad)
    for y in range(size):
        t = y / max(1, size - 1)
        r = int(0x4f + (0x7a - 0x4f) * t)
        g = int(0x7c + (0x4f - 0x7c) * t)
        b = int(0xff + (0xff - 0xff) * t)
        gdraw.line([(0, y), (size, y)], fill=(r, g, b, 255))

    # Yuvarlak mask
    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    img.paste(grad, (0, 0), mask)

    # Hafif ic glow (uste acik, alta gollge)
    highlight = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(highlight)
    hdraw.rounded_rectangle(
        [int(size * 0.06), int(size * 0.06), int(size * 0.94), int(size * 0.55)],
        radius=int(size * 0.18),
        fill=(255, 255, 255, 30),
    )
    img = Image.alpha_composite(img, highlight)

    draw = ImageDraw.Draw(img)

    # "R → R" metni: yeniden adlandirmayi temsil eder
    # Font secimi: Segoe UI Bold (Windows), fallback: default
    font = None
    for candidate in [
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
    ]:
        if os.path.exists(candidate):
            try:
                font = ImageFont.truetype(candidate, int(size * 0.42))
                break
            except OSError:
                continue
    if font is None:
        font = ImageFont.load_default()

    # Metin: "A→B" - yeniden adlandirma
    text_old = "A"
    text_new = "Z"
    arrow = "→"

    # Once metinleri olcelim
    def text_w(s, fnt):
        bbox = draw.textbbox((0, 0), s, font=fnt)
        return bbox[2] - bbox[0], bbox[3] - bbox[1]

    w1, h1 = text_w(text_old, font)
    wa, ha = text_w(arrow, font)
    w2, h2 = text_w(text_new, font)

    gap = int(size * 0.03)
    total_w = w1 + gap + wa + gap + w2
    y = (size - max(h1, ha, h2)) // 2 - int(size * 0.06)
    x = (size - total_w) // 2

    # Golge
    shadow_off = max(1, size // 80)
    shadow_color = (0, 0, 0, 80)
    draw.text((x + shadow_off, y + shadow_off), text_old, font=font, fill=shadow_color)
    draw.text((x + w1 + gap + shadow_off, y + shadow_off), arrow, font=font, fill=shadow_color)
    draw.text((x + w1 + gap + wa + gap + shadow_off, y + shadow_off), text_new, font=font, fill=shadow_color)

    # Beyaz metin
    white = (255, 255, 255, 255)
    draw.text((x, y), text_old, font=font, fill=white)
    draw.text((x + w1 + gap, y), arrow, font=font, fill=(255, 230, 140, 255))  # altin ok
    draw.text((x + w1 + gap + wa + gap, y), text_new, font=font, fill=white)

    return img


def main():
    sizes = [16, 24, 32, 48, 64, 128, 256]
    images = [make_base(s) for s in sizes]

    # Kaydet: PNG (preview) ve ICO (exe icin)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    png_path = os.path.join(out_dir, "icon_256.png")
    ico_path = os.path.join(out_dir, "app.ico")

    images[-1].save(png_path, "PNG")

    # .ico — coklu boyut
    images[-1].save(
        ico_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
    )
    print(f"OK: {ico_path}")
    print(f"OK: {png_path}")


if __name__ == "__main__":
    main()
