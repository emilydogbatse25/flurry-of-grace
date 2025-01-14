# import math

# class Vector3d:
#     """
#     A class representing a 3D vector with x, y, and z components.
#     Supports basic vector operations and transformations.
#     """
    
#     EPSILON = 1e-10  # Small value for floating point comparisons
    
#     def __init__(self, x, y, z):
#         """Initialize a 3D vector with given coordinates."""
#         self.x = float(x)  # Convert to float to ensure consistent behavior
#         self.y = float(y)
#         self.z = float(z)

#     def getX(self):
#         """Return the x coordinate."""
#         return self.x

#     def getY(self):
#         """Return the y coordinate."""
#         return self.y
    
#     def getZ(self):
#         """Return the z coordinate."""
#         return self.z

#     def setX(self, x):
#         """Set the x coordinate."""
#         self.x = float(x)

#     def setY(self, y):
#         """Set the y coordinate."""
#         self.y = float(y)
        
#     def setZ(self, z):
#         """Set the z coordinate."""
#         self.z = float(z)

#     def distance(self, vec):
#         """Calculate the Euclidean distance between this vector and another vector."""
#         diffx = self.x - vec.getX()
#         diffy = self.y - vec.getY()
#         diffz = self.z - vec.getZ()
#         return math.sqrt(diffx*diffx + diffy*diffy + diffz*diffz)

#     def dot(self, vec):
#         """Calculate the dot product with another vector."""
#         return (self.x * vec.getX() + 
#                 self.y * vec.getY() + 
#                 self.z * vec.getZ())

#     def cross(self, vec):
#         """
#         Calculate the cross product with another vector.
        
#         Args:
#             vec (Vector3d): The vector to cross with
            
#         Returns:
#             Vector3d: The cross product of this vector with vec
#         """
#         return Vector3d(
#             self.y * vec.getZ() - self.z * vec.getY(),
#             self.z * vec.getX() - self.x * vec.getZ(),
#             self.x * vec.getY() - self.y * vec.getX()
#         )

#     def scale(self, scalar):
#         """
#         Scale the vector by a scalar value.
#         This is an alternative to multiplication that returns a new vector.
        
#         Args:
#             scalar (float): The scaling factor
            
#         Returns:
#             Vector3d: A new scaled vector
#         """
#         return Vector3d(
#             self.x * scalar,
#             self.y * scalar,
#             self.z * scalar
#         )

#     def isZero(self):
#         """Check if this is effectively a zero vector (within epsilon)."""
#         return (abs(self.x) < self.EPSILON and 
#                 abs(self.y) < self.EPSILON and 
#                 abs(self.z) < self.EPSILON)

#     def length(self):
#         """Calculate the length (magnitude) of the vector."""
#         return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

#     def normalize(self):
#         """
#         Normalize the vector to unit length.
#         If the vector is zero, return a zero vector.
#         """
#         length = self.length()
#         if length > self.EPSILON:  # Only normalize if length is not effectively zero
#             return Vector3d(self.x / length, self.y / length, self.z / length)
#         return Vector3d(0, 0, 0)  # Return a zero vector if the length is zero

#     def clamp(self, min_val, max_val):
#         """
#         Clamp vector components between min_val and max_val.
        
#         Args:
#             min_val (float): Minimum value
#             max_val (float): Maximum value
            
#         Returns:
#             Vector3d: A new vector with clamped components
#         """
#         return Vector3d(
#             min(max_val, max(min_val, self.x)),
#             min(max_val, max(min_val, self.y)),
#             min(max_val, max(min_val, self.z))
#         )

#     def rotate(self, thetaDeg, axis='z'):
#         """
#         Rotate the vector around the specified axis by angle in degrees.
        
#         Args:
#             thetaDeg (float): Angle in degrees
#             axis (str): Rotation axis ('x', 'y', or 'z')
            
