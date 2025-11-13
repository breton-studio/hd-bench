#!/usr/bin/env python3
"""
Interactive 3D Bench Visualizer using Plotly
Creates browser-based 3D models with assembly/exploded view toggle
"""

import plotly.graph_objects as go
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class Panel3D:
    """3D panel for visualization"""
    name: str
    vertices: np.ndarray  # 8x3 array of corner points
    color: str
    opacity: float = 0.9


def create_box_mesh(x: float, y: float, z: float,
                    width: float, depth: float, thickness: float,
                    color: str = '#b0b0b0') -> Dict:
    """Create a box mesh for a panel"""
    # Define 8 corners
    vertices = np.array([
        [x, y, z],
        [x + width, y, z],
        [x + width, y + depth, z],
        [x, y + depth, z],
        [x, y, z + thickness],
        [x + width, y, z + thickness],
        [x + width, y + depth, z + thickness],
        [x, y + depth, z + thickness],
    ])

    # Define 12 triangles (2 per face, 6 faces)
    i = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5,  # Vertices for triangles
         0, 0, 1, 1, 4, 4, 5, 5, 2, 2, 3, 3]
    j = [1, 1, 2, 2, 3, 3, 0, 0, 5, 5, 6, 6,
         4, 4, 5, 5, 7, 7, 6, 6, 6, 6, 7, 7]
    k = [4, 2, 5, 6, 6, 7, 7, 4, 6, 7, 7, 4,
         1, 3, 0, 2, 3, 0, 1, 4, 3, 7, 0, 4]

    return {
        'x': vertices[:, 0],
        'y': vertices[:, 1],
        'z': vertices[:, 2],
        'i': i,
        'j': j,
        'k': k,
        'color': color,
        'vertices': vertices
    }


def create_concept_4_assembled() -> List[Dict]:
    """Create Concept 4 in assembled state"""
    panels = []

    # Seat: 60" x 11" x 0.125" at height 16"
    seat = create_box_mesh(0, 0, 16.0, 60.0, 11.0, 0.125, 'white')
    seat['name'] = 'Seat Panel'
    panels.append(seat)

    # Left leg: 11" x 16" x 0.25"
    left_leg = create_box_mesh(0, 0, 0, 11.0, 16.0, 0.25, 'white')
    left_leg['name'] = 'Left Leg'
    panels.append(left_leg)

    # Right leg: 11" x 16" x 0.25" at x=49"
    right_leg = create_box_mesh(49.0, 0, 0, 11.0, 16.0, 0.25, 'white')
    right_leg['name'] = 'Right Leg'
    panels.append(right_leg)

    return panels


def create_concept_4_exploded() -> List[Dict]:
    """Create Concept 4 in exploded state"""
    panels = []
    explode_offset = 8.0

    # Seat moved up
    seat = create_box_mesh(0, 0, 16.0 + explode_offset, 60.0, 11.0, 0.125, '#d4d4d4')
    seat['name'] = 'Seat Panel'
    panels.append(seat)

    # Left leg moved left
    left_leg = create_box_mesh(-explode_offset, 0, 0, 11.0, 16.0, 0.25, '#a0a0a0')
    left_leg['name'] = 'Left Leg'
    panels.append(left_leg)

    # Right leg moved right
    right_leg = create_box_mesh(49.0 + explode_offset, 0, 0, 11.0, 16.0, 0.25, 'white')
    right_leg['name'] = 'Right Leg'
    panels.append(right_leg)

    return panels


def create_concept_2_assembled() -> List[Dict]:
    """Create Concept 2 U-modules in assembled state"""
    panels = []

    for i in range(3):
        x_offset = i * 21.0
        module_color = 'white'

        # Seat top of U: 21" x 12" x 0.1" at height 17"
        seat = create_box_mesh(x_offset, 0, 17.0, 21.0, 12.0, 0.1, module_color)
        seat['name'] = f'Module {i+1} Seat'
        panels.append(seat)

        # Left wall: 3" x 12" x 14"
        left_wall = create_box_mesh(x_offset, 0, 3.0, 3.0, 12.0, 14.0, module_color)
        left_wall['name'] = f'Module {i+1} Left Wall'
        panels.append(left_wall)

        # Right wall: 3" x 12" x 14"
        right_wall = create_box_mesh(x_offset + 18.0, 0, 3.0, 3.0, 12.0, 14.0, module_color)
        right_wall['name'] = f'Module {i+1} Right Wall'
        panels.append(right_wall)

        # Bottom feet: 3" x 12" x 3"
        left_foot = create_box_mesh(x_offset, 0, 0, 3.0, 12.0, 3.0, module_color)
        left_foot['name'] = f'Module {i+1} Left Foot'
        panels.append(left_foot)

        right_foot = create_box_mesh(x_offset + 18.0, 0, 0, 3.0, 12.0, 3.0, module_color)
        right_foot['name'] = f'Module {i+1} Right Foot'
        panels.append(right_foot)

    return panels


