import time
import os
from PIL import Image as PILImage
from image import Image
from constants import *
from vector3d import Vector3d
from camera import Camera

def format_time(seconds):
    """Format render time nicely."""
    if seconds >= 3600:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours}h {minutes}m {seconds}s"
    elif seconds >= 60:
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"

def create_scene_description(t):
    """Create descriptive scene name based on animation phase."""
    if t < 0.33:
        return "Opening"
    elif t < 0.66:
        return "MainDance"
    else:
        return "Finale"

def render_frame(frame_num, total_frames):
    """Render a single frame."""
    t = frame_num / total_frames
    
    # Initialize camera
    camera = Camera(
        lookFrom=Vector3d(0, 3, 8),
        lookAt=Vector3d(0, 0, -2),
        vUp=Vector3d(0, 1, 0),
        vfov=60.0,
        aspect=CAMERA_ASPECT
    )
    
    # Create and render image
    image = Image(camera)
    image.createAnimatedScene(t)
    
    # Generate descriptive filename
    scene_desc = create_scene_description(t)
    filename = f"frame_{frame_num:04d}_{scene_desc}.ppm"
    
    # Save frame
    image.renderFrame(filename)
    
    return frame_num

def convert_to_png(input_folder="frames", output_folder="frames_png"):
    """Convert all PPM files to PNG format."""
    print("\nConverting frames to PNG...")
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    ppm_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.ppm')])
    total = len(ppm_files)
    
    for i, filename in enumerate(ppm_files, 1):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace('.ppm', '.png'))
        
        try:
            with PILImage.open(input_path) as img:
                img.save(output_path, 'PNG')
            
            if i % 10 == 0:
                print(f"Progress: {i}/{total} frames ({(i/total)*100:.1f}%)")
                
        except Exception as e:
            print(f"Error converting {filename}: {str(e)}")

def main():
    """Main function to render all frames."""
    print("\nChristmas Sugar Plum Fairy Animation Renderer")
    print("=" * 60)
    print(f"Resolution: {IMAGE_WIDTH}x{IMAGE_HEIGHT}")
    print(f"Total frames: {TOTAL_FRAMES} ({DURATION}s at {FPS}fps)")
    print(f"Anti-aliasing: {ANTI_ALIASING_SAMPLES}x")
    print(f"Shadow samples: {SOFT_SHADOW_SAMPLES}")
    
    # Create output directories
    os.makedirs("frames", exist_ok=True)
    os.makedirs("frames_png", exist_ok=True)
    
    try:
        start_time = time.time()
        
        # Render all frames
        for frame in range(TOTAL_FRAMES):
            frame_start = time.time()
            render_frame(frame, TOTAL_FRAMES)
            
            # Show progress
            elapsed = time.time() - start_time
            estimated_total = (elapsed / (frame + 1)) * TOTAL_FRAMES
            remaining = estimated_total - elapsed
            current_fps = (frame + 1) / elapsed if elapsed > 0 else 0
            
            print(f"\rFrame {frame+1}/{TOTAL_FRAMES} "
                  f"({(frame+1)/TOTAL_FRAMES*100:.1f}%) "
                  f"@ {current_fps:.1f} fps - "
                  f"Remaining: {format_time(remaining)}", end="")
        
        # Convert to PNG
        print("\n\nConverting frames to PNG format...")
        convert_to_png()
        
        # Print completion message
        total_time = time.time() - start_time
        print("\nRendering complete!")
        print(f"Total time: {format_time(total_time)}")
        print(f"Average speed: {TOTAL_FRAMES / total_time:.1f} fps")
        
        print("\nTo create video:")
        print(f"ffmpeg -framerate {FPS} -i frames_png/frame_%04d_*.png "
              f"-c:v libx264 -pix_fmt yuv420p -crf 22 christmas_dance.mp4")
        
    except Exception as e:
        print(f"\nError during rendering: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()