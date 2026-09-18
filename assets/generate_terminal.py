import os
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 860
HEIGHT = 400
SCALE = 2  # 2x supersampling
SW = WIDTH * SCALE
SH = HEIGHT * SCALE

font_mono_bold = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf', 14 * SCALE)
font_mono_reg = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf', 14 * SCALE)
font_title = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf', 13 * SCALE)
font_status = ImageFont.truetype('/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf', 12 * SCALE)

# Color Palette (Orange & Black Hacker Theme)
BG_TERM = (11, 14, 20, 255)            # Deep stealth black/charcoal
BORDER_ORANGE = (255, 102, 0, 240)     # Neon Orange Accent
TITLE_BG = (18, 22, 30, 255)           # Window Title Bar
TITLE_BORDER = (255, 102, 0, 90)

PROMPT_USER = (255, 119, 0, 255)       # Orange
PROMPT_HOST = (255, 165, 0, 255)       # Amber Orange
PROMPT_PUNCT = (139, 148, 158, 255)    # Gray
PROMPT_SYMBOL = (255, 102, 0, 255)     # Orange ~$
CMD_COLOR = (245, 247, 250, 255)       # Crisp White
OUTPUT_HI = (255, 160, 50, 255)        # Glowing Orange
OUTPUT_TAG = (255, 119, 0, 255)        # Bold Orange
OUTPUT_VAL = (235, 240, 245, 255)      # White
OUTPUT_SPECIAL = (255, 185, 65, 255)   # Amber Gold
STATUS_GREEN = (63, 185, 80, 255)      # Green check
CURSOR_COLOR = (255, 102, 0, 255)      # Orange Block Cursor

