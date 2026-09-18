import math, os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 860
HEIGHT = 220
SCALE = 2
SW = WIDTH * SCALE
SH = HEIGHT * SCALE

font_bold = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf', 12 * SCALE)
font_reg = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf', 11 * SCALE)
font_small = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf', 10 * SCALE)
font_title = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf', 13 * SCALE)

BG_COLOR = (11, 14, 20, 255)
BORDER_ORANGE = (255, 102, 0, 240)
HUD_ORANGE = (255, 119, 0, 180)
HUD_DIM = (255, 102, 0, 60)
TEXT_WHITE = (240, 246, 252, 255)
TEXT_ORANGE = (255, 140, 0, 255)
TEXT_GREEN = (63, 185, 80, 255)

# Radar center
RCX = 130 * SCALE
RCY = 110 * SCALE
RR = 85 * SCALE

frames = []
durations = []
num_frames = 24

ad_steps = [
    ("01", "BloodHound Recon & Graph Mapping", "[ GRAPH MAPPED ]", TEXT_GREEN),
    ("02", "Kerberoasting & AS-REP Extraction", "[ 3 HASHES DUMPED ]", TEXT_ORANGE),
    ("03", "ADCS Vulnerability Chain (ESC1)", "[ CSR SIGNED: DA ]", TEXT_ORANGE),
    ("04", "Domain Compromise & DCSync Rights", "[ DOMAIN COMPROMISED ]", (255, 102, 0, 255))
]

nodes = [
    (RCX + int(45 * math.cos(0.5) * SCALE), RCY + int(45 * math.sin(0.5) * SCALE), "DC01"),
    (RCX + int(65 * math.cos(2.2) * SCALE), RCY + int(65 * math.sin(2.2) * SCALE), "CA01"),
    (RCX + int(35 * math.cos(4.0) * SCALE), RCY + int(35 * math.sin(4.0) * SCALE), "SQL01"),
    (RCX + int(70 * math.cos(5.2) * SCALE), RCY + int(70 * math.sin(5.2) * SCALE), "BACKUP")
]

for f in range(num_frames):
    img = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Outer frame
    draw.rounded_rectangle([8 * SCALE, 8 * SCALE, SW - 8 * SCALE, SH - 8 * SCALE], radius=10 * SCALE, fill=BG_COLOR, outline=BORDER_ORANGE, width=2 * SCALE)
    
    # Radar Circles
    for r in [25 * SCALE, 55 * SCALE, RR]:
        draw.ellipse([RCX - r, RCY - r, RCX + r, RCY + r], outline=HUD_DIM, width=1 * SCALE)
        
    # Crosshairs
    draw.line([(RCX - RR, RCY), (RCX + RR, RCY)], fill=HUD_DIM, width=1 * SCALE)
    draw.line([(RCX, RCY - RR), (RCX, RCY + RR)], fill=HUD_DIM, width=1 * SCALE)
    
    # Sweep angle
    angle = (f / num_frames) * 2 * math.pi
    
    # Draw sweep trail
    trail_steps = 12
    for t in range(trail_steps):
        ta = angle - (t / trail_steps) * (math.pi / 2)
        alpha = int(140 * (1 - t / trail_steps))
        tx = RCX + int(RR * math.cos(ta))
        ty = RCY + int(RR * math.sin(ta))
        draw.line([(RCX, RCY), (tx, ty)], fill=(255, 102, 0, alpha), width=2 * SCALE)
        
    # Main beam
    bx = RCX + int(RR * math.cos(angle))
    by = RCY + int(RR * math.sin(angle))
    draw.line([(RCX, RCY), (bx, by)], fill=(255, 200, 100, 255), width=2 * SCALE)
    
    # Target blips on radar
    for nx, ny, name in nodes:
        node_angle = math.atan2(ny - RCY, nx - RCX) % (2 * math.pi)
        diff = (angle - node_angle) % (2 * math.pi)
        if diff < math.pi / 3:
            blip_alpha = int(255 * (1 - diff / (math.pi / 3)))
            draw.ellipse([nx - 4 * SCALE, ny - 4 * SCALE, nx + 4 * SCALE, ny + 4 * SCALE], fill=(255, 165, 0, blip_alpha))
            draw.text((nx + 6 * SCALE, ny - 5 * SCALE), name, fill=(255, 165, 0, blip_alpha), font=font_small)
        else:
            draw.ellipse([nx - 2 * SCALE, ny - 2 * SCALE, nx + 2 * SCALE, ny + 2 * SCALE], fill=(255, 102, 0, 80))
            
    # Radar Label
    draw.text((RCX, RCY + RR + 8 * SCALE), "ACTIVE DIRECTORY RADAR", fill=TEXT_ORANGE, font=font_small, anchor="mm")
    
    # Divider line
    div_x = 240 * SCALE
    draw.line([(div_x, 18 * SCALE), (div_x, SH - 18 * SCALE)], fill=HUD_DIM, width=1 * SCALE)
    
    # Right pane: Active Directory Attack Matrix
    draw.text((div_x + 20 * SCALE, 22 * SCALE), "⚡ ACTIVE DIRECTORY ATTACK SIMULATION // CONTOSO.LOCAL", fill=TEXT_ORANGE, font=font_title)
    
    active_idx = int((f / num_frames) * len(ad_steps))
    start_y = 54 * SCALE
    step_h = 32 * SCALE
    for idx, (num, title, status, stat_color) in enumerate(ad_steps):
        sy = start_y + idx * step_h
        is_done = idx <= active_idx
        num_color = TEXT_ORANGE if is_done else (100, 110, 120, 255)
        title_color = TEXT_WHITE if is_done else (120, 130, 140, 255)
        
        draw.text((div_x + 20 * SCALE, sy), f"[{num}]", fill=num_color, font=font_bold)
        draw.text((div_x + 55 * SCALE, sy), title, fill=title_color, font=font_reg)
        
        if is_done:
            draw.text((SW - 25 * SCALE, sy), status, fill=stat_color, font=font_bold, anchor="ra")
        else:
            draw.text((SW - 25 * SCALE, sy), "[ PENDING ]", fill=(80, 90, 100, 255), font=font_reg, anchor="ra")
            
    # Bottom HUD status ticker
    draw.line([(div_x + 20 * SCALE, SH - 32 * SCALE), (SW - 25 * SCALE, SH - 32 * SCALE)], fill=HUD_DIM, width=1 * SCALE)
    draw.text((div_x + 20 * SCALE, SH - 20 * SCALE), "OPSEC: STEALTH  |  SIEM DETECTIONS: 0  |  OPERATOR: LEANDROS (GHOST)", fill=(255, 153, 51, 255), font=font_small)

    resized = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS).convert("RGB")
    frames.append(resized)
    durations.append(100)

palette_img = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
quantized_frames = [f.quantize(palette=palette_img, dither=Image.Dither.NONE) for f in frames]

out_path = "/home/leandros/mygithub/FallenGodfather/assets/ad_radar.gif"
quantized_frames[0].save(
    out_path,
    save_all=True,
    append_images=quantized_frames[1:],
    duration=durations,
    loop=0,
    optimize=True
)
print(f"Saved {out_path}, size: {os.path.getsize(out_path) / 1024:.2f} KB")
