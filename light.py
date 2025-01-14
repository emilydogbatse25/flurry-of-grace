from vector3d import Vector3d

class Light:
    def __init__(self, position, ambient, diffuse, specular, color):
        """Initialize light with position and lighting properties."""
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.color = self.normalizeColor(color)

    def normalizeColor(self, color):
        """Convert RGB color from 0-255 range to 0-1 range."""
        return Vector3d(
            color[0] / 255.0,
            color[1] / 255.0,
            color[2] / 255.0
        )

    def getPosition(self):
        """Get light position."""
        return self.position

    def setPosition(self, position):
        """Set light position."""
        self.position = position

    def setIntensities(self, ambient=None, diffuse=None, specular=None):
        """Update light intensities."""
        if ambient is not None:
            self.ambient = ambient
        if diffuse is not None:
            self.diffuse = diffuse
        if specular is not None:
            self.specular = specular

    def getColor(self):
        """Get normalized light color."""
        return self.color

    def setColor(self, color):
        """Set light color (in RGB 0-255 range)."""
        self.color = self.normalizeColor(color)