#!/usr/bin/env python3
"""
SVG Technical Drawing Generator for Metal Bench Designs
Creates orthographic, isometric, exploded, and flat pattern views
"""

import math
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass


@dataclass
class Point3D:
    """3D point"""
    x: float
    y: float
    z: float

    def rotate_y(self, angle_rad: float) -> 'Point3D':
        """Rotate around Y axis"""
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Point3D(
            self.x * cos_a + self.z * sin_a,
            self.y,
            -self.x * sin_a + self.z * cos_a
        )

    def rotate_x(self, angle_rad: float) -> 'Point3D':
        """Rotate around X axis"""
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        return Point3D(
            self.x,
            self.y * cos_a - self.z * sin_a,
            self.y * sin_a + self.z * cos_a
        )

    def translate(self, dx: float, dy: float, dz: float) -> 'Point3D':
        """Translate point"""
        return Point3D(self.x + dx, self.y + dy, self.z + dz)

    def to_isometric(self, scale: float = 1.0) -> Tuple[float, float]:
        """Convert to isometric projection (30° angle)"""
        # Isometric: rotate 45° about Y, then ~35.264° about X
        p = self.rotate_y(math.radians(45))
        p = p.rotate_x(math.radians(35.264))
        return (p.x * scale, -p.y * scale)  # Flip Y for SVG coordinates


@dataclass
class Panel:
    """Sheet metal panel"""
    name: str
    width: float  # X dimension
    depth: float  # Y dimension
    thickness: float  # Z dimension
    position: Point3D  # Position in 3D space
    holes: List[Point3D]  # Hole positions relative to panel
    material: str = "304 Stainless"

    def get_corners(self) -> List[Point3D]:
        """Get 8 corner points of panel"""
        x, y, z = self.position.x, self.position.y, self.position.z
        w, d, t = self.width, self.depth, self.thickness
        return [
            Point3D(x, y, z),
            Point3D(x + w, y, z),
            Point3D(x + w, y + d, z),
            Point3D(x, y + d, z),
            Point3D(x, y, z + t),
            Point3D(x + w, y, z + t),
            Point3D(x + w, y + d, z + t),
            Point3D(x, y + d, z + t),
        ]