def create_concept_2_exploded() -> List[Dict]:
    """Create Concept 2 U-modules in exploded state"""
    panels = []
    spacing = 10.0

    for i in range(3):
        x_offset = i * (21.0 + spacing)
        module_color = 'white'

        # Seat
        seat = create_box_mesh(x_offset, -spacing, 17.0 + spacing, 21.0, 12.0, 0.1, module_color)
        seat['name'] = f'Module {i+1} Seat'
        panels.append(seat)

        # Left wall
        left_wall = create_box_mesh(x_offset - spacing/2, 0, 3.0, 3.0, 12.0, 14.0, module_color)
        left_wall['name'] = f'Module {i+1} Left Wall'
        panels.append(left_wall)

        # Right wall
        right_wall = create_box_mesh(x_offset + 18.0 + spacing/2, 0, 3.0, 3.0, 12.0, 14.0, module_color)
        right_wall['name'] = f'Module {i+1} Right Wall'
        panels.append(right_wall)

        # Bottom feet
        left_foot = create_box_mesh(x_offset - spacing/2, 0, -spacing/2, 3.0, 12.0, 3.0, module_color)
        left_foot['name'] = f'Module {i+1} Left Foot'
        panels.append(left_foot)

        right_foot = create_box_mesh(x_offset + 18.0 + spacing/2, 0, -spacing/2, 3.0, 12.0, 3.0, module_color)
        right_foot['name'] = f'Module {i+1} Right Foot'
        panels.append(right_foot)

    return panels


def add_connection_lines(fig: go.Figure, panels: List[Dict], connections: List[Tuple[int, int]]):
    """Add dashed lines showing connections between panels"""
    for idx1, idx2 in connections:
        p1_center = np.mean(panels[idx1]['vertices'], axis=0)
        p2_center = np.mean(panels[idx2]['vertices'], axis=0)

        fig.add_trace(go.Scatter3d(
            x=[p1_center[0], p2_center[0]],
            y=[p1_center[1], p2_center[1]],
            z=[p1_center[2], p2_center[2]],
            mode='lines',
            line=dict(color='rgba(0, 100, 200, 0.5)', width=2, dash='dash'),
            showlegend=False,
            hoverinfo='skip'
        ))


