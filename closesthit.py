class ClosestHit:
    def __init__(self):
        self.hit_point = None      # Point of intersection
        self.normal = None         # Surface normal at hit point
        self.t = float('inf')      # Distance along ray
        self.color = None          # Color at hit point
        self.sphere_center = None  # Center of hit sphere
        self.textureType = None    # Texture type of hit object
        self.shadowType = None     # Shadow type of hit object

    def reset(self):
        """Reset the hit record to initial state."""
        self.__init__()

    def update(self, t, hit_point, normal, color, sphere_center, textureType, shadowType):
        """Update all hit record parameters."""
        self.t = t
        self.hit_point = hit_point
        self.normal = normal
        self.color = color
        self.sphere_center = sphere_center
        self.textureType = textureType
        self.shadowType = shadowType