# 🎯 Complete Usage Guide

## Getting Started in 5 Minutes

### Step 1: Installation
```bash
cd /Users/ramya/Desktop/Ramya/UF\ Sem3/AML2/AML-2-Final-project
source aml2/bin/activate  # Use your existing virtual environment
pip install trimesh mapbox-earcut  # Install remaining dependencies
```

### Step 2: Run Quick Demo
```bash
python examples/quickstart.py
```

Expected output: A 3D model generated in `models/quickstart_demo.glb`

### Step 3: Launch Web Interface
```bash
cd src
python app.py
```

Visit `http://localhost:7860` in your browser.

## 📖 Detailed Usage

### Option 1: Web Interface (Recommended for Most Users)

1. **Start the Application**
   ```bash
   cd src
   python app.py
   ```

2. **Get Sample Data**
   - Click "📄 Download Sample JSON" button
   - Save the generated file

3. **Upload and Convert**
   - Click "Upload Floor Plan" and select your JSON file
   - Click "🚀 Generate 3D Model"
   - View the interactive 3D preview

4. **Download Result**
   - Right-click the 3D model
   - Select "Save As..." to download GLB file

### Option 2: Programmatic Usage

```python
from builder import HouseBuilder
import json

# Load your floor plan
with open('my_floorplan.json', 'r') as f:
    floor_plan = json.load(f)

# Initialize builder
builder = HouseBuilder(
    wall_thickness=0.1,  # 10cm walls
    wall_height=2.5,     # 2.5m ceiling height
    floor_offset=-0.05   # Floor slightly below ground
)

# Generate 3D model
scene = builder.process_floorplan(floor_plan)

# Export to GLB
builder.export_to_glb(scene, 'output.glb')
```

### Option 3: Command Line Script

Create `convert.py`:
```python
#!/usr/bin/env python3
import sys
from builder import HouseBuilder
import json

if len(sys.argv) != 3:
    print("Usage: python convert.py input.json output.glb")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

builder = HouseBuilder()
scene = builder.process_floorplan(data)
builder.export_to_glb(scene, sys.argv[2])
print(f"✅ Created {sys.argv[2]}")
```

Usage:
```bash
python convert.py floorplan.json model.glb
```

## 🏗️ Creating Floor Plans

### Basic Structure
```json
{
  "walls": [
    [[x1, y1], [x2, y2]],
    [[x3, y3], [x4, y4]]
  ]
}
```

### Example 1: Simple Room (5m × 5m)
```json
{
  "walls": [
    [[0, 0], [0, 5]],     // Left wall
    [[0, 5], [5, 5]],     // Top wall
    [[5, 5], [5, 0]],     // Right wall
    [[5, 0], [0, 0]]      // Bottom wall
  ]
}
```

### Example 2: Two Rooms with Divider
```json
{
  "walls": [
    [[0, 0], [0, 5]],
    [[0, 5], [10, 5]],
    [[10, 5], [10, 0]],
    [[10, 0], [0, 0]],
    [[5, 0], [5, 5]]      // Middle dividing wall
  ]
}
```

### Example 3: L-Shaped House
```json
{
  "walls": [
    // Main section (6m × 8m)
    [[0, 0], [0, 8]],
    [[0, 8], [6, 8]],
    [[6, 8], [6, 4]],
    
    // Extension (4m × 4m)
    [[6, 4], [10, 4]],
    [[10, 4], [10, 0]],
    [[10, 0], [0, 0]],
    
    // Interior walls
    [[0, 4], [6, 4]],
    [[3, 0], [3, 4]]
  ]
}
```

### Tips for Creating Floor Plans

1. **Use Consistent Units**
   - Typically meters, but any unit works
   - Keep coordinates consistent throughout

2. **Close Your Perimeter**
   - Ensure outer walls form a closed loop
   - End point of last wall should connect to start of first

3. **Interior Walls**
   - Add after defining perimeter
   - Should connect to perimeter or other interior walls

4. **Coordinate System**
   - Origin (0, 0) is bottom-left
   - X increases rightward
   - Y increases upward

5. **Wall Order**
   - Define perimeter first (clockwise or counter-clockwise)
   - Then add interior divisions

## 🎨 Customization Options

### Adjusting Wall Parameters

```python
builder = HouseBuilder(
    wall_thickness=0.2,   # Thicker walls (20cm)
    wall_height=3.5,      # Higher ceilings (3.5m)
    floor_offset=-0.1     # Lower floor
)
```

**Common Presets:**

```python
# Residential (Standard)
HouseBuilder(wall_thickness=0.15, wall_height=2.7)

# Commercial (High Ceiling)
HouseBuilder(wall_thickness=0.2, wall_height=4.0)

# Apartment (Thin Walls)
HouseBuilder(wall_thickness=0.1, wall_height=2.5)

# Warehouse (Industrial)
HouseBuilder(wall_thickness=0.25, wall_height=6.0)
```

### Modifying UI Appearance

Edit `app.py`, find the `custom_css` variable:

```python
custom_css = """
.header {
    background: linear-gradient(135deg, #your-color1, #your-color2);
    /* ... */
}
"""
```

## 📤 Exporting and Using 3D Models

### GLB Format
- **Full Name**: GL Transmission Format Binary
- **Standard**: Khronos Group (OpenGL creators)
- **Support**: Universal (all major 3D software)

### Opening GLB Files