def draw_base_window(draw):
    rect = [8 * SCALE, 8 * SCALE, SW - 8 * SCALE, SH - 8 * SCALE]
    draw.rounded_rectangle(rect, radius=12 * SCALE, fill=BG_TERM, outline=BORDER_ORANGE, width=2 * SCALE)
    
    # Title bar
    draw.rounded_rectangle([8 * SCALE, 8 * SCALE, SW - 8 * SCALE, 46 * SCALE], radius=12 * SCALE, fill=TITLE_BG)
    draw.rectangle([8 * SCALE, 34 * SCALE, SW - 8 * SCALE, 46 * SCALE], fill=TITLE_BG)
    draw.line([(8 * SCALE, 46 * SCALE), (SW - 8 * SCALE, 46 * SCALE)], fill=TITLE_BORDER, width=1 * SCALE)
    
    # macOS style buttons
    draw.ellipse([26 * SCALE, 21 * SCALE, 38 * SCALE, 33 * SCALE], fill=(255, 95, 86, 255))
    draw.ellipse([46 * SCALE, 21 * SCALE, 58 * SCALE, 33 * SCALE], fill=(255, 189, 46, 255))
    draw.ellipse([66 * SCALE, 21 * SCALE, 78 * SCALE, 33 * SCALE], fill=(39, 201, 63, 255))
    
    # Title
    draw.text((SW // 2, 27 * SCALE), "⚡ ghost@domain-controller: ~ (Active Directory Exploitation)", fill=(255, 153, 51, 255), font=font_title, anchor="mm")
    draw.text((SW - 25 * SCALE, 27 * SCALE), "[OPSEC: STEALTH]", fill=(255, 102, 0, 255), font=font_status, anchor="rm")

def get_prompt_segments():
    return [
        ("ghost", PROMPT_USER, font_mono_bold),
        ("@", PROMPT_PUNCT, font_mono_bold),
        ("ad-infra", PROMPT_HOST, font_mono_bold),
        (":", PROMPT_PUNCT, font_mono_reg),
        ("~$ ", PROMPT_SYMBOL, font_mono_bold)
    ]

def render_frame(lines_data, cursor_line_idx=None, cursor_active=True):
    img = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_base_window(draw)
    
    start_x = 28 * SCALE
    start_y = 66 * SCALE
    line_spacing = 28 * SCALE
    
    cursor_box = None
    
    for i, line in enumerate(lines_data):
        curr_x = start_x
        curr_y = start_y + i * line_spacing
        for text, color, font in line:
            draw.text((curr_x, curr_y), text, fill=color, font=font)
            bbox = font.getbbox(text)
            text_width = bbox[2] - bbox[0]
            curr_x += text_width
            
        if cursor_active and i == cursor_line_idx:
            cursor_w = 9 * SCALE
            cursor_h = 17 * SCALE
            cursor_box = [curr_x + 2 * SCALE, curr_y + 1 * SCALE, curr_x + 2 * SCALE + cursor_w, curr_y + 1 * SCALE + cursor_h]
            
    if cursor_box:
        draw.rectangle(cursor_box, fill=CURSOR_COLOR)
        
    frame = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    return frame.convert("RGB")

frames = []
durations = []

def add_frame(lines, cursor_line, cursor_on, dur=80):
    frames.append(render_frame(lines, cursor_line, cursor_on))
    durations.append(dur)

prompt = get_prompt_segments()

# 0. Initial prompt blink
base = [list(prompt)]
add_frame(base, 0, True, 250)
add_frame(base, 0, False, 200)
add_frame(base, 0, True, 250)

# 1. Type "whoami"
cmd1 = "whoami"
for j in range(1, len(cmd1) + 1):
    current = [list(prompt) + [(cmd1[:j], CMD_COLOR, font_mono_reg)]]
    add_frame(current, 0, True, 90)

add_frame([list(prompt) + [(cmd1, CMD_COLOR, font_mono_reg)]], 0, True, 200)

# Output 1: "⚡ Hi, I am Leandros"
out1 = [("⚡ Hi, I am Leandros", OUTPUT_HI, font_mono_bold)]
step1 = [
    list(prompt) + [(cmd1, CMD_COLOR, font_mono_reg)],
    out1
]
add_frame(step1, 1, False, 350)

# 2. Add prompt for specialization
step2_prompt = list(step1) + [list(prompt)]
add_frame(step2_prompt, 2, True, 200)

# Type "cat /etc/specialization"
cmd2 = "cat /etc/specialization"
for j in range(2, len(cmd2) + 1, 2):
    typed = cmd2[:j]
    add_frame(list(step1) + [list(prompt) + [(typed, CMD_COLOR, font_mono_reg)]], 2, True, 70)
if len(cmd2) % 2 != 0:
    add_frame(list(step1) + [list(prompt) + [(cmd2, CMD_COLOR, font_mono_reg)]], 2, True, 70)

add_frame(list(step1) + [list(prompt) + [(cmd2, CMD_COLOR, font_mono_reg)]], 2, True, 200)

# Outputs for specialization
out2_1 = [("  [*] Role   : ", OUTPUT_TAG, font_mono_bold), ("Penetration Tester", OUTPUT_VAL, font_mono_bold)]
out2_2 = [("  [*] Degree : ", OUTPUT_TAG, font_mono_bold), ("MSc Cybersecurity", OUTPUT_VAL, font_mono_bold)]
out2_3 = [("  [*] Focus  : ", OUTPUT_TAG, font_mono_bold), ("Specializes in Active Directory Pentesting", OUTPUT_SPECIAL, font_mono_bold)]

step3 = list(step1) + [
    list(prompt) + [(cmd2, CMD_COLOR, font_mono_reg)],
    out2_1,
    out2_2,
    out2_3
]
add_frame(step3, 5, False, 350)

# 3. Add prompt for ghost mode status
step4_prompt = list(step3) + [list(prompt)]
add_frame(step4_prompt, 6, True, 200)

# Type "./ghost_mode.sh --status"
cmd3 = "./ghost_mode.sh --status"
for j in range(2, len(cmd3) + 1, 2):
    typed = cmd3[:j]
    add_frame(list(step3) + [list(prompt) + [(typed, CMD_COLOR, font_mono_reg)]], 6, True, 70)
if len(cmd3) % 2 != 0:
    add_frame(list(step3) + [list(prompt) + [(cmd3, CMD_COLOR, font_mono_reg)]], 6, True, 70)

add_frame(list(step3) + [list(prompt) + [(cmd3, CMD_COLOR, font_mono_reg)]], 6, True, 200)

# Output for ghost mode
out3 = [
    ("  [✓] ", STATUS_GREEN, font_mono_bold),
    ("Identity: ", OUTPUT_TAG, font_mono_bold),
    ("Talented Ghost", OUTPUT_HI, font_mono_bold),
    ("  |  ", PROMPT_PUNCT, font_mono_reg),
    ("TTPs: ", OUTPUT_TAG, font_mono_bold),
    ("Living off the Land", OUTPUT_VAL, font_mono_reg),
    ("  |  ", PROMPT_PUNCT, font_mono_reg),
    ("Detections: ", OUTPUT_TAG, font_mono_bold),
    ("Zero", (63, 185, 80, 255), font_mono_bold)
]

final_screen = list(step3) + [
    list(prompt) + [(cmd3, CMD_COLOR, font_mono_reg)],
    out3,
    list(prompt)
]

# Final hold: cursor blinks at bottom prompt for 3.5 seconds
for _ in range(5):
    add_frame(final_screen, 8, True, 450)
    add_frame(final_screen, 8, False, 300)

# Quantize and save GIF
print(f"Total frames generated: {len(frames)}")
output_gif_path = "/home/leandros/mygithub/FallenGodfather/assets/terminal.gif"

palette_img = frames[0].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
quantized_frames = [f.quantize(palette=palette_img, dither=Image.Dither.NONE) for f in frames]

quantized_frames[0].save(
    output_gif_path,
    save_all=True,
    append_images=quantized_frames[1:],
    duration=durations,
    loop=0,
    optimize=True
)

file_size = os.path.getsize(output_gif_path)
print(f"Successfully saved {output_gif_path}, size: {file_size / 1024:.2f} KB")
