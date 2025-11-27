"""
Quick Start Demo

This script demonstrates programmatic usage of the HouseBuilder
without the web interface.
"""

import json
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from builder import HouseBuilder


def main():
    """Generate a sample 3D floor plan programmatically."""
    
    print("🏗️ 3D Floor Plan Converter - Quick Start Demo")
    print("=" * 60)
    
    # Define a simple L-shaped floor plan
    floor_plan = {
        "walls": [
            # Main rectangle
            [[0.0, 0.0], [0.0, 8.0]],      # Left wall
            [[0.0, 8.0], [6.0, 8.0]],      # Top wall
            [[6.0, 8.0], [6.0, 4.0]],      # Right wall (partial)
            
            # L-extension
            [[6.0, 4.0], [10.0, 4.0]],     # Extension top
            [[10.0, 4.0], [10.0, 0.0]],    # Extension right
            [[10.0, 0.0], [0.0, 0.0]],     # Bottom wall
            
            # Interior walls
            [[0.0, 4.0], [6.0, 4.0]],      # Horizontal divider
            [[3.0, 0.0], [3.0, 4.0]],      # Vertical divider
        ]
    }
    
    print("\n📐 Floor Plan Configuration:")
    print(f"   - Total walls: {len(floor_plan['walls'])}")
    print(f"   - Layout: L-shaped with interior divisions")
    
    # Initialize builder with custom parameters
    builder = HouseBuilder(
        wall_thickness=0.15,    # Slightly thicker walls
        wall_height=3.0,        # Taller walls (3 meters)
        floor_offset=-0.02
    )
    
    print("\n⚙️ Builder Parameters:")
    print(f"   - Wall thickness: {builder.wall_thickness}m")
    print(f"   - Wall height: {builder.wall_height}m")
    print(f"   - Floor offset: {builder.floor_offset}m")
    
    # Process the floor plan
    print("\n🔄 Processing geometry...")
    scene = builder.process_floorplan(floor_plan)
    
    print("✅ 3D Scene generated:")
    print(f"   - Geometries: {len(scene.geometry)}")
    print(f"   - Components: {', '.join(scene.geometry.keys())}")
    
    # Calculate bounding box
    bounds = scene.bounds
    dimensions = bounds[1] - bounds[0]
    print(f"\n📏 Model Dimensions:")
    print(f"   - Width (X): {dimensions[0]:.2f}m")
    print(f"   - Depth (Y): {dimensions[1]:.2f}m")
    print(f"   - Height (Z): {dimensions[2]:.2f}m")
    
    # Export to GLB
    output_dir = os.path.join(os.path.dirname(__file__), '../models')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'quickstart_demo.glb')
    
    print(f"\n💾 Exporting to GLB...")
    builder.export_to_glb(scene, output_path)
    
    file_size = os.path.getsize(output_path)
    print(f"✅ Export complete!")
    print(f"   - File: {output_path}")
    print(f"   - Size: {file_size:,} bytes")
    
    # Also save the JSON for reference
    json_path = os.path.join(output_dir, 'quickstart_demo.json')
    with open(json_path, 'w') as f:
        json.dump(floor_plan, f, indent=2)
    
    print(f"   - JSON: {json_path}")
    
    print("\n" + "=" * 60)
    print(" Demo completed successfully!")
    print("\nNext steps:")
    print("  1. Open the GLB file in a 3D viewer")
    print("  2. Run 'python src/app.py' to launch the web interface")
    print("  3. Upload the JSON file to test the UI")
    print("=" * 60)


if __name__ == "__main__":
    main()
