#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261124 (v1).

Dense newspaper front page, 1024x1024, PIL + DejaVu only. One lead
story (Iran / Strait of Hormuz) plus a 3-column grid of 30 short
verified stories from Tuesday 24 November 2026, grouped by region
and field. No network, no randomness, no timestamps: deterministic
output, two runs write identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (247, 243, 232)
INK = (17, 24, 39)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREY = (75, 85, 99)
BODY = (55, 65, 81)
WHITE = (255, 255, 255)
BORDER = (203, 213, 225)

FD = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FD + name, size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def text_center(y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)


def wrap(s, f, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in s.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(s, f, max_w, max_lines):
    """Wrap and truncate with an ellipsis if it needs more lines."""
    lines = wrap(s, f, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and d.textlength(lines[-1] + " ...", font=f) > max_w:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
    lines[-1] = (lines[-1] + " ...").strip()
    return lines


# Top bar
d.rectangle([0, 0, W, 8], fill=RED)

# Masthead
text_center(18, "TUESDAY  24 NOVEMBER 2026", F_SERIF_B(38), INK)
text_center(64, "WORLD NEWS IN ONE IMAGE", F_SANS_B(22), RED)
text_center(92, "31 stories from one day \u2014 war in the Gulf, a chip rout, a Dow record",
            F_SANS(16), GREY)
d.line([28, 118, 996, 118], fill=INK, width=2)

# Lead story
d.rounded_rectangle([28, 128, 996, 264], radius=10, fill=WHITE,
                    outline=INK, width=2)
d.rectangle([28, 128, 40, 264], fill=RED)
d.text((52, 138), "TOP STORY  \u00b7  MIDDLE EAST  \u00b7  STRAIT OF HORMUZ",
       font=F_SANS_B(14), fill=RED)
d.text((52, 158), "MINES HIT TANKERS IN THE STRAIT OF HORMUZ",
       font=F_SANS_B(29), fill=INK)
lead_body = ("Iran's Revolutionary Guards say three oil tankers hit naval "
             "mines in the strait; six tankers have been hit in all. The US "
             "is investigating cyberattacks on up to 50 tankers.")
y = 196
for line in fit_lines(lead_body, F_SANS(16), 924, 2):
    d.text((52, y), line, font=F_SANS(16), fill=INK)
    y += 21
d.text((52, 240), "SIX TANKERS HIT   \u2022   HOUTHIS STRIKE A RIYADH TOWER, 11 HURT   \u2022   US PROBES 50 TANKERS",
       font=F_SANS_B(14), fill=RED)

# Grid: 30 stories, 3 columns x 10 rows
stories = [
    # Middle East & war
    ("MIDDLE EAST \u00b7 GAZA", "HAMAS SECURITY CHIEF KILLED",
     "Naim Abu Nahal, 50, is among seven killed in Israeli strikes in Gaza."),
    ("UKRAINE \u00b7 ZAPORIZHZHIA", "2 KILLED, 40 WOUNDED IN STRIKE",
     "Russian overnight attack hits a house and a five-storey block; four children hurt."),
    ("UKRAINE \u00b7 BERLIN", "GERMANY FIRST INTO DELTA",
     "Berlin signs a letter of intent for access to Ukraine's Delta battlefield system."),
    ("CONGO \u00b7 ITURI", "EBOLA TEAM FLEES AFTER 3 DAYS",
     "WHO workers leave a hospital after sheltering in a maternity ward amid fighting."),
    ("S. SUDAN \u00b7 TONJ EAST", "UN SENDS PATROLS TO TONJ EAST",
     "Peacekeepers deploy after a weekend cattle-camp attack with a heavy death toll."),
    # Asia
    ("KOREA \u00b7 ADIZ", "RUSSIAN JETS ENTER KOREA ADIZ",
     "Fighters scramble after a false alert wrongly claims a North Korean jet crossed in."),
    ("ASIA \u00b7 QUAKES", "QUAKES HIT PAKISTAN, NEPAL",
     "A 4.1 quake hits Pakistan; a 5.4 quake in Nepal is felt in India, Bhutan, Bangladesh."),
    ("CHIPS \u00b7 SINGAPORE", "US BLACKLISTS MEGASPEED",
     "Washington adds the cloud firm and six related companies to its Entity List."),
    ("MARKETS \u00b7 ASIA", "ASIAN STOCKS SURGE ON HUANG",
     "Kospi +7.5%, Nikkei +3.9% and Taiwan +9% as Nvidia's CEO comeback revives AI."),
    ("CHINA \u00b7 TRADE", "CHINA EXTENDS MINERALS TRUCE",
     "China prolongs its suspension of export curbs on critical minerals to the US."),
    ("JAPAN \u00b7 ECONOMY", "JAPAN FACTORIES PICK UP PACE",
     "Japan's manufacturing PMI rises to 53.7 as chip and electronics demand lifts output."),
    # Americas
    ("TRADE \u00b7 WASHINGTON", "TRUMP PLANS NEW TARIFFS",
     "US weighs duties on China, the EU and 14 others over subsidies; EU and Japan face 15% or less."),
    ("CANADA \u00b7 OTTAWA", "CANADA: WE DON'T REPORT TO US",
     "Defence minister David McGuinty answers the Pentagon's blunt fact sheet on spending."),
    ("VENEZUELA \u00b7 CARACAS", "VENEZUELA DEBT: $237.5 BILLION",
     "Venezuela publishes its economic framework; output is forecast to more than double."),
    # Europe
    ("WEATHER \u00b7 BRITAIN", "FLOODS SWAMP WALES, FRANCE",
     "A red flood warning in Pembrokeshire leaves a McDonald's under water; Pas-de-Calais on alert."),
    ("EUROPE \u00b7 AUTOS", "EVS NEAR 30% OF EU CAR SALES",
     "Battery electrics hit 29.8% of October registrations; BYD +119% and Chery +151%."),
    # Markets & tech
    ("WALL ST \u00b7 NEW YORK", "DOW CLOSES ABOVE 50,000",
     "Dow +0.85% to 50,018.70 while the S&P 500 falls 0.5% and the Nasdaq drops 1.5%."),
    ("TECH \u00b7 NVIDIA", "NVIDIA GIVES BACK 5.9%",
     "Shares fall a day after a 31.5% jump on Jensen Huang's return as chief executive."),
    ("ECONOMY \u00b7 US", "US CONFIDENCE JUMPS TO 103.3",
     "The Conference Board index hits its highest since January 2025, beating forecasts."),
    ("TECH \u00b7 ANTHROPIC", "ANTHROPIC BELOW IPO PRICE",
     "The AI firm slips under its $83 listing price as the tech sell-off resumes."),
    ("ENERGY \u00b7 OIL", "OIL NEAR 3-MONTH LOW",
     "Brent holds near $89 as rising supply outweighs the threat to shipping in the strait."),
    ("CRYPTO \u00b7 BITCOIN", "BITCOIN SLIPS TO $59,655",
     "Bitcoin falls 2.7% as crypto joins the sell-off; gold drops 2.7% to $3,553 an ounce."),
    ("TECH \u00b7 DELL", "DELL REVENUE DOUBLES ON AI",
     "Quarterly sales hit $54.9bn, up 103%; AI server backlog reaches a record $132.3bn."),
    ("CHIPS \u00b7 SEMIS", "CHIP STOCKS GIVE BACK GAINS",
     "Micron -11%, AMD -9% and Analog Devices -17% despite beating estimates."),
    ("RETAIL \u00b7 US", "RETAILERS SURGE ON GUIDANCE",
     "Abercrombie +19.7%, Kohl's +19.5% and Dick's +14.6% lead Wall Street's gainers."),
    ("MARKETS \u00b7 EUROPE", "EUROPE SLIPS ON TARIFF FEARS",
     "Stoxx 600 -0.66% and DAX -1.26% as tariff reports and the tech rout weigh on shares."),
    ("PHARMA \u00b7 PARIS", "SANOFI DEAL LIFTS INSMED 14%",
     "Insmed jumps 14% on a deal with Sanofi, whose shares rise 9.7% in Paris."),
    # Sport, space & culture
    ("FOOTBALL \u00b7 UCL", "REAL MADRID THRASH PSV 5-1",
     "Mbapp\u00e9 scores twice in the Champions League; Man City draw 2-2 with Napoli, Arsenal 1-1."),
    ("SPACE \u00b7 LAUNCHES", "THREE ROCKETS FLY IN ONE DAY",
     "SpaceX launches a classified USSF-266 mission; Soyuz resupplies the ISS; Ariane lifts Leo."),
    ("CULTURE \u00b7 SAN JUAN", "MISS UNIVERSE FINAL IN SAN JUAN",
     "The 75th pageant crowns a new winner in Puerto Rico, with 116 contestants on stage."),
]

assert len(stories) == 30, len(stories)
COLS = [28, 354, 680]
CW, CH, GAP = 314, 68, 4
Y0 = 274
for i, (cat, head, body) in enumerate(stories):
    col, row = i % 3, i // 3
    x, y = COLS[col], Y0 + row * (CH + GAP)
    d.rounded_rectangle([x, y, x + CW, y + CH], radius=8, fill=WHITE,
                        outline=BORDER, width=1)
    d.text((x + 8, y + 5), cat, font=F_SANS_B(11), fill=RED)
    head_lines = fit_lines(head, F_SANS_B(15), CW - 16, 2)
    hy = y + 20
    for line in head_lines:
        d.text((x + 8, hy), line, font=F_SANS_B(15), fill=INK)
        hy += 16
    body_max = 2 if len(head_lines) == 1 else 1
    by = hy + 3
    for line in fit_lines(body, F_SANS(12), CW - 16, body_max):
        d.text((x + 8, by), line, font=F_SANS(12), fill=BODY)
        by += 13

# Footer
d.line([28, 996, 996, 996], fill=INK, width=2)
text_center(1004, "24 NOVEMBER 2026  \u00b7  HORMUZ  \u00b7  GAZA  \u00b7  UKRAINE  \u00b7  DOW 50,000  \u00b7  NVIDIA  \u00b7  DELL  \u00b7  CHAMPIONS LEAGUE",
            F_SANS_B(13), INK)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size, "stories:", 1 + len(stories))
