"""
3D Floor Plan Converter - Web Application

This module provides a Gradio-based web interface for converting 2D floor plans
(JSON format) into interactive 3D models (GLB format).

Author: Senior Python Engineer
Purpose: User-friendly interface for the HouseBuilder engine
"""

import json
import os
import tempfile
from typing import Optional, Tuple
import gradio as gr
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


def process_floor_plan(uploaded_file: Optional[gr.File]) -> Tuple[Optional[str], str]:
    """
    Process an uploaded JSON floor plan and generate a 3D model.
    
    This function serves as the main processing pipeline for the Gradio interface.
    It validates the input, invokes the HouseBuilder, and returns the 3D model
    along with status information.
    
    Args:
        uploaded_file: A Gradio File object containing the uploaded JSON
        
    Returns:
        A tuple of (glb_file_path, status_message)
        - glb_file_path: Path to the generated GLB file, or None if error
        - status_message: Human-readable status/error message
        
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
        
        # Initialize the builder
        builder = HouseBuilder(
            wall_thickness=0.1,
            wall_height=2.5,
            floor_offset=-0.05
        )
        
        # Process the floor plan
        scene = builder.process_floorplan(json_data)
        
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
        status_message = (
            f"✅ Successfully generated 3D model!\n"
            f"📊 Processed {wall_count} wall{'s' if wall_count != 1 else ''}\n"
            f"📦 Output format: GLB (compatible with all 3D viewers)"
        )
        
        return output_file.name, status_message
        
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
    
    Builds a professional-looking UI with file upload, sample download,
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
                            Transform 2D vector floor plans into interactive 3D models
                        </p>
                    </div>
                    """
                )
        
        # Main content area
        with gr.Row():
            # Left column: Input controls
            with gr.Column(scale=1):
                gr.Markdown("### 📥 Upload Floor Plan")
                gr.Markdown(
                    "Upload a JSON file containing wall coordinates. "
                    "Don't have one? Download a sample below!"
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
            
            # Right column: 3D viewer
            with gr.Column(scale=2):
                gr.Markdown("### 🎨 3D Preview")
                model_output = gr.Model3D(
                    label="Interactive 3D Model",
                    height=500,
                    clear_color=[0.95, 0.95, 0.95, 1.0]
                )
        
        # Instructions section
        with gr.Row():
            with gr.Column():
                gr.Markdown(
                    """
                    ### 📋 Input Format
                    
                    Your JSON file should follow this structure:
                    
                    ```json
{
  "walls": [
    [[x1, y1], [x2, y2]],
    [[x3, y3], [x4, y4]]
  ]
}
                    ```
                    
                    *Each wall is defined by two coordinate pairs representing start and end points.*
                    """
                )
        
        # Event handlers
        
        # Sample file generation
        sample_button.click(
            fn=generate_sample_json,
            inputs=None,
            outputs=sample_file_output
        ).then(
            fn=lambda: gr.File(visible=True),
            inputs=None,
            outputs=sample_file_output
        )
        
        # Main processing pipeline
        process_button.click(
            fn=process_floor_plan,
            inputs=file_input,
            outputs=[model_output, status_output]
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
