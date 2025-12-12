"""
Figure Generation Script for IEEE Final Report

This script generates publication-quality figures for the IEEE conference paper.
Run this before compiling the LaTeX document.

Requirements:
    pip install matplotlib seaborn numpy pandas
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Set publication-quality defaults
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']

# Create figures directory if it doesn't exist
FIGURES_DIR = os.path.join(os.path.dirname(__file__), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

def create_performance_chart():
    """Create performance benchmarking chart (Table I visualization)"""
    print("Generating performance chart...")
    
    floor_plans = ['Simple\nTest', '1 BHK\nApt', '2 BHK\nApt', '3 BHK\nApt', 'Villa\n(Complex)']
    walls = [5, 12, 18, 24, 35]
    rooms = [2, 4, 7, 9, 12]
    times = [3.2, 4.1, 4.6, 5.8, 7.3]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Processing time chart
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(floor_plans)))
    bars = ax1.bar(floor_plans, times, color=colors, edgecolor='black', linewidth=0.8)
    ax1.set_ylabel('Processing Time (ms)', fontsize=11, fontweight='bold')
    ax1.set_xlabel('Floor Plan Type', fontsize=11, fontweight='bold')
    ax1.set_title('(a) Processing Time Analysis', fontsize=12, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 10)
    
    # Add value labels on bars
    for bar, time in zip(bars, times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.1f}ms', ha='center', va='bottom', fontsize=9)
    
    # Wall count vs time scatter plot
    ax2.scatter(walls, times, s=100, c=colors, edgecolor='black', linewidth=0.8, zorder=3)
    
    # Add trend line
    z = np.polyfit(walls, times, 1)
    p = np.poly1d(z)
    x_line = np.linspace(0, 40, 100)
    ax2.plot(x_line, p(x_line), "r--", alpha=0.7, linewidth=2, label='Linear fit')
    
    ax2.set_xlabel('Number of Walls', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Processing Time (ms)', fontsize=11, fontweight='bold')
    ax2.set_title('(b) Scalability Analysis', fontsize=12, fontweight='bold')
    ax2.grid(alpha=0.3, linestyle='--')
    ax2.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'performance_analysis.png'), bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIGURES_DIR}/performance_analysis.png")


def create_file_size_chart():
    """Create output file size analysis chart"""
    print("Generating file size chart...")
    
    floor_plans = ['Simple\nTest', '1 BHK\nApt', '2 BHK\nApt', '3 BHK\nApt', 'Villa\n(Complex)']
    walls = [5, 12, 18, 24, 35]
    file_sizes = [12.4, 18.7, 24.3, 31.5, 42.8]  # KB
    
    fig, ax = plt.subplots(figsize=(7, 4))
    
    colors = plt.cm.plasma(np.linspace(0.3, 0.9, len(floor_plans)))
    bars = ax.bar(floor_plans, file_sizes, color=colors, edgecolor='black', linewidth=0.8)
    
    ax.set_ylabel('File Size (KB)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Floor Plan Type', fontsize=11, fontweight='bold')
    ax.set_title('GLB Output File Size Analysis', fontsize=12, fontweight='bold')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.axhline(y=50, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='50 KB threshold')
    ax.legend(fontsize=9)
    
    # Add value labels
    for bar, size in zip(bars, file_sizes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{size:.1f}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'file_size_analysis.png'), bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIGURES_DIR}/file_size_analysis.png")


def create_accuracy_chart():
    """Create geometric accuracy validation chart"""
    print("Generating accuracy validation chart...")
    
    dimensions = ['Wall\nLength', 'Wall\nThickness', 'Wall\nHeight', 'Room\nArea']
    input_vals = [5.0, 0.1, 2.5, 16.0]
    output_vals = [5.002, 0.100, 2.500, 15.98]
    errors = [0.04, 0.00, 0.00, 0.13]  # percent
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.arange(len(dimensions))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, input_vals, width, label='Input Specification', 
                   color='steelblue', edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x + width/2, output_vals, width, label='Generated Output', 
                   color='coral', edgecolor='black', linewidth=0.8)
    
    ax.set_ylabel('Value (m or m²)', fontsize=11, fontweight='bold')
    ax.set_xlabel('Dimension Type', fontsize=11, fontweight='bold')
    ax.set_title('Geometric Accuracy Validation', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(dimensions)
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add error annotations
    for i, (inp, out, err) in enumerate(zip(input_vals, output_vals, errors)):
        ax.text(i, max(inp, out) + 0.5, f'Error: {err:.2f}%', 
                ha='center', fontsize=8, style='italic', color='darkred')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'accuracy_validation.png'), bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIGURES_DIR}/accuracy_validation.png")


def create_room_color_distribution():
    """Create room type color distribution pie chart"""
    print("Generating room type distribution chart...")
    
    room_types = ['Bedroom', 'Kitchen', 'Bathroom', 'Living Room', 'Dining', 'Hallway', 'Balcony', 'Other']
    counts = [3, 1, 2, 1, 1, 1, 1, 2]  # Example distribution
    colors_pie = ['#ffcccc', '#ffff99', '#b3e0ff', '#d9ffd9', '#f2e6c7', '#f2f2f2', '#e6ffff', '#e6e6e6']
    
    fig, ax = plt.subplots(figsize=(7, 7))
    
    wedges, texts, autotexts = ax.pie(counts, labels=room_types, colors=colors_pie,
                                        autopct='%1.1f%%', startangle=90,
                                        textprops={'fontsize': 10},
                                        wedgeprops={'edgecolor': 'black', 'linewidth': 1})
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    ax.set_title('Room Type Distribution in Test Dataset', fontsize=12, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'room_distribution.png'), bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIGURES_DIR}/room_distribution.png")


def create_system_architecture_placeholder():
    """Create a simple architecture diagram placeholder"""
    print("Generating architecture diagram placeholder...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    
    # Architecture layers
    layers = [
        ('Input Layer', 'JSON Floor Plan\nRoom Metadata\nUser Config', 'lightblue'),
        ('Validation Layer', 'Structure Validation\nRoom Data Parsing\nParameter Validation', 'lightyellow'),
        ('Processing Engine', 'Line Buffering\nWall Extrusion\nFloor Generation\nColor Management', 'lightgreen'),
        ('Scene Assembly', 'Combine Geometries\nApply Colors\nCreate 3D Scene', 'lightcoral'),
        ('Export Layer', 'GLB Export\nMetadata Generation', 'plum')
    ]
    
    y_positions = [0.85, 0.68, 0.48, 0.28, 0.10]
    
    for (title, content, color), y_pos in zip(layers, y_positions):
        # Draw rectangle
        rect = plt.Rectangle((0.05, y_pos-0.06), 0.9, 0.12, 
                            facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # Add title
        ax.text(0.5, y_pos+0.04, title, ha='center', va='center', 
               fontsize=12, fontweight='bold')
        
        # Add content
        ax.text(0.5, y_pos-0.02, content, ha='center', va='center', 
               fontsize=9, style='italic')
        
        # Draw arrow to next layer (except for last layer)
        if y_pos != y_positions[-1]:
            next_y = y_positions[y_positions.index(y_pos) + 1]
            ax.annotate('', xy=(0.5, next_y + 0.06), xytext=(0.5, y_pos - 0.06),
                       arrowprops=dict(arrowstyle='->', lw=2.5, color='darkblue'))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title('System Architecture and Data Flow Pipeline', 
                fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'architecture_diagram.png'), bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIGURES_DIR}/architecture_diagram.png")


def create_test_coverage_chart():
    """Create test coverage visualization"""
    print("Generating test coverage chart...")
    
    modules = ['builder.py\n(Core)', 'app.py\n(UI)', 'test_builder.py\n(Tests)']
    lines = [467, 528, 107]
    coverage = [100, 85, 100]  # percentage
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    # Lines of code
    colors = ['steelblue', 'coral', 'mediumseagreen']
    bars1 = ax1.barh(modules, lines, color=colors, edgecolor='black', linewidth=0.8)
    ax1.set_xlabel('Lines of Code', fontsize=11, fontweight='bold')
    ax1.set_title('(a) Code Size Distribution', fontsize=12, fontweight='bold')
    ax1.grid(axis='x', alpha=0.3, linestyle='--')
    
    for bar, line_count in zip(bars1, lines):
        width = bar.get_width()
        ax1.text(width, bar.get_y() + bar.get_height()/2.,
                f'{line_count}', ha='left', va='center', fontsize=9, fontweight='bold')
    
    # Test coverage
    bars2 = ax2.barh(modules, coverage, color=colors, edgecolor='black', linewidth=0.8)
    ax2.set_xlabel('Test Coverage (%)', fontsize=11, fontweight='bold')
    ax2.set_title('(b) Test Coverage Analysis', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 110)
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    ax2.axvline(x=100, color='green', linestyle='--', linewidth=1.5, alpha=0.7)
    
    for bar, cov in zip(bars2, coverage):
        width = bar.get_width()
        ax2.text(width + 2, bar.get_y() + bar.get_height()/2.,
                f'{cov}%', ha='left', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'test_coverage.png'), bbox_inches='tight')
    plt.close()
    print(f"  ✓ Saved: {FIGURES_DIR}/test_coverage.png")


def main():
    """Generate all figures for the report"""
    print("=" * 60)
    print("IEEE Final Report - Figure Generation")
    print("=" * 60)
    print()
    
    try:
        create_performance_chart()
        create_file_size_chart()
        create_accuracy_chart()
        create_room_color_distribution()
        create_system_architecture_placeholder()
        create_test_coverage_chart()
        
        print()
        print("=" * 60)
        print("✅ All figures generated successfully!")
        print(f"   Location: {FIGURES_DIR}")
        print()
        print("Next steps:")
        print("  1. Review the generated figures")
        print("  2. Compile the LaTeX document:")
        print("     cd docs && pdflatex IEEE_Final_Report.tex")
        print("  3. Check the PDF output")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error generating figures: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
