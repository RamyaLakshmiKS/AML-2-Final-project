"""
3D Floor Plan Converter - Web Application

This module provides a Gradio-based web interface for converting 2D floor plans
(JSON format) into interactive 3D models (GLB format).

Author: Senior Python Engineer
Purpose: User-friendly interface for the HouseBuilder engine
"""

import json
import os
import sys
import tempfile
from typing import Optional, Tuple
import gradio as gr

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from builder import HouseBuilder


# Sample floor plan data for demonstration purposes
SAMPLE_FLOOR_PLAN = {
    "walls": [
        # Outer perimeter walls forming a rectangular room
        [[0.0, 0.0], [0.0, 5.0]],      # Left wall
        [[0.0, 5.0], [5.0, 5.0]],      # Top wall
        [[5.0, 5.0], [5.0, 0.0]],      # Right wall
        [[5.0, 0.0], [0.0, 0.0]],      # Bottom wall
        
        # Interior wall creating two rooms
        [[2.5, 0.0], [2.5, 3.0]],      # Dividing wall
    ]
}


def generate_sample_json() -> str:
    """
    Generate a sample JSON file for testing purposes.
    
    Creates a temporary JSON file containing a simple floor plan that users
    can download and use to test the application without external data.
    
    Returns:
        Path to the generated sample JSON file
    """
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(
        mode='w', 
        suffix='.json', 
        delete=False,
        prefix='sample_floorplan_'
    )
    
    # Write the sample data
    json.dump(SAMPLE_FLOOR_PLAN, temp_file, indent=2)
    temp_file.close()
    
    return temp_file.name


def generate_template_json(template: str) -> Tuple[str, str]:
    """
    Generate a floor plan from a predefined template.
    
    Args:
        template: Template name ('1bhk', '2bhk', '3bhk', 'villa', 'penthouse')
    
    Returns:
        Tuple of (file_path, status_message)
    """
    # Load template from examples directory
    template_map = {
        "1bhk": "apartment_1bhk.json",
        "2bhk": "apartment_2bhk.json",
        "3bhk": "apartment_3bhk.json",
        "villa": "house_villa.json",
        "penthouse": "apartment_3bhk.json"  # Using 3bhk as fallback
    }
    
    try:
        # Get the template filename
        template_filename = template_map.get(template.lower(), "apartment_2bhk.json")
        template_path = os.path.join(
            os.path.dirname(__file__),
            "../examples",
            template_filename
        )
        
        # Load the template file
        with open(template_path, 'r') as f:
            floor_plan = json.load(f)
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            prefix=f'{template}_'
        )
        
        json.dump(floor_plan, temp_file, indent=2)
        temp_file.close()
        
        plan_name = floor_plan.get('name', template)
        total_area = floor_plan.get('total_area', 0)
        room_count = len(floor_plan.get('rooms', {}))
        
        status_msg = (
            f"✅ Loaded {plan_name}\n"
            f"📐 Total Area: {total_area:.2f} sq.m\n"
            f"🏠 Rooms: {room_count}"
        )
        
        return temp_file.name, status_msg
        
    except Exception as e:
        raise gr.Error(f"Error loading template: {str(e)}. Please check that example files exist.")


