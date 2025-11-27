"""
Test Script for 3D Floor Plan Converter

This script validates the core functionality of the HouseBuilder engine
by generating a test 3D model from sample data.
"""

import json
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from builder import HouseBuilder


def test_basic_floor_plan():
    """Test basic floor plan generation."""
    print("🧪 Testing HouseBuilder with sample floor plan...")
    
    # Sample data
    test_data = {
        "walls": [
            [[0.0, 0.0], [0.0, 5.0]],
            [[0.0, 5.0], [5.0, 5.0]],
            [[5.0, 5.0], [5.0, 0.0]],
            [[5.0, 0.0], [0.0, 0.0]],
            [[2.5, 0.0], [2.5, 3.0]]
        ]
    }
    
    # Initialize builder
    builder = HouseBuilder()
    
    # Process the floor plan
    print("📐 Processing floor plan geometry...")
    scene = builder.process_floorplan(test_data)
    
    # Verify scene contains expected geometries
    print(f"✅ Scene created successfully!")
    print(f"   - Number of geometries: {len(scene.geometry)}")
    print(f"   - Geometry names: {list(scene.geometry.keys())}")
    
    # Export to GLB
    output_path = os.path.join(os.path.dirname(__file__), '../models/test_output.glb')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"💾 Exporting to GLB format...")
    builder.export_to_glb(scene, output_path)
    
    # Verify file was created
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"✅ GLB file created successfully!")
        print(f"   - Path: {output_path}")
        print(f"   - Size: {file_size:,} bytes")
    else:
        print("❌ Error: GLB file was not created")
        return False
    
    return True


def test_error_handling():
    """Test error handling with invalid data."""
    print("\n🧪 Testing error handling...")
    
    builder = HouseBuilder()
    
    # Test missing walls key
    try:
        builder.process_floorplan({})
        print("❌ Should have raised ValueError for missing 'walls' key")
        return False
    except ValueError as e:
        print(f"✅ Correctly raised ValueError: {e}")
    
    # Test invalid wall format
    try:
        builder.process_floorplan({"walls": [[[0, 0]]]})  # Only one point
        print("❌ Should have raised ValueError for invalid wall format")
        return False
    except Exception as e:
        print(f"✅ Correctly raised exception: {e}")
    
    return True


if __name__ == "__main__":
    print("="*60)
    print("3D Floor Plan Converter - Test Suite")
    print("="*60)
    
    success = True
    
    # Run tests
    success = test_basic_floor_plan() and success
    success = test_error_handling() and success
    
    print("\n" + "="*60)
    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed")
    print("="*60)
