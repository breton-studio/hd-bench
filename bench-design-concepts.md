# Metal Bench Design Concepts
Fukasawa-inspired minimalist bench designs for SendCutSend fabrication

## Design Constraints
- Max panel size: 44" × 30" (1118mm × 762mm)
- Max bend size: 44" × 30" flat pattern
- Target bench length: ~65" (165cm) like Fukasawa's Asian Bench
- Target seat depth: ~12" (30cm)
- Target height: ~17" (43cm)

---

## Concept 1: L-Bracket Legs + Continuous Seat

### Description
Two identical L-shaped leg assemblies with a single flat seat panel spanning across.

### Components
```
SIDE VIEW (one leg assembly):

     17"
     ↕
    ┌─────────┐ ← 0.5" lip
    │  SEAT   │
════╧═════════╧════
│               │
│               │ 16.5"
│               │
│               │
└───────────────┘
    ← 12" →

LEG PANEL (flat pattern before bending):
┌──────────────────┐
│                  │ 12"
│    Bend line     │
│    ─ ─ ─ ─ ─     │
│                  │ 17"
│                  │
└──────────────────┘
  ← 12" or 14" →
```

### Panel List
1. **Seat Panel**: 65" × 12" × 0.125" (fits within 44" if split)
2. **Left Leg**: 12" × 29" flat → bent to L-shape (16.5" + 12")
3. **Right Leg**: 12" × 29" flat → bent to L-shape (16.5" + 12")

### Assembly
- Legs bolt through seat from underneath
- 4-6 holes per leg connection
- Clean top surface (no visible fasteners)

### Pros
- Extremely simple: 2 bends total
- Stable structure
- Easy to disassemble/flat pack
- Classic Fukasawa simplicity

### Cons
- Seat needs to be split (65" > 44") or designed shorter
- Requires precise bend angles

---

## Concept 2: Interlocking U-Modules

### Description
Three identical U-shaped modules that slot together horizontally.

### Components
```
TOP VIEW:
┌──────┐  ┌──────┐  ┌──────┐
│      │  │      │  │      │
│  U   │──│  U   │──│  U   │
│      │  │      │  │      │
└──────┘  └──────┘  └──────┘
← 21" →  ← 21" →  ← 21" →

SIDE VIEW (one module):
┌─────────────┐
│   SEAT      │
│             │
├─┐         ┌─┤
│ │         │ │
│ │         │ │ 17"
│ │         │ │
└─┘         └─┘
  ← 12" →

FLAT PATTERN (one module):
                12"
        ┌───────────────┐
        │               │
        │     SEAT      │
        │               │
   ─ ─ ─├───────────────┤─ ─ ─  Bend lines
3" │    │               │    │ 3"
   │    │     SIDE      │    │
14"│    │               │    │ 14"
   │    │               │    │
   └────┴───────────────┴────┘
        ←─── 21" ────→
Total flat: 21" × 31" ✓ FITS!
```

### Panel List
1. **Module 1**: 21" × 31" flat → U-shape
2. **Module 2**: 21" × 31" flat → U-shape
3. **Module 3**: 21" × 31" flat → U-shape

### Assembly
- Slot tabs or bolt modules together
- Optional: continuous aluminum bar through all three
- Can be used as 1, 2, or 3 units independently

### Pros
- Each module fits in one panel (21" × 31")
- Only 2 bends per module, parallel bends
- Modular: use 1-3 units as needed
- Can ship flat, easy assembly
- Very "Fukasawa" - simple repeated form

