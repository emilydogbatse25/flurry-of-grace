import math
from vector3d import Vector3d
from ray import Ray
from constants import *

class Camera:
    def __init__(self, lookFrom, lookAt, vUp, vfov, aspect):
        """Initialize camera for Sugar Plum Fairy animation."""
        self.lookFrom = lookFrom
        self.lookAt = lookAt
        self.vUp = vUp
        self.vfov = vfov
        self.aspect = aspect
        
        self._updateCamera()

    def _updateCamera(self):
        """Update all camera parameters."""
        # Calculate viewport dimensions
        theta = math.radians(self.vfov)
        half_height = math.tan(theta/2)
        half_width = self.aspect * half_height
        
        # Calculate basis vectors
        self.w = (self.lookFrom - self.lookAt).normalize()
        self.u = self.vUp.cross(self.w).normalize()
        self.v = self.w.cross(self.u)
        
        # Calculate viewport corners and dimensions
        self.origin = self.lookFrom
        self.horizontal = self.u * (2.0 * half_width)
        self.vertical = self.v * (2.0 * half_height)
        self.lower_left = (self.origin - 
                          (self.horizontal * 0.5) - 
                          (self.vertical * 0.5) - 
                          self.w)

    def getARay(self, s, t):
        """Get ray for current camera position."""
        direction = (self.lower_left + 
                    self.horizontal * s + 
                    self.vertical * t - 
                    self.origin)
        return Ray(self.origin, direction)

    def updateForAnimation(self, t):
        """
        Update camera for Christmas ballet animation.
        t ranges from 0 to 1 representing animation progress.
        """
        if t < PHASE_1_END:
            # Phase 1: Opening sequence - Graceful descent
            phase_t = t / PHASE_1_END
            height = 12 - phase_t * 4  # Start high, descend slowly
            radius = 12 - phase_t * 2  # Move closer
            angle = phase_t * math.pi * 0.5  # Gentle rotation
            
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius + 8
            y = height + math.sin(phase_t * math.pi * 2) * 0.5
            
            self.lookFrom = Vector3d(x, y, z)
            self.lookAt = Vector3d(0, 1 - phase_t, -2)
            
        elif t < PHASE_2_END:
            # Phase 2: Main dance - Orbital movement
            phase_t = (t - PHASE_1_END) / (PHASE_2_END - PHASE_1_END)
            base_height = 8
            radius = 10
            
            # Create graceful circular motion
            angle = phase_t * math.pi * 3  # 1.5 orbits during main dance
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius + 6
            y = base_height + math.sin(phase_t * math.pi * 4) * 1.0
            
            self.lookFrom = Vector3d(x, y, z)
            self.lookAt = Vector3d(0, 2 + math.sin(phase_t * math.pi * 2), -2)
            
        else:
            # Phase 3: Crystal finale - Rising movement
            phase_t = (t - PHASE_2_END) / (PHASE_3_END - PHASE_2_END)
            
            # Spiral upward movement
            angle = phase_t * math.pi * 2
            radius = 8 + phase_t * 2
            height = 8 + phase_t * 6
            
            x = math.cos(angle) * radius
            z = math.sin(angle) * radius + 6
            y = height + math.sin(phase_t * math.pi * 3) * 0.5
            
            self.lookFrom = Vector3d(x, y, z)
            self.lookAt = Vector3d(0, 4 + phase_t * 3, -2)
        
        # Always maintain vertical up vector
        self.vUp = Vector3d(0, 1, 0)
        
        # Update camera parameters
        self._updateCamera()