def process_floor_plan(uploaded_file: Optional[gr.File], custom_bedroom_color: Optional[str] = None, 
                       custom_bathroom_color: Optional[str] = None, custom_kitchen_color: Optional[str] = None,
                       custom_livingroom_color: Optional[str] = None) -> Tuple[Optional[str], str, str]:
    """
    Process an uploaded JSON floor plan and generate a 3D model with optional room colors.
    
    This function serves as the main processing pipeline for the Gradio interface.
    It validates the input, invokes the HouseBuilder, and returns the 3D model
    along with status information and room details.
    
    Args:
        uploaded_file: A Gradio File object containing the uploaded JSON
        custom_bedroom_color: Hex color for bedrooms (e.g., "#FF8080")
        custom_bathroom_color: Hex color for bathrooms
        custom_kitchen_color: Hex color for kitchens
        custom_livingroom_color: Hex color for living rooms
        
    Returns:
        A tuple of (glb_file_path, status_message, room_details)
        
    Raises:
        gr.Error: For user-facing errors (malformed JSON, missing data, etc.)
    """
    # Validate that a file was uploaded
    if uploaded_file is None:
        raise gr.Error("Please upload a JSON file to continue.")
    
    try:
        # Read and parse the JSON file
        with open(uploaded_file.name, 'r') as f:
            json_data = json.load(f)
        
        # Validate the structure
        if "walls" not in json_data:
            raise gr.Error(
                "Invalid JSON format: Missing 'walls' key. "
                "Expected format: {\"walls\": [[[x1, y1], [x2, y2]], ...]}"
            )
        
        if not isinstance(json_data["walls"], list):
            raise gr.Error(
                "Invalid JSON format: 'walls' must be a list of wall coordinates."
            )
        
        if len(json_data["walls"]) == 0:
            raise gr.Error(
                "Invalid JSON format: 'walls' list is empty. "
                "Please provide at least one wall."
            )
        
        # Build custom colors dictionary if provided
        custom_colors = {}
        def hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
            """Convert hex color to RGB tuple (0-1 range)."""
            if not hex_color:
                return None
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
        
        if custom_bedroom_color:
            custom_colors["bedroom"] = hex_to_rgb(custom_bedroom_color)
            custom_colors["master_bedroom"] = hex_to_rgb(custom_bedroom_color)
        
        if custom_bathroom_color:
            custom_colors["bathroom"] = hex_to_rgb(custom_bathroom_color)
            custom_colors["toilet"] = hex_to_rgb(custom_bathroom_color)
        
        if custom_kitchen_color:
            custom_colors["kitchen"] = hex_to_rgb(custom_kitchen_color)
        
        if custom_livingroom_color:
            custom_colors["living_room"] = hex_to_rgb(custom_livingroom_color)
        
        # Initialize the builder with custom colors
        builder = HouseBuilder(
            wall_thickness=0.1,
            wall_height=2.5,
            floor_offset=-0.05,
            custom_colors=custom_colors if custom_colors else None
        )
        
        # Process the floor plan
        scene = builder.process_floorplan(json_data, use_room_colors=True)
        
        # Export to a temporary GLB file
        output_file = tempfile.NamedTemporaryFile(
            suffix='.glb', 
            delete=False,
            prefix='floorplan_3d_'
        )
        output_file.close()
        
        builder.export_to_glb(scene, output_file.name)
        
        # Generate success message
        wall_count = len(json_data["walls"])
        plan_name = json_data.get("name", "Floor Plan")
        plan_desc = json_data.get("description", "")
        total_area = json_data.get("total_area", 0)
        
        status_message = (
            f"✅ Successfully generated 3D model!\n"
            f"📋 Plan: {plan_name}\n"
            f"📊 Processed {wall_count} wall{'s' if wall_count != 1 else ''}\n"
            f"🎨 Room-based coloring applied\n"
            f"📦 Output format: GLB (compatible with all 3D viewers)"
        )
        
        if plan_desc:
            status_message += f"\n📝 {plan_desc}"
        
        # Generate room details
        room_details = ""
        if "rooms" in json_data:
            room_details = "📐 Room Details:\n" + "-" * 35 + "\n\n"
            total_room_area = 0
            
            for room_id, room_info in json_data["rooms"].items():
                name = room_info.get("name", "Room")
                area = room_info.get("area", 0)
                room_type = room_info.get("type", "")
                dimensions = room_info.get("dimensions", [0, 0])
                
                # Get color for this room type
                color = builder.get_color_for_room_type(room_type) if room_type else None
                color_hex = ""
                if color:
                    color_hex = f" [Color: #{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}]"
                
                room_details += f"🏠 {name}{color_hex}\n"
                if room_type:
                    room_details += f"   Type: {room_type}\n"
                room_details += f"   Dimensions: {dimensions[0]:.2f}m × {dimensions[1]:.2f}m\n"
                room_details += f"   Area: {area:.2f} sq.m\n\n"
                total_room_area += area
            
            room_details += "-" * 35 + "\n"
            room_details += f"Total Room Area: {total_room_area:.2f} sq.m"
        
        if total_area > 0:
            room_details += f"\n\n📏 Total Plan Area: {total_area:.2f} sq.m"
        
        return output_file.name, status_message, room_details
        
    except json.JSONDecodeError as e:
        raise gr.Error(
            f"Invalid JSON file: {str(e)}\n"
            "Please ensure your file contains valid JSON syntax."
        )
    
    except ValueError as e:
        raise gr.Error(f"Data validation error: {str(e)}")
    
    except Exception as e:
        raise gr.Error(
            f"An unexpected error occurred: {str(e)}\n"
            "Please check your input data and try again."
        )