#         Raises:
#             ValueError: If an invalid axis is specified
#         """
#         if axis.lower() not in {'x', 'y', 'z'}:
#             raise ValueError("Axis must be 'x', 'y', or 'z'")
            
#         thetaRad = math.radians(thetaDeg)
#         costh = math.cos(thetaRad)
#         sinth = math.sin(thetaRad)
        
#         if axis.lower() == 'z':
#             newX = self.x*costh - self.y*sinth
#             newY = self.x*sinth + self.y*costh
#             newZ = self.z
#         elif axis.lower() == 'y':
#             newX = self.x*costh + self.z*sinth
#             newY = self.y
#             newZ = -self.x*sinth + self.z*costh
#         else:  # x axis
#             newX = self.x
#             newY = self.y*costh - self.z*sinth
#             newZ = self.y*sinth + self.z*costh
            
#         self.x = newX
#         self.y = newY
#         self.z = newZ

#     def __str__(self):
#         """Return a string representation of the vector."""
#         return f"({self.x}, {self.y}, {self.z})"

#     def __repr__(self):
#         """Return a detailed string representation of the vector."""
#         return f"Vector3d({self.x}, {self.y}, {self.z})"

#     def print(self, msg=""):
#         """Print the vector with an optional message."""
#         print(f"{msg}: ({self.x}, {self.y}, {self.z})")

#     def __add__(self, vec):
#         """Vector addition."""
#         return Vector3d(self.x + vec.getX(),
#                        self.y + vec.getY(),
#                        self.z + vec.getZ())

#     def __iadd__(self, vec):
#         """In-place vector addition."""
#         self.x += vec.getX()
#         self.y += vec.getY()
#         self.z += vec.getZ()
#         return self

#     def __sub__(self, vec):
#         """Vector subtraction."""
#         return Vector3d(self.x - vec.getX(),
#                        self.y - vec.getY(),
#                        self.z - vec.getZ())

#     def __isub__(self, vec):
#         """In-place vector subtraction."""
#         self.x -= vec.getX()
#         self.y -= vec.getY()
#         self.z -= vec.getZ()
#         return self

#     def __mul__(self, scalar):
#         """Scalar multiplication."""
#         return Vector3d(self.x * scalar,
#                        self.y * scalar,
#                        self.z * scalar)

#     def __rmul__(self, scalar):
#         """Right scalar multiplication."""
#         return self.__mul__(scalar)

#     def __imul__(self, scalar):
#         """In-place scalar multiplication."""
#         self.x *= scalar
#         self.y *= scalar
#         self.z *= scalar
#         return self

#     def __truediv__(self, scalar):
#         """Vector division by scalar."""
#         if abs(scalar) < self.EPSILON:
#             raise ValueError("Division by zero")
#         return Vector3d(self.x / scalar,
#                        self.y / scalar,
#                        self.z / scalar)

#     def __itruediv__(self, scalar):
#         """In-place vector division by scalar."""
#         if abs(scalar) < self.EPSILON:
#             raise ValueError("Division by zero")
#         self.x /= scalar
#         self.y /= scalar
#         self.z /= scalar
#         return self

#     def __neg__(self):
#         """Vector negation."""
#         return Vector3d(-self.x, -self.y, -self.z)

#     def __eq__(self, other):
#         """Vector equality comparison (within epsilon)."""
#         if not isinstance(other, Vector3d):
#             return False
#         return (abs(self.x - other.x) < self.EPSILON and
#                 abs(self.y - other.y) < self.EPSILON and
#                 abs(self.z - other.z) < self.EPSILON)

#     def __ne__(self, other):
#         """Vector inequality comparison."""
#         return not self.__eq__(other)
#     def clamp(self, min_val=0.0, max_val=1.0):
#         """
#         Clamp vector components between min_val and max_val.
#         Default clamps between 0 and 1 for color calculations.
    
#         Args:
#             min_val (float): Minimum value (default 0.0)
#             max_val (float): Maximum value (default 1.0)
        
