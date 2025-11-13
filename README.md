# Metal Bench Design Project

High-fidelity design visualizations for minimalist metal benches inspired by Naoto Fukasawa, optimized for SendCutSend fabrication.

## 📁 Project Files

### Visualization Tools
- **`svg_bench_drawer.py`** - SVG technical drawing generator
  - Orthographic projections (top, front, side views)
  - Isometric 3D projection
  - Exploded assembly views
  - Flat patterns with dimensions for fabrication

- **`bench_3d_viewer.py`** - Interactive 3D visualizer
  - Browser-based 3D models using Plotly
  - Rotate/pan/zoom controls
  - Assembly/exploded view toggle
  - Connection visualization

### Generated Visualizations
- **`concept-2-drawings.svg`** - Technical drawings for U-Modules concept
- **`concept-2-3d.html`** - Interactive 3D model for U-Modules
- **`concept-4-drawings.svg`** - Technical drawings for Slab Legs concept
- **`concept-4-3d.html`** - Interactive 3D model for Slab Legs
- **`comparison.html`** - Side-by-side comparison page

### Documentation
- **`bench-design-concepts.md`** - Detailed design concepts and constraints

## 🚀 Quick Start

### View the Comparison
Open `comparison.html` in your browser to see side-by-side SVG and 3D visualizations.

### Generate New Visualizations

1. **Setup Python environment:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install plotly numpy
```

2. **Generate SVG technical drawings:**
```bash
python3 svg_bench_drawer.py
```
Output: `concept-2-drawings.svg`, `concept-4-drawings.svg`

3. **Generate 3D interactive models:**
```bash
python3 bench_3d_viewer.py
```
Output: `concept-2-3d.html`, `concept-4-3d.html`

## 🎨 Design Concepts

### Concept 4: Thin Slab Legs (Recommended)
- **Philosophy**: Most Fukasawa-like, absolute minimal form
- **Panels**: 3 flat panels, NO BENDING required
- **Dimensions**: 60" × 11" seat + two 11" × 16" legs
- **Material**: 304 Stainless Steel (.125" seat, .250" legs)
- **Assembly**: Through-bolts or slot/tab connection

### Concept 2: Interlocking U-Modules
- **Philosophy**: Modular, scalable system
- **Panels**: Three identical U-shaped modules
- **Dimensions**: Each module 21" × 31" flat pattern
- **Material**: 304 Stainless Steel (.100" thickness)
- **Assembly**: Bolt or slot together horizontally

## 🏭 SendCutSend Manufacturing Constraints

### Size Limits
- **Maximum part size**: 44" × 30" (varies by material)
- **Maximum bend size**: 44" × 30" flat pattern
- **Maximum thickness for bending**: 0.250"

### Materials Available
- **304 Stainless Steel**: .030" to .500" (10 thicknesses)
- **5052 Aluminum**: .040" to .500" (10 thicknesses)
- **6061 Aluminum**: .040" to .750" (9 thicknesses)
- **Cold Rolled 1008**: .030" to .135" (7 thicknesses)

### Bending Specifications
- **Process**: Air bending only (no roll forming)
- **Bend radius**: Preset per material/thickness (.024" - .250")
- **No custom bend radii** available
- **Feature distortion**: Keep holes/cutouts >0.5" from bend lines
- **Minimum flange length**: Varies by material thickness

## 🎯 Design Philosophy (Naoto Fukasawa)

- **"Without Thought"**: Objects that dissolve into everyday behavior
- **Normality over novelty**: Find the iconic form, then minimize
- **Contextual design**: Never design in isolation
- **Observation-based**: Derived from unconscious human interactions
- **Material honesty**: Simple planes, visible structure

Reference: Asian Bench for Maruni
- Dimensions: 165cm/240cm long × 30cm deep × 44cm high
- Simple horizontal and vertical planes
- Dual function (bench/side table)

## 📐 Fusion 360 Workflow

### For Concept 4 (No Bends)
1. Create new design
2. Import SVG flat patterns as sketches
3. Extrude to material thickness
4. Add hole features from dimensions
5. Create assembly with constraints
6. Export each panel as DXF

### For Concept 2 (With Bends)
1. Use Sheet Metal workspace
2. Set K-factor from SendCutSend material catalog
3. Model folded form
4. Generate flat pattern
5. Verify flat pattern ≤ 44" × 30"
6. Export flat pattern as DXF

### SendCutSend Upload
1. Go to sendcutsend.com
2. Upload DXF files
3. Select material and thickness
4. Configure bending (if needed)
5. Add hardware insertion (optional)
6. Choose finish (powder coat, anodize, etc.)
7. Review and order

## 📊 Visualization Comparison

### SVG Technical Drawings
**Best for:**
- Production documentation
- Dimensioned drawings
- Flat pattern export
- Print-friendly shop floor docs
- DXF conversion

**Features:**
- Orthographic projections
- Isometric view
- Exploded assembly
- Dimension lines
- Material callouts

### Interactive 3D Models
**Best for:**
- Design validation
- Client presentations
- Spatial understanding
- Assembly visualization
- Design review

**Features:**
- Rotate/pan/zoom
- Assembly/exploded toggle
- Real-time interaction
- Browser-based
- No software required

## 🔧 Customization

### Modify Dimensions
Edit the panel creation functions in the Python files:
- `create_concept_4_slab_legs()` in both files
- `create_concept_2_u_modules()` in both files

### Change Materials
Update the `material` parameter in Panel definitions.

### Adjust Scale
Modify the `scale` parameter in drawing functions:
- SVG: `draw_orthographic_views(panels, y_offset, scale=2.0)`
- 3D: `create_box_mesh()` coordinates (1 unit = 1 inch)

### Add New Concepts
1. Create panel definition function
2. Add to both `svg_bench_drawer.py` and `bench_3d_viewer.py`
3. Generate visualizations
4. Update `comparison.html`

## 📝 Next Steps

1. **Choose a concept**: Review designs in `comparison.html`
2. **Verify constraints**: Check SendCutSend material catalog for latest specs
3. **Model in Fusion 360**: Use dimensions from SVG flat patterns
4. **Export DXF**: Generate fabrication files from Fusion 360
5. **Upload to SendCutSend**: Configure materials and finishing
6. **Order**: Review quote and place order

## 🎓 Resources

- [SendCutSend Material Catalog](https://sendcutsend.com/materials/)
- [SendCutSend Bending Guidelines](https://sendcutsend.com/guidelines/bending/)
- [Naoto Fukasawa Design](https://naotofukasawa.com/)
- [Fusion 360 Sheet Metal Workspace](https://help.autodesk.com/view/fusion360/ENU/?guid=SLD-SHEET-METAL)

## 🤝 Contributing

To add new design concepts:
1. Define panel dimensions and positions
2. Add creation functions to both Python tools
3. Run generators to create visualizations
4. Update comparison page

## 📄 License

This is a design exploration project. Generated designs are free to use for personal or commercial fabrication.

---

**Status**: Ready for Fusion 360 modeling and SendCutSend fabrication
**Last Updated**: 2025-11-13