class SVGDrawing:
    """SVG drawing builder"""

    def __init__(self, width: int = 1200, height: int = 1600):
        self.width = width
        self.height = height
        self.elements: List[str] = []
        self.defs: List[str] = []

    def add_def(self, def_element: str):
        """Add SVG definition (marker, pattern, etc)"""
        self.defs.append(def_element)

    def add_element(self, element: str):
        """Add SVG element"""
        self.elements.append(element)

    def line(self, x1: float, y1: float, x2: float, y2: float,
             stroke: str = "black", stroke_width: float = 1,
             stroke_dasharray: str = None, opacity: float = 1.0,
             marker_start: str = None, marker_end: str = None):
        """Draw line"""
        dash = f'stroke-dasharray="{stroke_dasharray}"' if stroke_dasharray else ''
        marker_s = f'marker-start="{marker_start}"' if marker_start else ''
        marker_e = f'marker-end="{marker_end}"' if marker_end else ''
        self.add_element(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{stroke}" stroke-width="{stroke_width}" '
            f'opacity="{opacity}" {dash} {marker_s} {marker_e}/>'
        )

    def rect(self, x: float, y: float, width: float, height: float,
             fill: str = "none", stroke: str = "black",
             stroke_width: float = 1, opacity: float = 1.0):
        """Draw rectangle"""
        self.add_element(
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" '
            f'opacity="{opacity}"/>'
        )

    def circle(self, cx: float, cy: float, r: float,
               fill: str = "none", stroke: str = "black",
               stroke_width: float = 1):
        """Draw circle"""
        self.add_element(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'
        )

    def polygon(self, points: List[Tuple[float, float]],
                fill: str = "none", stroke: str = "black",
                stroke_width: float = 1, opacity: float = 1.0):
        """Draw polygon"""
        pts = " ".join(f"{x},{y}" for x, y in points)
        self.add_element(
            f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{stroke_width}" opacity="{opacity}"/>'
        )

    def text(self, x: float, y: float, text: str,
             font_size: int = 12, anchor: str = "start",
             font_weight: str = "normal", fill: str = "black"):
        """Draw text"""
        self.add_element(
            f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" '
            f'font-size="{font_size}" text-anchor="{anchor}" '
            f'font-weight="{font_weight}" fill="{fill}">{text}</text>'
        )

    def group(self, elements: List[str], transform: str = None) -> str:
        """Create group element"""
        trans = f'transform="{transform}"' if transform else ''
        inner = '\n'.join(elements)
        return f'<g {trans}>\n{inner}\n</g>'

    def dimension_line(self, x1: float, y1: float, x2: float, y2: float,
                       label: str, offset: float = 20):
        """Draw dimension line with arrows and label"""
        # Calculate perpendicular offset
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            return

        # Perpendicular unit vector
        px = -dy / length
        py = dx / length

        # Offset points
        ox1 = x1 + px * offset
        oy1 = y1 + py * offset
        ox2 = x2 + px * offset
        oy2 = y2 + py * offset

        # Draw witness lines
        self.line(x1, y1, ox1, oy1, stroke="black", stroke_width=0.3)
        self.line(x2, y2, ox2, oy2, stroke="black", stroke_width=0.3)

        # Draw dimension line
        self.line(ox1, oy1, ox2, oy2, stroke="black", stroke_width=0.5,
                 marker_end="url(#arrowhead)", marker_start="url(#arrowhead-start)")

        # Add label at midpoint
        mid_x = (ox1 + ox2) / 2
        mid_y = (oy1 + oy2) / 2

        # Rotate text to align with dimension line
        angle = math.degrees(math.atan2(dy, dx))
        if angle > 90 or angle < -90:
            angle += 180

        self.add_element(
            f'<text x="{mid_x}" y="{mid_y - 3}" '
            f'font-family="Arial, sans-serif" font-size="8" text-anchor="middle" '
            f'fill="black" transform="rotate({angle} {mid_x} {mid_y})">{label}</text>'
        )

    def add_arrow_markers(self):
        """Add arrow marker definitions"""
        self.add_def('''
            <marker id="arrowhead" markerWidth="8" markerHeight="8"
                    refX="4" refY="2.5" orient="auto">
                <polygon points="0 0, 5 2.5, 0 5" fill="black"/>
            </marker>
        ''')
        self.add_def('''
            <marker id="arrowhead-start" markerWidth="8" markerHeight="8"
                    refX="1" refY="2.5" orient="auto">
                <polygon points="5 0, 0 2.5, 5 5" fill="black"/>
            </marker>
        ''')

    def to_svg(self) -> str:
        """Generate complete SVG"""
        defs_section = f'<defs>\n{" ".join(self.defs)}\n</defs>' if self.defs else ''
        elements_section = '\n'.join(self.elements)

        return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{self.width}" height="{self.height}"
     xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {self.width} {self.height}">
    {defs_section}
    {elements_section}