#         Returns:
#             Vector3d: A new vector with clamped components
#         """
#         return Vector3d(
#             min(max_val, max(min_val, self.x)),
#             min(max_val, max(min_val, self.y)),
#             min(max_val, max(min_val, self.z))
#         )

import math

class Vector3d:
    """
    A 3D vector class with methods for common vector operations.
    """
    def __init__(self, x, y, z):
        """Initialize a vector with x, y, z components."""
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def getX(self):
        """Get x component."""
        return self.x
        
    def getY(self):
        """Get y component."""
        return self.y
        
    def getZ(self):
        """Get z component."""
        return self.z

    def dot(self, other):
        """Calculate dot product with another vector."""
        return (self.x * other.x + 
                self.y * other.y + 
                self.z * other.z)

    def cross(self, other):
        """Calculate cross product with another vector."""
        return Vector3d(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self):
        """Calculate vector length."""
        return math.sqrt(self.dot(self))

    def squared_length(self):
        """Calculate squared vector length (faster than length)."""
        return self.dot(self)

    def normalize(self):
        """Return a normalized copy of the vector."""
        length = self.length()
        if length > 0:
            return Vector3d(
                self.x / length,
                self.y / length,
                self.z / length
            )
        return Vector3d(0, 0, 0)

    def normalized(self):
        """Alias for normalize() to match some APIs."""
        return self.normalize()

    def clamp(self, min_val=0.0, max_val=1.0):
        """Clamp vector components between min and max values."""
        return Vector3d(
            min(max_val, max(min_val, self.x)),
            min(max_val, max(min_val, self.y)),
            min(max_val, max(min_val, self.z))
        )

    def reflect(self, normal):
        """Reflect this vector around a normal vector."""
        return self - normal * 2 * self.dot(normal)

    # Arithmetic operations
    def __add__(self, other):
        """Vector addition."""
        return Vector3d(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        """Vector subtraction."""
        return Vector3d(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )

    def __mul__(self, other):
        """Multiplication by scalar or vector."""
        if isinstance(other, (int, float)):
            return Vector3d(
                self.x * other,
                self.y * other,
                self.z * other
            )
        return Vector3d(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z
        )

    def __rmul__(self, other):
        """Right multiplication by scalar."""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Division by scalar."""
        if isinstance(other, (int, float)):
            if other == 0:
                raise ValueError("Division by zero")
            inv = 1.0 / other
            return Vector3d(
                self.x * inv,
                self.y * inv,
                self.z * inv
            )
        raise TypeError("Unsupported operand type")

    def __neg__(self):
        """Vector negation."""
        return Vector3d(-self.x, -self.y, -self.z)

    # Comparison operations
    def __eq__(self, other):
        """Vector equality."""
        if not isinstance(other, Vector3d):
            return False
        return (abs(self.x - other.x) < 1e-9 and
                abs(self.y - other.y) < 1e-9 and
                abs(self.z - other.z) < 1e-9)

    def __ne__(self, other):
        """Vector inequality."""
        return not self.__eq__(other)

    # String representations
    def __str__(self):
        """String representation."""
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        """Detailed string representation."""
        return f"Vector3d({self.x}, {self.y}, {self.z})"

    # Utility methods
    def to_tuple(self):
        """Convert to tuple."""
        return (self.x, self.y, self.z)

    def copy(self):
        """Create a copy of this vector."""
        return Vector3d(self.x, self.y, self.z)

    @staticmethod
    def zero():
        """Return a zero vector."""
        return Vector3d(0, 0, 0)

    @staticmethod
    def one():
        """Return a vector of ones."""
        return Vector3d(1, 1, 1)

    @staticmethod
    def up():
        """Return an up vector."""
        return Vector3d(0, 1, 0)

    @staticmethod
    def right():
        """Return a right vector."""
        return Vector3d(1, 0, 0)

    @staticmethod
    def forward():
        """Return a forward vector."""
        return Vector3d(0, 0, 1)