### Cons
- 6 total bends across all modules
- Needs connection hardware between modules
- Legs might feel less substantial (3" depth)

---

## Concept 3:折り紙 (Origami) Fold

### Description
Two identical zigzag panels that create legs and structure, with seat spanning across.

### Components
```
SIDE VIEW:
      SEAT PANEL
    ┌────────────┐
════╧════════════╧════
   ╱│            │╲
  ╱ │            │ ╲
 ╱  │            │  ╲
╱   │            │   ╲
────┘            └────

ZIGZAG PANEL (flat pattern):
        12"
    ┌─────────┐
    │         │ 8"
 ─ ─├─────────┤─ ─  Bend 1
    │         │ 10"
 ─ ─├─────────┤─ ─  Bend 2
    │         │ 8"
    └─────────┘
Total: 12" × 26" ✓ FITS!
```

### Panel List
1. **Seat**: 65" × 12" (needs split or shorter)
2. **Left Zigzag**: 12" × 26" flat → 3D folded form
3. **Right Zigzag**: 12" × 26" flat → 3D folded form

### Assembly
- Zigzag panels bolt to seat from underneath
- Angled legs provide visual interest
- Could add crossbar between legs for rigidity

### Pros
- Sculptural, still minimal
- Strong triangulated structure
- Each panel easily fits constraint
- Interesting shadow play (Fukasawa likes this)

### Cons
- More complex bending (2 bends per leg, different angles)
- Harder to calculate flat pattern accurately
- May need custom bend angles

---

## Concept 4: Thin Leg Slabs (Most Fukasawa)

### Description
Two vertical slab legs with continuous seat. Absolute minimal form.

### Components
```
END VIEW:
    ┌─────────────┐
    │    SEAT     │
════╧═════════════╧════
    │             │
    │    SLAB     │ 16.5"
    │     LEG     │
    └─────────────┘
      ← 12" →

TOP VIEW:
┌─────────────────────────────────────┐
│                                     │
│            SEAT                     │
│                                     │
│════╧═══════════════════════╧════    │
     │                       │
     │  LEG 1          LEG 2 │
     └───────────────────────┘
     ↕                       ↕
    12"                     12"
     ←───── 50"-60" ─────→
```

### Panel List
1. **Seat**: 60" × 12" flat panel (fits if ≤60")
2. **Leg 1**: 12" × 16.5" flat slab
3. **Leg 2**: 12" × 16.5" flat slab

### Assembly
- Through-bolts or threaded inserts
- Could add slot in seat, tab on leg (CNC cut)
- Extremely simple connection
- Hardware can be decorative (visible from side)

### Pros
- NO BENDS! Pure flat panels
- Absolutely minimal
- Closest to Fukasawa's aesthetic
- Easy to fabricate, ship flat
- Can customize length by cutting seat panel
- Visual lightness from thin profile

### Cons
- Less stable without cross-bracing
- Might need diagonal brace or thicker material
- Hardware visible from sides (could be feature)
- Legs might rack without additional support

### Variations
- Add small feet (bent tabs at bottom)
- Use thicker material for legs (.187"-.250")
- Add decorative cutout in legs (weight reduction + visual interest)
- Slot + tab connection instead of bolts

---

## Material Recommendations by Concept

| Concept | Material | Thickness | Why |
|---------|----------|-----------|-----|
| 1: L-Bracket | 5052 Aluminum | .125" | Good bend radius, lightweight |
| 2: U-Modules | 304 Stainless | .090"-.100" | Thin enough to bend cleanly, strong |
| 3: Origami | 5052 Aluminum | .080" | Multiple bends need thinner stock |
| 4: Slabs | 304 Stainless or Cold Rolled | .187"-.250" | No bends = can use thick, stable material |

---

## Recommended Starting Point

**Concept 4 (Thin Leg Slabs)** is most aligned with Fukasawa's philosophy:
- "Without thought" simplicity
- Honest material expression
- Minimal intervention
- Easy to understand form

### Refined Dimensions
```
SEAT: 60" × 11" × 0.125" (1524mm × 279mm)
LEGS: 11" × 16" × 0.250" (279mm × 406mm)
Material: 304 Stainless Steel, brushed finish

All panels fit well within 44" × 30" constraint.
```

### Next Steps for Fusion 360
1. Create new design
2. Model seat as flat panel with slot cutouts
3. Model legs with tab protrusions
4. Add assembly constraints to verify fit
5. Export DXF for each component
6. Add hardware callouts (M6 socket head cap screws)

Would you like me to detail the connection method and hardware for Concept 4?
