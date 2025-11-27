"""
3D House Builder Module

This module provides the core geometry engine for converting 2D floor plans 
into 3D models using computational geometry techniques.

Author: Senior Python Engineer
Purpose: Production-ready 3D model generation from vector floor plans
"""

from typing import Dict, List, Tuple, Any
import numpy as np
import trimesh
from shapely.geometry import LineString, Polygon
from shapely.ops import unary_union


class HouseBuilder:
    """
    A builder class for converting 2D floor plan data into 3D mesh models.
    
    This class handles the geometric transformation of 2D wall coordinates
    into extruded 3D meshes with proper thickness and height. It uses
    computational geometry libraries to ensure accurate spatial representation.
    
    Attributes:
        wall_thickness (float): The thickness to apply to wall lines (default: 0.1 units)
        wall_height (float): The height to extrude walls vertically (default: 2.5 units)
        floor_offset (float): The Z-offset for the floor plane (default: -0.05 units)
        room_metadata (dict): Stores room information for reference
    """
    
    def __init__(
        self, 
        wall_thickness: float = 0.1, 
        wall_height: float = 2.5,
        floor_offset: float = -0.05
    ) -> None:
        """
        Initialize the HouseBuilder with geometric parameters.
        
        Args:
            wall_thickness: Thickness to buffer wall lines (meters/units)
            wall_height: Vertical extrusion height for walls (meters/units)
            floor_offset: Vertical offset for floor positioning (meters/units)
        """
        self.wall_thickness = wall_thickness
        self.wall_height = wall_height
        self.floor_offset = floor_offset
        self.room_metadata: Dict[str, Dict[str, Any]] = {}
    
    def _create_wall_polygon(self, wall_coords: List[List[float]]) -> Polygon:
        """
        Convert a wall line segment into a 2D polygon with thickness.
        
        This method uses Shapely's buffer operation to add thickness to a line,
        creating a rectangular polygon that represents the wall's footprint.
        
        Args:
            wall_coords: A list of two [x, y] coordinate pairs defining the wall line
            
        Returns:
            A Shapely Polygon representing the wall's 2D footprint
            
        Raises:
            ValueError: If wall_coords doesn't contain exactly 2 points
        """
        if len(wall_coords) != 2:
            raise ValueError(
                f"Wall must have exactly 2 points, got {len(wall_coords)}"
            )
        
        # Create a LineString from the two points
        line = LineString(wall_coords)
        
        # Buffer the line to give it thickness (cap_style=2 creates flat ends)
        # This transforms the 1D line into a 2D rectangular polygon
        wall_polygon = line.buffer(
            self.wall_thickness / 2, 
            cap_style=2,  # Flat caps
            join_style=2  # Mitered joins
        )
        
        return wall_polygon
    
    def _extrude_wall(self, wall_polygon: Polygon) -> trimesh.Trimesh:
        """
        Extrude a 2D wall polygon into a 3D mesh.
        
        Uses trimesh's extrusion functionality to create a vertical wall
        from a 2D footprint polygon.
        
        Args:
            wall_polygon: A Shapely Polygon representing the wall's footprint
            
        Returns:
            A trimesh.Trimesh object representing the 3D wall
        """
        # Extract exterior coordinates from the polygon
        coords = np.array(wall_polygon.exterior.coords[:-1])  # Remove duplicate last point
        
        # Create a trimesh polygon and extrude it vertically
        wall_mesh = trimesh.creation.extrude_polygon(
            polygon=Polygon(coords),
            height=self.wall_height
        )
        
        return wall_mesh
    
    def _create_floor(self, wall_polygons: List[Polygon]) -> trimesh.Trimesh:
        """
        Generate a floor plane that encompasses all walls.
        
        Creates a rectangular floor mesh based on the bounding box of all walls,
        with a small margin for aesthetic purposes.
        
        Args:
            wall_polygons: List of Shapely Polygons representing all wall footprints
            
        Returns:
            A trimesh.Trimesh object representing the floor plane
        """
        # Compute the union of all wall polygons to get overall bounds
        union_poly = unary_union(wall_polygons)
        minx, miny, maxx, maxy = union_poly.bounds
        
        # Add a margin around the walls for better visualization
        margin = 0.5
        floor_vertices = np.array([
            [minx - margin, miny - margin, self.floor_offset],
            [maxx + margin, miny - margin, self.floor_offset],
            [maxx + margin, maxy + margin, self.floor_offset],
            [minx - margin, maxy + margin, self.floor_offset]
        ])
        
        # Define two triangular faces to create a rectangular floor
        floor_faces = np.array([
            [0, 1, 2],  # First triangle
            [0, 2, 3]   # Second triangle
        ])
        
        floor_mesh = trimesh.Trimesh(
            vertices=floor_vertices, 
            faces=floor_faces
        )
        
        return floor_mesh
    
    def process_floorplan(self, json_data: Dict[str, Any]) -> trimesh.Scene:
        """
        Convert a JSON floor plan specification into a 3D mesh scene.
        
        This is the main entry point for the builder. It processes the wall
        coordinates, generates 3D geometry, and assembles everything into
        a single Scene object that can be exported to GLB format.
        
        Args:
            json_data: A dictionary containing "walls" key with list of wall coordinates
                      Format: {"walls": [[[x1, y1], [x2, y2]], ...]}
        
        Returns:
            A trimesh.Scene containing all 3D meshes (walls + floor)
            
        Raises:
            ValueError: If json_data is missing "walls" key or has invalid structure
            Exception: For any geometry processing errors
        """
        # Extract room metadata if available
        self.extract_room_info(json_data)
        
        # Validate input structure
        if "walls" not in json_data:
            raise ValueError("JSON data must contain 'walls' key")
        
        walls_data = json_data["walls"]
        
        if not isinstance(walls_data, list) or len(walls_data) == 0:
            raise ValueError("'walls' must be a non-empty list")
        
        # Step 1: Convert all wall lines into 2D polygons with thickness
        wall_polygons: List[Polygon] = []
        wall_meshes: List[trimesh.Trimesh] = []
        
        for idx, wall_coords in enumerate(walls_data):
            try:
                # Create buffered polygon for this wall
                wall_polygon = self._create_wall_polygon(wall_coords)
                wall_polygons.append(wall_polygon)
                
                # Extrude the polygon into a 3D mesh
                wall_mesh = self._extrude_wall(wall_polygon)
                wall_meshes.append(wall_mesh)
                
            except Exception as e:
                raise Exception(
                    f"Error processing wall {idx} with coords {wall_coords}: {str(e)}"
                )
        
        # Step 2: Create the floor mesh
        floor_mesh = self._create_floor(wall_polygons)
        
        # Step 3: Combine all meshes into a single scene
        scene = trimesh.Scene()
        
        # Add all wall meshes
        for idx, mesh in enumerate(wall_meshes):
            scene.add_geometry(
                mesh, 
                node_name=f"wall_{idx}",
                geom_name=f"wall_{idx}"
            )
        
        # Add floor mesh
        scene.add_geometry(
            floor_mesh, 
            node_name="floor",
            geom_name="floor"
        )
        
        return scene
    
    def extract_room_info(self, json_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Extract room information from floor plan JSON.
        
        Args:
            json_data: Floor plan data containing room metadata
            
        Returns:
            Dictionary with room information (name, area, type, etc.)
        """
        rooms = {}
        
        if "rooms" in json_data:
            for room_id, room_data in json_data["rooms"].items():
                rooms[room_id] = {
                    "name": room_data.get("name", "Room"),
                    "type": room_data.get("type", "unknown"),
                    "dimensions": room_data.get("dimensions", [0, 0]),
                    "area": room_data.get("area", 0),
                    "position": room_data.get("position", [0, 0])
                }
        
        self.room_metadata = rooms
        return rooms
    
    def get_room_summary(self) -> str:
        """
        Generate a text summary of all rooms.
        
        Returns:
            Formatted string with room details
        """
        if not self.room_metadata:
            return "No room information available"
        
        summary = "Floor Plan Rooms:\n" + "=" * 40 + "\n"
        total_area = 0
        
        for room_id, info in self.room_metadata.items():
            name = info.get("name", "Unknown")
            area = info.get("area", 0)
            dimensions = info.get("dimensions", [0, 0])
            
            summary += f"\n{name}:\n"
            summary += f"  Type: {info.get('type', 'N/A')}\n"
            summary += f"  Dimensions: {dimensions[0]:.2f}m × {dimensions[1]:.2f}m\n"
            summary += f"  Area: {area:.2f} sq.m\n"
            
            total_area += area
        
        summary += "\n" + "=" * 40 + "\n"
        summary += f"Total Area: {total_area:.2f} sq.m\n"
        
        return summary
    
    def export_to_glb(self, scene: trimesh.Scene, output_path: str) -> None:
        """
        Export a trimesh Scene to GLB format.
        
        Args:
            scene: The trimesh.Scene to export
            output_path: File path for the output GLB file
        """
        scene.export(output_path, file_type='glb')
