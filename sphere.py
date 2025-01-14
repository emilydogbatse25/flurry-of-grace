from vector3d import Vector3d
import math

class Sphere:
    def __init__(self, center, radius, color, textureType="None", shadowType="None"):
        """Initialize sphere with position, size, and appearance properties."""
        self.center = center
        self.radius = radius
        self.color = color
        self.textureType = textureType
        self.shadowType = shadowType

    def rayIntersect(self, ray):
        """Calculate ray-sphere intersection."""
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return False, float('inf')

        # Find closest intersection
        sqrt_disc = math.sqrt(discriminant)
        t1 = (-b - sqrt_disc) / (2.0 * a)
        t2 = (-b + sqrt_disc) / (2.0 * a)

        if t1 > 0:
            return True, t1
        if t2 > 0:
            return True, t2
        return False, float('inf')

    def getNormalAt(self, point):
        """Calculate surface normal at given point."""
        return (point - self.center).normalize()

    def getColor(self):
        """Get sphere color."""
        return self.color

    def getTextureType(self):
        """Get texture type (None, Stripe, or Checkerboard)."""
        return self.textureType

    def getShadowType(self):
        """Get shadow type (Sharp or Smooth)."""
        return self.shadowType

    def getCenter(self):
        """Get sphere center position."""
        return self.center

    def getRadius(self):
        """Get sphere radius."""
        return self.radius