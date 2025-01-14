class Ray:
    def __init__(self, origin, direction):
        """Initialize ray with origin point and direction vector."""
        self.origin = origin
        self.direction = direction.normalize()

    def getOrigin(self):
        """Get ray origin point."""
        return self.origin

    def getDirection(self):
        """Get normalized ray direction."""
        return self.direction

    def getPointAtParameter(self, t):
        """Get point along ray at parameter t."""
        return self.origin + self.direction * t

    def reflect(self, normal):
        """Calculate reflection direction given surface normal."""
        return self.direction - normal * 2 * self.direction.dot(normal)