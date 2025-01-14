import time
import os
import random
import math
from constants import *
from vector3d import Vector3d
from ray import Ray
from sphere import Sphere
from closesthit import ClosestHit
from light import Light

class Image:
    def __init__(self, camera):
        """Initialize renderer with camera."""
        self.camera = camera
        self.pixels = []
        self.scene_objects = []
        self.lights = []

    def easeInOutSine(self, t):
        """Smooth easing function for animations."""
        return -(math.cos(math.pi * t) - 1) / 2

    def bezierPoint(self, t, P0, P1, P2, P3):
        """Calculate point on cubic Bezier curve with smoothing."""
        t = self.easeInOutSine(t)
        return (P0 * (1-t)**3 + 
                P1 * 3*t*(1-t)**2 + 
                P2 * 3*t**2*(1-t) + 
                P3 * t**3)

    def createAnimatedScene(self, t):
        """Create scene with three animated spheres."""
        self.scene_objects = []
        
        # 1. Main red ornament (largest) - Bezier curve motion
        pos = self.bezierPoint(t, P0, P1, P2, P3)
        pos.y += math.sin(t * math.pi * 2) * BOUNCE_AMOUNT
        self.scene_objects.append(
            Sphere(pos, 0.5, CHRISTMAS_RED,
                  TEXTURE_TYPE_STRIPE, SHADOW_TYPE_SMOOTH)
        )
        
        # 2. Gold ornament (medium) - Circular orbital motion
        angle = t * CIRCLE_ORBIT_SPEED * math.pi * 2
        orbit_radius = CIRCLE_RADIUS + math.sin(t * math.pi * 2) * 0.2
        circle_pos = Vector3d(
            math.cos(angle) * orbit_radius,
            CIRCLE_HEIGHT + math.sin(t * CIRCLE_VERTICAL_SPEED * math.pi) * BOUNCE_AMOUNT,
            math.sin(angle) * orbit_radius - 2
        )
        self.scene_objects.append(
            Sphere(circle_pos, 0.3, GOLD,
                  TEXTURE_TYPE_STRIPE, SHADOW_TYPE_SMOOTH)
        )
        
        # 3. Silver ornament (smallest) - Second Bezier curve
        pos2 = self.bezierPoint(t, P0_2, P1_2, P2_2, P3_2)
        pos2.y += math.cos(t * math.pi * 3) * BOUNCE_AMOUNT * 0.5
        self.scene_objects.append(
            Sphere(pos2, 0.25, SILVER,
                  TEXTURE_TYPE_STRIPE, SHADOW_TYPE_SMOOTH)
        )
        
        # Ground sphere (stage)
        self.scene_objects.append(
            Sphere(Vector3d(0, -100.5, 0), 100.0, WHITE,
                  TEXTURE_TYPE_CHECKERBOARD, SHADOW_TYPE_SHARP)
        )
        
        # Animate lights
        angle = t * math.pi * 2
        light_radius = 8.0
        height_offset = math.sin(t * math.pi * 2) * 2.0
        
        self.lights = [
            Light(Vector3d(math.cos(angle) * light_radius,
                         8 + height_offset,
                         math.sin(angle) * light_radius),
                 AMBIENT_INTENSITY * 0.5,
                 DIFFUSE_INTENSITY,
                 SPECULAR_INTENSITY,
                 WARM_GOLD_LIGHT),
            
            Light(Vector3d(math.cos(angle + math.pi) * light_radius,
                         6 - height_offset,
                         math.sin(angle + math.pi) * light_radius),
                 AMBIENT_INTENSITY * 0.3,
                 DIFFUSE_INTENSITY * 0.6,
                 SPECULAR_INTENSITY * 0.8,
                 COOL_SILVER_LIGHT)
        ]

    def rayHitsSphere(self, ray, sphere, hit_record):
        """Check ray-sphere intersection and update hit record."""
        hit, t = sphere.rayIntersect(ray)
        
        if hit and t < hit_record.t:
            hit_point = ray.getPointAtParameter(t)
            normal = sphere.getNormalAt(hit_point)
            
            hit_record.update(
                t=t,
                hit_point=hit_point,
                normal=normal,
                color=sphere.getColor(),
                sphere_center=sphere.getCenter(),
                textureType=sphere.getTextureType(),
                shadowType=sphere.getShadowType()
            )
            return True
        return False

    def generateStripeTexture(self, hit_point, base_color, sphere_center):
        """Generate shimmering stripe texture."""
        stripe_color = Vector3d(1.0, 0.95, 0.8)  # Warm golden shimmer
        
        local_point = (hit_point - sphere_center).normalize()
        angle = math.atan2(local_point.z, local_point.x)
        height = local_point.y
        
        pattern = (math.sin(height * STRIPE_FREQUENCY + angle * 4) + 
                  math.sin(height * 12 - angle * 6) * 0.5)
        
        blend = (math.sin(pattern * math.pi) + 1) * 0.5
        return base_color * (1 - blend * 0.3) + stripe_color * (blend * 0.3)

    def generateCheckTexture(self, hit_point):
        """Generate checkerboard texture for stage."""
        scale = CHECKERBOARD_SCALE
        x = int(hit_point.x * scale)
        z = int(hit_point.z * scale)
        
        if (x + z) % 2 == 0:
            return Vector3d(1.0, 1.0, 0.9)  # Warm white
        return Vector3d(0.8, 0.8, 1.0)      # Cool white

    def calcBlinnPhongShading(self, ray, hit_record, light):
        """Calculate Blinn-Phong shading."""
        light_dir = (light.getPosition() - hit_record.hit_point).normalize()
        view_dir = (ray.getOrigin() - hit_record.hit_point).normalize()
        half_vector = (light_dir + view_dir).normalize()
        
        diff = max(0.0, hit_record.normal.dot(light_dir))
        spec = max(0.0, hit_record.normal.dot(half_vector)) ** SPECULAR_POWER
        
        return diff * light.diffuse + spec * light.specular

    def calcShadows(self, hit_record, light):
        """Calculate shadows with smooth transitions."""
        shadow_hits = 0
        num_samples = SOFT_SHADOW_SAMPLES if hit_record.shadowType == SHADOW_TYPE_SMOOTH else 1

        for _ in range(num_samples):
            light_pos = light.getPosition()
            
            if hit_record.shadowType == SHADOW_TYPE_SMOOTH:
                jitter_range = 0.5
                light_pos = light_pos + Vector3d(
                    random.uniform(-jitter_range, jitter_range),
                    random.uniform(-jitter_range, jitter_range),
                    random.uniform(-jitter_range, jitter_range)
                )

            shadow_origin = hit_record.hit_point + hit_record.normal * RAY_EPSILON
            shadow_dir = (light_pos - shadow_origin).normalize()
            shadow_ray = Ray(shadow_origin, shadow_dir)

            for obj in self.scene_objects:
                hit, _ = obj.rayIntersect(shadow_ray)
                if hit:
                    shadow_hits += 1
                    if hit_record.shadowType == SHADOW_TYPE_SHARP:
                        return 0.95
                    break

        if hit_record.shadowType == SHADOW_TYPE_SMOOTH:
            shadow_factor = (shadow_hits / num_samples)
            return shadow_factor * 0.9
        
        return 0.0

    def calculatePixelColor(self, ray, depth=MAX_RAY_DEPTH):
        """Calculate final pixel color with reflection and lighting."""
        if depth <= 0:
            return BACKGROUND_COLOR_BOTTOM
            
        hit_record = ClosestHit()
        has_hit = False
        
        for obj in self.scene_objects:
            if self.rayHitsSphere(ray, obj, hit_record):
                has_hit = True
                
        if has_hit:
            base_color = Vector3d(*hit_record.color) / 255.0
            
            if hit_record.textureType == TEXTURE_TYPE_STRIPE:
                base_color = self.generateStripeTexture(
                    hit_record.hit_point,
                    base_color,
                    hit_record.sphere_center
                )
            elif hit_record.textureType == TEXTURE_TYPE_CHECKERBOARD:
                base_color = self.generateCheckTexture(hit_record.hit_point)
            
            reflectivity = 0.5 if hit_record.color == GOLD else 0.3
            reflected_color = Vector3d(0, 0, 0)
            
            if reflectivity > 0 and depth > 0:
                reflect_dir = ray.reflect(hit_record.normal)
                reflect_ray = Ray(hit_record.hit_point + hit_record.normal * RAY_EPSILON,
                                reflect_dir)
                reflected_color = Vector3d(*self.calculatePixelColor(reflect_ray, depth-1)) / 255.0
            
            lit_color = Vector3d(0, 0, 0)
            for light in self.lights:
                diffuse_specular = self.calcBlinnPhongShading(ray, hit_record, light)
                shadow = self.calcShadows(hit_record, light)
                
                light_color = light.getColor()
                shadow_factor = 1.0 - shadow
                lit_color += ((base_color * diffuse_specular * shadow_factor) * 
                            light_color)
            
            final_color = lit_color * (1 - reflectivity) + reflected_color * reflectivity
            
            return (min(255, max(0, int(final_color.x * 255))),
                   min(255, max(0, int(final_color.y * 255))),
                   min(255, max(0, int(final_color.z * 255))))
        
        # Background gradient
        t = 0.5 * (ray.direction.normalize().y + 1.0)
        color = ((1.0 - t) * Vector3d(*BACKGROUND_COLOR_BOTTOM) + 
                t * Vector3d(*BACKGROUND_COLOR_TOP))
        return (int(color.x), int(color.y), int(color.z))

    def renderFrame(self, filename):
        """Render a single frame and save to file with error checking."""
        try:
            self.pixels = []
            
            # Create pixel data
            for row in range(IMAGE_HEIGHT):
                row_pixels = []
                for col in range(IMAGE_WIDTH):
                    pixel_color = Vector3d(0, 0, 0)
                    
                    for _ in range(ANTI_ALIASING_SAMPLES):
                        u = (col + random.random()) / (IMAGE_WIDTH - 1)
                        v = (row + random.random()) / (IMAGE_HEIGHT - 1)
                        ray = self.camera.getARay(u, v)
                        color = self.calculatePixelColor(ray)
                        pixel_color += Vector3d(*color)
                    
                    pixel_color = pixel_color / ANTI_ALIASING_SAMPLES
                    row_pixels.append((
                        int(max(0, min(255, pixel_color.x))),
                        int(max(0, min(255, pixel_color.y))),
                        int(max(0, min(255, pixel_color.z)))
                    ))
                
                self.pixels.append(row_pixels)
            
            # Ensure output directory exists
            os.makedirs("frames", exist_ok=True)
            file_path = os.path.join("frames", filename)
            
            # Write PPM file with strict format
            with open(file_path, "w") as f:
                # Write PPM header
                f.write("P3\n")
                f.write(f"{IMAGE_WIDTH} {IMAGE_HEIGHT}\n")
                f.write("255\n")
                
                # Write pixel data with careful formatting
                for row in reversed(self.pixels):
                    row_data = []
                    for r, g, b in row:
                        r = max(0, min(255, r))
                        g = max(0, min(255, g))
                        b = max(0, min(255, b))
                        row_data.extend([str(r), str(g), str(b)])
                    f.write(" ".join(row_data) + "\n")
                
                # Ensure file is properly written
                f.flush()
                os.fsync(f.fileno())
                
        except Exception as e:
            print(f"Error in renderFrame for {filename}: {str(e)}")
            raise