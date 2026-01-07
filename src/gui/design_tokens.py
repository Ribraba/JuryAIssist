"""
Design tokens extraits du design Figma.
"""

# === COLORS ===
COLORS = {
    "#000000": {  # Used in: Transcription brute, Playlist section title, Rechercher
        "hex": "#000000",
    },
    "#1e1e1e": {  # Used in: Page 1 (bg)
        "hex": "#1e1e1e",
    },
    "#444444": {  # Used in: Édition, Pédale connectée (RS-31), Lecture
        "hex": "#444444",
    },
    "#477ed8": {  # Used in: Rectangle 12
        "hex": "#477ed8",
    },
    "#eeeeee": {  # Used in: Timeline brouillon (bg), Timeline brouillon
        "hex": "#eeeeee",
    },
    "#f7f7f7": {  # Used in: Menu item, Menu item (bg)
        "hex": "#f7f7f7",
    },
    "#ffffff": {  # Used in: Home Page (bg), Home Page, Sidebar
        "hex": "#ffffff",
    },
}

# === TYPOGRAPHY ===
TYPOGRAPHY = {
    "Inter_11_0px_400": {
        "family": "Inter",
        "size": 11.0,
        "weight": 400,
        # Used for: Pédale connectée (RS-31)
    },
    "Inter_15_0px_400": {
        "family": "Inter",
        "size": 15.0,
        "weight": 400,
        # Used for: 00:15 / 02:45:30
    },
    "Inter_16_0px_400": {
        "family": "Inter",
        "size": 16.0,
        "weight": 400,
        # Used for: Lecture
    },
    "Inter_16_0px_500": {
        "family": "Inter",
        "size": 16.0,
        "weight": 500,
        # Used for: Rechercher
    },
    "Inter_16_0px_600": {
        "family": "Inter",
        "size": 16.0,
        "weight": 600,
        # Used for: Transcriptions
    },
    "Inter_20_0px_500": {
        "family": "Inter",
        "size": 20.0,
        "weight": 500,
        "letterSpacing": -0.4,
        # Used for: Veuillez vous asseoir. La séance est ouverte. Maître, vous avez la parole. Merci, Monsieur le
    },
    "Inter_20_0px_600": {
        "family": "Inter",
        "size": 20.0,
        "weight": 600,
        "letterSpacing": -0.2,
        # Used for: Title
    },
    "Inter_24_0px_500": {
        "family": "Inter",
        "size": 24.0,
        "weight": 500,
        "letterSpacing": -0.48,
        # Used for: M. le Juge : Veuillez vous asseoir. La séance est ouverte. Maître, vous avez la parole. [00:15] Avocat : Merci, Monsieur le Président. Nous plaidons aujourd’hui pour la défense de M. Martin...
    },
    "Inter_34_0px_600": {
        "family": "Inter",
        "size": 34.0,
        "weight": 600,
        "letterSpacing": -0.68,
        # Used for: Transcription brute
    },
}

# === SPACING ===
SPACING = [4.0, 8.0, 16.0, 24.0]
