"""Generate default Open Graph PNG image (1200x630)."""

from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise SystemExit("Install Pillow first: pip install pillow")


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "app" / "static" / "images" / "og-default.png"
    img = Image.new("RGB", (1200, 630), color=(37, 99, 235))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 64)
        font_sm = ImageFont.truetype("arial.ttf", 32)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    draw.text((80, 240), "Seller Toolkit", fill=(255, 255, 255), font=font)
    draw.text((80, 330), "Free Tools for eCommerce Sellers", fill=(219, 234, 254), font=font_sm)
    img.save(out, format="PNG", optimize=True)
    print(f"Created {out}")


if __name__ == "__main__":
    main()