**Online Viewers:**
- [gltf-viewer.donmccurdy.com](https://gltf-viewer.donmccurdy.com/)
- [sandbox.babylonjs.com](https://sandbox.babylonjs.com/)

**Desktop Software:**
- **Windows**: 3D Viewer (built-in), Paint 3D
- **macOS**: Preview, Quick Look (Space bar)
- **Cross-platform**: Blender (free), Autodesk Viewer

### Using in Web Pages

```html
<!-- Using Three.js -->
<script src="https://cdn.jsdelivr.net/npm/three@0.150.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/loaders/GLTFLoader.js"></script>

<script>
const loader = new THREE.GLTFLoader();
loader.load('your_model.glb', (gltf) => {
    scene.add(gltf.scene);
});
</script>
```

### Converting to Other Formats

Using Blender:
```python
# In Blender Python console
import bpy

# Import GLB
bpy.ops.import_scene.gltf(filepath='model.glb')

# Export as OBJ
bpy.ops.export_scene.obj(filepath='model.obj')

# Export as FBX
bpy.ops.export_scene.fbx(filepath='model.fbx')
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### "Import Error: No module named 'trimesh'"
```bash
# Solution: Install dependencies
pip install trimesh mapbox-earcut shapely gradio
```

#### "ValueError: No available triangulation engine"
```bash
# Solution: Install triangulation engine
pip install mapbox-earcut
```

#### "JSON Decode Error"
```
Problem: Invalid JSON syntax
Solution: Validate JSON at jsonlint.com before uploading
```

#### "Wall must have exactly 2 points"
```json
// ❌ Wrong: Only one point
{"walls": [[[0, 0]]]}

// ✅ Correct: Two points
{"walls": [[[0, 0], [5, 0]]]}
```

#### Model Appears Too Small/Large
```python
# Adjust scale by changing coordinates
# Original: 5m × 5m room
{"walls": [[[0, 0], [0, 5]], ...]}

# Scaled: 10m × 10m room
{"walls": [[[0, 0], [0, 10]], ...]}
```

#### Walls Not Connecting Properly
```
Problem: Gaps in floor plan
Solution: Ensure coordinates match exactly

❌ Wrong:
[[5.0, 0.0], [5.0, 5.0]]  // First wall ends at (5, 5)
[[5.1, 5.0], [0.0, 5.0]]  // Second wall starts at (5.1, 5) - gap!

✅ Correct:
[[5.0, 0.0], [5.0, 5.0]]
[[5.0, 5.0], [0.0, 5.0]]  // Matches exactly
```

### Performance Issues

**Large Floor Plans (100+ walls)**
```python
# Process in batches
def process_large_floorplan(data, batch_size=20):
    scenes = []
    walls = data["walls"]
    
    for i in range(0, len(walls), batch_size):
        batch = {"walls": walls[i:i+batch_size]}
        scene = builder.process_floorplan(batch)
        scenes.append(scene)
    
    # Combine scenes
    final_scene = trimesh.Scene()
    for scene in scenes:
        final_scene.add_geometry(scene.geometry)
    
    return final_scene
```

## 📊 Advanced Examples

### Multi-Room House
```json
{
  "walls": [
    // Outer perimeter (15m × 10m)
    [[0, 0], [0, 10]],
    [[0, 10], [15, 10]],
    [[15, 10], [15, 0]],
    [[15, 0], [0, 0]],
    
    // Vertical corridor (center)
    [[7, 0], [7, 10]],
    
    // Horizontal divisions (left side)
    [[0, 5], [7, 5]],
    
    // Horizontal divisions (right side)
    [[7, 3.33], [15, 3.33]],
    [[7, 6.66], [15, 6.66]]
  ]
}
```

Result: 6 rooms (3 on each side)

### Batch Processing Script
```python
import os
import json
from builder import HouseBuilder

def batch_convert(input_dir, output_dir):
    """Convert all JSON files in a directory to GLB."""
    
    builder = HouseBuilder()
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(
                output_dir, 
                filename.replace('.json', '.glb')
            )
            
            try:
                with open(input_path, 'r') as f:
                    data = json.load(f)
                
                scene = builder.process_floorplan(data)
                builder.export_to_glb(scene, output_path)
                print(f"✅ {filename} → {output_path}")
                
            except Exception as e:
                print(f"❌ {filename}: {e}")

# Usage
batch_convert('floor_plans/', 'models/')
```

## 🎓 Best Practices

1. **Always Validate JSON**
   - Use online validators before uploading
   - Check for trailing commas

2. **Keep Coordinates Simple**
   - Use whole numbers when possible
   - Align walls to grid (e.g., 5m increments)

3. **Test Incrementally**
   - Start with perimeter only
   - Add interior walls one at a time
   - Verify each addition works

4. **Document Your Floor Plans**
   ```json
   {
     "_comment": "Ground floor - 3 bedroom house",
     "walls": [...]
   }
   ```

5. **Use Consistent Naming**
   ```
   house_ground_floor.json
   house_first_floor.json
   house_roof.json
   ```

## 🚀 Next Steps

After mastering the basics:

1. **Experiment with Complex Layouts**
   - Try circular rooms (approximate with many short walls)
   - Create multi-wing buildings
   - Design maze-like structures

2. **Integrate with Other Tools**
   - Export to Blender for texturing
   - Import to Unity/Unreal for games
   - Use in architectural visualization

3. **Extend the Code**
   - Add door/window cutouts
   - Implement roof generation
   - Create multi-story buildings

4. **Contribute**
   - Report bugs on GitHub
   - Suggest new features
   - Share your floor plans

---

**Need Help?** Check the `docs/ARCHITECTURE.md` for technical details or `docs/PROJECT_README.md` for project overview.