</svg>'''


class BenchDrawing:
    """Generate technical drawings for bench designs"""

    def __init__(self, concept_name: str):
        self.concept_name = concept_name
        self.svg = SVGDrawing(1200, 1600)
        self.svg.add_arrow_markers()

    def draw_title_block(self, y_offset: int = 50):
        """Draw title block"""
        self.svg.text(50, y_offset, self.concept_name,
                     font_size=18, font_weight="normal")
        self.svg.text(50, y_offset + 22,
                     "Sheet Metal Bench - SendCutSend Fabrication",
                     font_size=12, fill="black")
        self.svg.line(50, y_offset + 32, 1150, y_offset + 32,
                     stroke="black", stroke_width=0.5)
        return y_offset + 50

    def draw_orthographic_views(self, panels: List[Panel],
                                y_offset: int, scale: float = 2.0):
        """Draw top, front, and side views"""
        x_start = 100
        spacing = 350

        # Section title
        self.svg.text(50, y_offset, "ORTHOGRAPHIC VIEWS",
                     font_size=12, font_weight="normal")
        y_offset += 25

        # Calculate bounding box of entire assembly
        all_corners = []
        for panel in panels:
            all_corners.extend(panel.get_corners())

        min_x = min(p.x for p in all_corners)
        max_x = max(p.x for p in all_corners)
        min_y = min(p.y for p in all_corners)
        max_y = max(p.y for p in all_corners)
        min_z = min(p.z for p in all_corners)
        max_z = max(p.z for p in all_corners)

        # TOP VIEW (looking down -Z)
        self.svg.text(x_start + 50, y_offset, "Top View",
                     font_size=10, font_weight="normal", fill="black")
        y_offset += 20

        for panel in panels:
            corners = panel.get_corners()
            # Project to XY plane
            rect_points = [
                (x_start + (corners[0].x - min_x) * scale,
                 y_offset + (corners[0].y - min_y) * scale),
                (x_start + (corners[1].x - min_x) * scale,
                 y_offset + (corners[1].y - min_y) * scale),
                (x_start + (corners[2].x - min_x) * scale,
                 y_offset + (corners[2].y - min_y) * scale),
                (x_start + (corners[3].x - min_x) * scale,
                 y_offset + (corners[3].y - min_y) * scale),
            ]
            self.svg.polygon(rect_points, fill="white", stroke="black", stroke_width=0.5)

            # Draw holes
            for hole in panel.holes:
                hole_world = Point3D(
                    panel.position.x + hole.x,
                    panel.position.y + hole.y,
                    panel.position.z + hole.z
                )
                hx = x_start + (hole_world.x - min_x) * scale
                hy = y_offset + (hole_world.y - min_y) * scale
                self.svg.circle(hx, hy, 2, fill="white", stroke="black", stroke_width=1)

        # FRONT VIEW (looking from +Y)
        front_x = x_start + spacing
        self.svg.text(front_x + 50, y_offset - 20, "Front View",
                     font_size=10, font_weight="normal", fill="black")

        for panel in panels:
            corners = panel.get_corners()
            # Project to XZ plane
            rect_points = [
                (front_x + (corners[0].x - min_x) * scale,
                 y_offset + 250 - (corners[0].z - min_z) * scale),
                (front_x + (corners[1].x - min_x) * scale,
                 y_offset + 250 - (corners[1].z - min_z) * scale),
                (front_x + (corners[5].x - min_x) * scale,
                 y_offset + 250 - (corners[5].z - min_z) * scale),
                (front_x + (corners[4].x - min_x) * scale,
                 y_offset + 250 - (corners[4].z - min_z) * scale),
            ]
            self.svg.polygon(rect_points, fill="white", stroke="black", stroke_width=0.5)

        # SIDE VIEW (looking from +X)
        side_x = x_start + spacing * 2
        self.svg.text(side_x + 50, y_offset - 20, "Right Side View",
                     font_size=10, font_weight="normal", fill="black")

        for panel in panels:
            corners = panel.get_corners()
            # Project to YZ plane
            rect_points = [
                (side_x + (corners[0].y - min_y) * scale,
                 y_offset + 250 - (corners[0].z - min_z) * scale),
                (side_x + (corners[3].y - min_y) * scale,
                 y_offset + 250 - (corners[3].z - min_z) * scale),
                (side_x + (corners[7].y - min_y) * scale,
                 y_offset + 250 - (corners[7].z - min_z) * scale),
                (side_x + (corners[4].y - min_y) * scale,
                 y_offset + 250 - (corners[4].z - min_z) * scale),
            ]
            self.svg.polygon(rect_points, fill="white", stroke="black", stroke_width=0.5)

        return y_offset + 270

    def draw_isometric_view(self, panels: List[Panel],
                           y_offset: int, scale: float = 2.5):
        """Draw isometric 3D projection"""
        self.svg.text(50, y_offset, "ISOMETRIC VIEW",
                     font_size=12, font_weight="normal")
        y_offset += 25

        x_center = 400
        y_center = y_offset + 150

        # Draw each panel in isometric
        for panel in panels:
            corners = panel.get_corners()

            # Convert to isometric projection
            iso_points = [c.to_isometric(scale) for c in corners]

            # Draw visible faces (simple back-to-front)
            # Bottom face (0,1,2,3)
            face_bottom = [
                (x_center + iso_points[0][0], y_center + iso_points[0][1]),
                (x_center + iso_points[1][0], y_center + iso_points[1][1]),
                (x_center + iso_points[2][0], y_center + iso_points[2][1]),
                (x_center + iso_points[3][0], y_center + iso_points[3][1]),
            ]
            self.svg.polygon(face_bottom, fill="white", stroke="black",
                           stroke_width=0.5, opacity=1.0)

            # Top face (4,5,6,7)
            face_top = [
                (x_center + iso_points[4][0], y_center + iso_points[4][1]),
                (x_center + iso_points[5][0], y_center + iso_points[5][1]),
                (x_center + iso_points[6][0], y_center + iso_points[6][1]),
                (x_center + iso_points[7][0], y_center + iso_points[7][1]),
            ]
            self.svg.polygon(face_top, fill="white", stroke="black",
                           stroke_width=0.5)

            # Right face (1,2,6,5)
            face_right = [
                (x_center + iso_points[1][0], y_center + iso_points[1][1]),
                (x_center + iso_points[2][0], y_center + iso_points[2][1]),
                (x_center + iso_points[6][0], y_center + iso_points[6][1]),
                (x_center + iso_points[5][0], y_center + iso_points[5][1]),
            ]
            self.svg.polygon(face_right, fill="white", stroke="black",
                           stroke_width=0.5, opacity=1.0)

        # Add material notes
        materials_y = y_center + 200
        self.svg.text(x_center + 250, materials_y, "Materials",
                     font_size=10, font_weight="normal", fill="black")
        for i, panel in enumerate(panels):
            self.svg.text(x_center + 250, materials_y + 16 + i*14,
                         f"{panel.name}: {panel.material} {panel.thickness}\"",
                         font_size=9, fill="black")

        return y_offset + 320

    def draw_exploded_view(self, panels: List[Panel],
                          y_offset: int, scale: float = 2.5,
                          explode_distance: float = 5.0):
        """Draw exploded assembly view"""
        self.svg.text(50, y_offset, "EXPLODED ASSEMBLY",
                     font_size=12, font_weight="normal")
        y_offset += 25

        x_center = 400
        y_center = y_offset + 150

        # Explode panels along primary axis
        exploded_panels = []
        for i, panel in enumerate(panels):
            # Move panel along Z axis for explosion
            offset = explode_distance * (i - len(panels)//2)
            exploded_pos = panel.position.translate(0, 0, offset)
            exploded_panel = Panel(
                panel.name, panel.width, panel.depth, panel.thickness,
                exploded_pos, panel.holes, panel.material
            )
            exploded_panels.append(exploded_panel)

        # Draw exploded panels
        for panel in exploded_panels:
            corners = panel.get_corners()
            iso_points = [c.to_isometric(scale) for c in corners]

            # Top face
            face_top = [
                (x_center + iso_points[4][0], y_center + iso_points[4][1]),
                (x_center + iso_points[5][0], y_center + iso_points[5][1]),
                (x_center + iso_points[6][0], y_center + iso_points[6][1]),
                (x_center + iso_points[7][0], y_center + iso_points[7][1]),
            ]
            self.svg.polygon(face_top, fill="white", stroke="black",
                           stroke_width=0.5)

            # Right face
            face_right = [
                (x_center + iso_points[1][0], y_center + iso_points[1][1]),
                (x_center + iso_points[2][0], y_center + iso_points[2][1]),
                (x_center + iso_points[6][0], y_center + iso_points[6][1]),
                (x_center + iso_points[5][0], y_center + iso_points[5][1]),
            ]
            self.svg.polygon(face_right, fill="white", stroke="black",
                           stroke_width=0.5)

            # Label
            label_pos = iso_points[6]
            self.svg.text(x_center + label_pos[0] + 10,
                         y_center + label_pos[1],
                         panel.name, font_size=8, fill="black")

        # Draw assembly direction arrows
        for i in range(len(exploded_panels) - 1):
            p1 = exploded_panels[i].get_corners()[6]
            p2 = exploded_panels[i+1].get_corners()[4]
            iso1 = p1.to_isometric(scale)
            iso2 = p2.to_isometric(scale)

            self.svg.line(
                x_center + iso1[0], y_center + iso1[1],
                x_center + iso2[0], y_center + iso2[1],
                stroke="black", stroke_width=0.5,
                stroke_dasharray="2,2", opacity=0.5
            )

        return y_offset + 320

    def draw_flat_patterns(self, panels: List[Panel], y_offset: int, scale: float = 1.5):
        """Draw flat patterns for cutting"""
        self.svg.text(50, y_offset, "FLAT PATTERNS",
                     font_size=12, font_weight="normal")
        self.svg.text(50, y_offset + 16,
                     "For SendCutSend DXF Export",
                     font_size=9, fill="black")
        y_offset += 35

        x_offset = 100
        y_pos = y_offset

        for panel in panels:
            # Draw panel outline
            px = x_offset
            py = y_pos
            pw = panel.width * scale
            ph = panel.depth * scale

            self.svg.rect(px, py, pw, ph, fill="white",
                         stroke="black", stroke_width=1)

            # Draw holes
            for hole in panel.holes:
                hx = px + hole.x * scale
                hy = py + hole.y * scale
                self.svg.circle(hx, hy, 2, fill="white",
                              stroke="black", stroke_width=0.5)
                # Hole dimension
                self.svg.text(hx + 6, hy + 3, f"Ø0.25\"",
                            font_size=7, fill="black")

            # Dimensions
            self.svg.dimension_line(px, py, px + pw, py,
                                   f"{panel.width:.1f}\"", offset=-15)
            self.svg.dimension_line(px, py, px, py + ph,
                                   f"{panel.depth:.1f}\"", offset=-15)

            # Label
            self.svg.text(px + pw/2, py - 25, panel.name,
                         font_size=10, font_weight="normal", anchor="middle")
            self.svg.text(px + pw/2, py - 14,
                         f"{panel.material} - {panel.thickness}\" thick",
                         font_size=8, fill="black", anchor="middle")

            # Move to next panel position
            y_pos += ph + 80
            if y_pos > 1400:  # Start new column
                y_pos = y_offset
                x_offset += 400

        return max(y_pos, y_offset + 300)

    def save(self, filename: str):
        """Save SVG to file"""
        with open(filename, 'w') as f:
            f.write(self.svg.to_svg())


# Concept-specific definitions

def create_concept_4_slab_legs() -> List[Panel]:
    """Create Concept 4: Thin Slab Legs panels"""
    panels = []

    # Seat panel: 60" x 11" x 0.125"
    # Position at Z = 16" (height of legs)
    seat = Panel(
        name="Seat Panel",
        width=60.0,
        depth=11.0,
        thickness=0.125,
        position=Point3D(0, 0, 16.0),
        holes=[
            # 4 mounting holes per leg, 2" from edges
            Point3D(2, 2, 0),
            Point3D(2, 9, 0),
            Point3D(9, 2, 0),
            Point3D(9, 9, 0),
            # Right leg holes
            Point3D(51, 2, 0),
            Point3D(51, 9, 0),
            Point3D(58, 2, 0),
            Point3D(58, 9, 0),
        ],
        material="304 Stainless Steel"
    )
    panels.append(seat)

    # Left leg: 11" x 16" x 0.250"
    left_leg = Panel(
        name="Left Leg",
        width=11.0,
        depth=16.0,
        thickness=0.250,
        position=Point3D(0, 0, 0),
        holes=[
            # Matching holes for seat connection
            Point3D(2, 14, 0),
            Point3D(2, 14, 0),
            Point3D(9, 14, 0),
            Point3D(9, 14, 0),
        ],
        material="304 Stainless Steel"
    )
    panels.append(left_leg)

    # Right leg: 11" x 16" x 0.250"
    right_leg = Panel(
        name="Right Leg",
        width=11.0,
        depth=16.0,
        thickness=0.250,
        position=Point3D(49.0, 0, 0),
        holes=[
            # Matching holes for seat connection
            Point3D(2, 14, 0),
            Point3D(2, 14, 0),
            Point3D(9, 14, 0),
            Point3D(9, 14, 0),
        ],
        material="304 Stainless Steel"
    )
    panels.append(right_leg)

    return panels


def create_concept_2_u_modules() -> List[Panel]:
    """Create Concept 2: Three interlocking U-modules"""
    panels = []

    # Each U-module is 21" wide x 12" deep x 17" tall
    # Flat pattern: 21" x 31" (12" + 3" + 14" + 3")

    for i in range(3):
        x_pos = i * 21.0  # Position modules side by side

        # For visualization, we'll represent each U-module as 3 panels:
        # Seat, left side, right side

        # Seat portion of U
        seat = Panel(
            name=f"Module {i+1} - Seat",
            width=21.0,
            depth=12.0,
            thickness=0.100,
            position=Point3D(x_pos, 0, 17.0),
            holes=[],
            material="304 Stainless Steel"
        )
        panels.append(seat)

        # Left side of U
        left_side = Panel(
            name=f"Module {i+1} - Left Side",
            width=3.0,
            depth=12.0,
            thickness=0.100,
            position=Point3D(x_pos, 0, 3.0),
            holes=[],
            material="304 Stainless Steel"
        )
        panels.append(left_side)

        # Right side of U
        right_side = Panel(
            name=f"Module {i+1} - Right Side",
            width=3.0,
            depth=12.0,
            thickness=0.100,
            position=Point3D(x_pos + 18.0, 0, 3.0),
            holes=[],
            material="304 Stainless Steel"
        )
        panels.append(right_side)

    return panels


if __name__ == "__main__":
    # Generate Concept 4 drawings
    print("Generating Concept 4 (Slab Legs) technical drawings...")
    concept4 = BenchDrawing("Concept 4: Thin Slab Legs")
    panels4 = create_concept_4_slab_legs()

    y = concept4.draw_title_block()
    y = concept4.draw_orthographic_views(panels4, y)
    y = concept4.draw_isometric_view(panels4, y)
    y = concept4.draw_exploded_view(panels4, y)
    y = concept4.draw_flat_patterns(panels4, y)

    concept4.save("concept-4-drawings.svg")
    print("✓ Saved concept-4-drawings.svg")

    # Generate Concept 2 drawings
    print("\nGenerating Concept 2 (U-Modules) technical drawings...")
    concept2 = BenchDrawing("Concept 2: Interlocking U-Modules")
    panels2 = create_concept_2_u_modules()

    y = concept2.draw_title_block()
    y = concept2.draw_orthographic_views(panels2, y)
    y = concept2.draw_isometric_view(panels2, y)
    y = concept2.draw_exploded_view(panels2, y)
    y = concept2.draw_flat_patterns(panels2, y)

    concept2.save("concept-2-drawings.svg")
    print("✓ Saved concept-2-drawings.svg")

    print("\n✓ SVG technical drawings complete!")
