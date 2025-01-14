from vector3d import Vector3d

# Image resolution settings - lower for rough animation
IMAGE_WIDTH = 300
IMAGE_HEIGHT = 150

# Animation settings
FPS = 24
DURATION = 10  # 6 seconds for rough animation
TOTAL_FRAMES = FPS * DURATION  # 144 frames

# Reduced quality settings for faster rendering
ANTI_ALIASING_SAMPLES = 2
SOFT_SHADOW_SAMPLES = 2
MAX_RAY_DEPTH = 2
RAY_EPSILON = 0.001

# Camera settings
CAMERA_FOV = 60.0
CAMERA_ASPECT = IMAGE_WIDTH / IMAGE_HEIGHT

# Christmas Color Palette
CHRISTMAS_RED = (220, 20, 60)     # Main ornament red
CHRISTMAS_GREEN = (34, 139, 34)   # Forest green accents
GOLD = (255, 215, 0)              # Gold ornament
SILVER = (192, 192, 192)          # Silver ornament
WHITE = (255, 255, 255)           # Snow color

# Light colors
WARM_GOLD_LIGHT = (255, 230, 140)  # Warm golden glow
COOL_SILVER_LIGHT = (220, 240, 255) # Cool moonlight

# Background colors
BACKGROUND_COLOR_TOP = (25, 25, 112)     # Dark midnight blue
BACKGROUND_COLOR_BOTTOM = (47, 79, 79)   # Dark slate gray

# Light settings
AMBIENT_INTENSITY = 0.1
DIFFUSE_INTENSITY = 0.7
SPECULAR_INTENSITY = 0.5

# Material settings
SPECULAR_POWER = 32.0
SHADOW_INTENSITY = 0.7

# Animation phase timing
PHASE_1_END = 0.33
PHASE_2_END = 0.66
PHASE_3_END = 1.0

# Texture settings
STRIPE_FREQUENCY = 8.0      # Controls density of stripes
CHECKERBOARD_SCALE = 4.0    # Controls size of checkerboard squares

# Bezier curve control points (main red ornament)
P0 = Vector3d(-2, 0, -2)
P1 = Vector3d(-1, 2, -2)
P2 = Vector3d(1, 2, -2)
P3 = Vector3d(2, 0, -2)

# Secondary Bezier curve (silver ornament)
P0_2 = Vector3d(2, 0, -1)
P1_2 = Vector3d(1, 3, -1)
P2_2 = Vector3d(-1, 3, -1)
P3_2 = Vector3d(-2, 0, -1)

# Circular motion settings
CIRCLE_RADIUS = 1.5
CIRCLE_HEIGHT = 1.0
CIRCLE_VERTICAL_SPEED = 2.0
CIRCLE_ORBIT_SPEED = 1.5
BOUNCE_AMOUNT = 0.2

# Types
SHADOW_TYPE_SHARP = "Sharp"
SHADOW_TYPE_SMOOTH = "Smooth"
TEXTURE_TYPE_NONE = "None"
TEXTURE_TYPE_STRIPE = "Stripe"
TEXTURE_TYPE_CHECKERBOARD = "Checkerboard"