def create_interactive_viewer(concept_name: str, assembled_panels: List[Dict],
                              exploded_panels: List[Dict], output_file: str):
    """Create interactive 3D viewer with assembly/exploded toggle"""

    fig = go.Figure()

    # Add assembled state (visible by default)
    for panel in assembled_panels:
        fig.add_trace(go.Mesh3d(
            x=panel['x'],
            y=panel['y'],
            z=panel['z'],
            i=panel['i'],
            j=panel['j'],
            k=panel['k'],
            color=panel['color'],
            opacity=1.0,
            name=panel['name'],
            visible=True,
            flatshading=False,
            lighting=dict(ambient=0.8, diffuse=0.5, specular=0.1, roughness=0.8),
            lightposition=dict(x=100, y=200, z=300),
            contour=dict(show=True, color='black', width=1)
        ))

    # Add exploded state (hidden by default)
    for panel in exploded_panels:
        fig.add_trace(go.Mesh3d(
            x=panel['x'],
            y=panel['y'],
            z=panel['z'],
            i=panel['i'],
            j=panel['j'],
            k=panel['k'],
            color=panel['color'],
            opacity=1.0,
            name=panel['name'] + ' (Exploded)',
            visible=False,
            flatshading=False,
            lighting=dict(ambient=0.8, diffuse=0.5, specular=0.1, roughness=0.8),
            lightposition=dict(x=100, y=200, z=300),
            contour=dict(show=True, color='black', width=1)
        ))

    # Add connection lines for exploded view
    if len(exploded_panels) == 3:  # Concept 4
        connections = [(0, 1), (0, 2)]  # Seat to legs
        for idx1, idx2 in connections:
            p1_center = np.mean(exploded_panels[idx1]['vertices'], axis=0)
            p2_center = np.mean(exploded_panels[idx2]['vertices'], axis=0)

            fig.add_trace(go.Scatter3d(
                x=[p1_center[0], p2_center[0]],
                y=[p1_center[1], p2_center[1]],
                z=[p1_center[2], p2_center[2]],
                mode='lines',
                line=dict(color='black', width=1, dash='dash'),
                showlegend=False,
                hoverinfo='skip',
                visible=False
            ))

    # Create toggle buttons
    n_assembled = len(assembled_panels)
    n_exploded = len(exploded_panels)
    n_lines = len(fig.data) - n_assembled - n_exploded

    # Visibility for assembled state
    assembled_visible = [True] * n_assembled + [False] * n_exploded + [False] * n_lines

    # Visibility for exploded state
    exploded_visible = [False] * n_assembled + [True] * n_exploded + [True] * n_lines

    # Update layout with buttons
    fig.update_layout(
        title=dict(
            text=f"{concept_name}",
            x=0.5,
            xanchor='center',
            font=dict(size=14, family='Arial, sans-serif', color='black')
        ),
        scene=dict(
            xaxis=dict(title='Length (inches)', backgroundcolor='white', gridcolor='black',
                      gridwidth=0.3, showbackground=True, linecolor='black', linewidth=0.5),
            yaxis=dict(title='Depth (inches)', backgroundcolor='white', gridcolor='black',
                      gridwidth=0.3, showbackground=True, linecolor='black', linewidth=0.5),
            zaxis=dict(title='Height (inches)', backgroundcolor='white', gridcolor='black',
                      gridwidth=0.3, showbackground=True, linecolor='black', linewidth=0.5),
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.5, y=1.8, z=1.2),
                center=dict(x=0, y=0, z=0)
            )
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.7,
                y=1.12,
                buttons=[
                    dict(
                        label="Assembled",
                        method="update",
                        args=[{"visible": assembled_visible}]
                    ),
                    dict(
                        label="Exploded",
                        method="update",
                        args=[{"visible": exploded_visible}]
                    )
                ],
                bgcolor='white',
                bordercolor='black',
                borderwidth=0.5,
                font=dict(size=11, family='Arial, sans-serif', color='black')
            )
        ],
        annotations=[
            dict(
                text="Left-drag: Rotate / Right-drag: Pan / Scroll: Zoom",
                showarrow=False,
                x=0.5,
                y=-0.05,
                xref="paper",
                yref="paper",
                xanchor='center',
                yanchor='top',
                font=dict(size=10, family='Arial, sans-serif', color='black')
            )
        ],
        height=800,
        showlegend=True,
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor='white',
            bordercolor='black',
            borderwidth=0.5,
            font=dict(size=10, family='Arial, sans-serif', color='black')
        ),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    # Save to HTML
    fig.write_html(output_file, config={
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['toImage'],
        'modeBarButtonsToAdd': ['hoverclosest', 'hovercompare']
    })

    return fig


def add_dimension_annotations(fig: go.Figure, concept_name: str):
    """Add dimension annotations to the 3D view"""
    if "Concept 4" in concept_name:
        # Add dimension lines for Concept 4
        # These would be added as additional Scatter3d traces
        pass


if __name__ == "__main__":
    print("Generating 3D interactive visualizations...\n")

    # Concept 4
    print("Creating Concept 4 (Slab Legs) 3D viewer...")
    c4_assembled = create_concept_4_assembled()
    c4_exploded = create_concept_4_exploded()
    create_interactive_viewer(
        "Concept 4: Thin Slab Legs",
        c4_assembled,
        c4_exploded,
        "concept-4-3d.html"
    )
    print("✓ Saved concept-4-3d.html")

    # Concept 2
    print("\nCreating Concept 2 (U-Modules) 3D viewer...")
    c2_assembled = create_concept_2_assembled()
    c2_exploded = create_concept_2_exploded()
    create_interactive_viewer(
        "Concept 2: Interlocking U-Modules",
        c2_assembled,
        c2_exploded,
        "concept-2-3d.html"
    )
    print("✓ Saved concept-2-3d.html")

    print("\n✓ 3D visualizations complete!")
    print("\nOpen the HTML files in your browser to interact with the 3D models:")
    print("  - concept-4-3d.html")
    print("  - concept-2-3d.html")