def create_interface() -> gr.Blocks:
    """
    Create and configure the Gradio web interface.
    
    Builds a professional-looking UI with file upload, template selection,
    3D visualization, and comprehensive error handling.
    
    Returns:
        A configured Gradio Blocks interface
    """
    
    interface = gr.Blocks(title="3D Floor Plan Converter")
    
    with interface:
        
        # Header section
        with gr.Row():
            with gr.Column():
                gr.HTML(
                    """
                    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 20px;">
                        <h1>🏗️ 3D Floor Plan Converter</h1>
                        <p style="font-size: 1.1em; margin-top: 10px;">
                            Transform 2D floor plans into interactive 3D models with room details
                        </p>
                    </div>
                    """
                )
        
        # Main content area
        with gr.Row():
            # Left column: Input controls
            with gr.Column(scale=1):
                gr.Markdown("### 📋 Quick Templates")
                
                # Template buttons
                with gr.Row():
                    btn_1bhk = gr.Button("1 BHK", scale=1, variant="secondary", size="sm")
                    btn_2bhk = gr.Button("2 BHK", scale=1, variant="secondary", size="sm")
                
                with gr.Row():
                    btn_3bhk = gr.Button("3 BHK", scale=1, variant="secondary", size="sm")
                    btn_villa = gr.Button("Villa", scale=1, variant="secondary", size="sm")
                
                with gr.Row():
                    btn_penthouse = gr.Button("Penthouse", scale=1, variant="secondary", size="sm")
                
                gr.Markdown("---")
                gr.Markdown("### 🎨 Room Colors")
                gr.Markdown(
                    "Customize colors for different room types"
                )
                
                color_bedroom = gr.Textbox(
                    label="Bedroom Color",
                    placeholder="#FF8080",
                    value="#FF8080",
                    info="Hex color code (e.g., #FF8080)"
                )
                
                color_bathroom = gr.Textbox(
                    label="Bathroom Color",
                    placeholder="#70E8FF",
                    value="#70E8FF",
                    info="Hex color code (e.g., #70E8FF)"
                )
                
                color_kitchen = gr.Textbox(
                    label="Kitchen Color",
                    placeholder="#FFFF70",
                    value="#FFFF70",
                    info="Hex color code (e.g., #FFFF70)"
                )
                
                color_livingroom = gr.Textbox(
                    label="Living Room Color",
                    placeholder="#D9FFD9",
                    value="#D9FFD9",
                    info="Hex color code (e.g., #D9FFD9)"
                )
                
                gr.Markdown("---")
                gr.Markdown(
                    "Upload a custom JSON file or use templates above."
                )
                
                # File uploader
                file_input = gr.File(
                    label="JSON Floor Plan",
                    file_types=[".json"],
                    type="filepath"
                )
                
                # Sample file download button
                sample_button = gr.Button(
                    "📄 Download Sample JSON",
                    variant="secondary",
                    size="sm"
                )
                sample_file_output = gr.File(
                    label="Sample File",
                    visible=False
                )
                
                # Process button
                process_button = gr.Button(
                    "🚀 Generate 3D Model",
                    variant="primary",
                    size="lg"
                )
                
                # Status output
                status_output = gr.Textbox(
                    label="Status",
                    placeholder="Upload a file and click 'Generate' to start...",
                    lines=3,
                    interactive=False
                )
            
            # Right column: 3D viewer and room details
            with gr.Column(scale=2):
                gr.Markdown("### 🎨 3D Preview")
                model_output = gr.Model3D(
                    label="Interactive 3D Model",
                    height=500,
                    clear_color=[0.95, 0.95, 0.95, 1.0]
                )
                
                gr.Markdown("### 📐 Room Analysis")
                room_details_output = gr.Textbox(
                    label="Room Details",
                    placeholder="Room information will appear here...",
                    lines=8,
                    interactive=False,
                    show_label=True
                )
        
        # Instructions section
        with gr.Row():
            with gr.Column():
                gr.Markdown(
                    """
                    ### 📋 JSON Format Guide
                    
                    Your custom JSON should follow this structure:
                    
                    ```json
{
  "name": "Floor Plan Name",
  "description": "Optional description",
  "total_area": 850,
  "rooms": {
    "hall": {
      "name": "Living Room",
      "type": "living_room",
      "dimensions": [5.0, 4.5],
      "area": 22.5,
      "position": [0, 0]
    }
  },
  "walls": [
    [[x1, y1], [x2, y2]],
    [[x3, y3], [x4, y4]]
  ]
}
                    ```
                    
                    **Room Types**: bedroom, kitchen, toilet, hall, balcony, dining, office, garage, patio, garden, etc.
                    """
                )
        
        # Hidden file to store template data
        template_file = gr.File(visible=False)
        
        # Event handlers
        
        # Template buttons
        def load_template(template_name: str) -> Tuple[str, str]:
            file_path, status = generate_template_json(template_name)
            return file_path, status
        
        btn_1bhk.click(fn=lambda: load_template("1bhk"), outputs=[file_input, status_output])
        btn_2bhk.click(fn=lambda: load_template("2bhk"), outputs=[file_input, status_output])
        btn_3bhk.click(fn=lambda: load_template("3bhk"), outputs=[file_input, status_output])
        btn_villa.click(fn=lambda: load_template("villa"), outputs=[file_input, status_output])
        btn_penthouse.click(fn=lambda: load_template("penthouse"), outputs=[file_input, status_output])
        
        # Sample file generation
        sample_button.click(
            fn=generate_sample_json,
            inputs=None,
            outputs=sample_file_output
        )
        
        # Main processing pipeline
        process_button.click(
            fn=process_floor_plan,
            inputs=[file_input, color_bedroom, color_bathroom, color_kitchen, color_livingroom],
            outputs=[model_output, status_output, room_details_output]
        )
    
    return interface


def main() -> None:
    """
    Launch the Gradio web application.
    
    Starts the web server and makes the interface accessible via browser.
    """
    interface = create_interface()
    
    interface.launch(
        server_name="0.0.0.0",  # Allow external connections
        server_port=7860,        # Default Gradio port
        share=False,             # Set to True for public sharing
        show_error=True          # Display detailed errors in UI
    )


if __name__ == "__main__":
    main()
