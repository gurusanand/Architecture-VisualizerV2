# Draw.io Export Feature Guide

## Overview

The Full Architecture diagram can now be exported to draw.io (diagrams.net) format for further editing and customization!

---

## 🎯 How to Export

### Step 1: Configure Your Diagram

1. Open the visualizer: https://8501-icga2n723qzn0e7tah8bd-3e19ad68.manus-asia.computer
2. Navigate to **"📊 Full Architecture"** in the sidebar
3. Configure your diagram:
   - **Show Layers**: Select which layers to include (all selected by default)
   - **Highlight Component**: Optional - highlight a specific component
   - **Diagram Direction**: Choose "Top to Bottom" or "Left to Right"

### Step 2: Export to Draw.io

1. Click the **"📥 Export to Draw.io"** button (centered below the filters)
2. A download button will appear: **"💾 Download .drawio File"**
3. Click the download button
4. Save the file as `enterprise_architecture.drawio`

### Step 3: Open in Draw.io

**Option A: Online (Recommended)**
1. Go to https://app.diagrams.net
2. Click **"Open Existing Diagram"**
3. Select the downloaded `.drawio` file
4. Edit and customize as needed!

**Option B: Desktop App**
1. Download draw.io desktop app from https://github.com/jgraph/drawio-desktop/releases
2. Install and open the app
3. File → Open → Select the `.drawio` file
4. Edit and customize!

**Option C: VS Code Extension**
1. Install "Draw.io Integration" extension in VS Code
2. Open the `.drawio` file in VS Code
3. Edit directly in your editor!

---

## 📊 What Gets Exported

### Components
- All components in selected layers
- Component names with icons (📨, 🎯, etc.)
- Component colors matching the visualizer
- Rounded rectangle shapes

### Layers
- Each layer as a swimlane container
- Layer names and colors
- Hierarchical organization

### Connections
- All edges between components in selected layers
- Edge labels showing protocols/actions
- Orthogonal routing (right-angle connectors)
- Arrows indicating direction

### Layout
- Automatic positioning based on layers
- 4 components per row within each layer
- Proper spacing and alignment
- Responsive to diagram direction (TB or LR)

---

## 🎨 Customization in Draw.io

Once you open the exported file in draw.io, you can:

### Edit Components
- **Resize**: Drag corners to resize boxes
- **Recolor**: Right-click → Style → Fill color
- **Rename**: Double-click to edit text
- **Add icons**: Insert → Advanced → Icons
- **Change shape**: Right-click → Edit Style → shape=...

### Edit Connections
- **Reroute**: Drag connection points
- **Change style**: Right-click → Style → Line style
- **Add waypoints**: Drag the line to add bends
- **Change arrows**: Right-click → Style → Arrow type

### Add Elements
- **Text boxes**: Insert → Text
- **Shapes**: Insert → Shapes → Select category
- **Images**: Insert → Image → Upload or URL
- **Notes**: Insert → Advanced → Note

### Layout Options
- **Auto-arrange**: Arrange → Layout → Choose algorithm
- **Align**: Arrange → Align → Choose alignment
- **Distribute**: Arrange → Distribute → Horizontal/Vertical
- **Group**: Select multiple → Right-click → Group

### Export from Draw.io
- **PNG**: File → Export as → PNG
- **SVG**: File → Export as → SVG
- **PDF**: File → Export as → PDF
- **HTML**: File → Export as → HTML

---

## 💡 Use Cases

### 1. Executive Presentations
- Export diagram
- Simplify by removing technical details
- Add company branding
- Export as PNG for PowerPoint

### 2. Technical Documentation
- Export full architecture
- Add detailed notes and annotations
- Include version information
- Export as PDF for documentation

### 3. Architecture Reviews
- Export diagram
- Highlight proposed changes in different color
- Add decision notes
- Share with team for feedback

### 4. Compliance Audits
- Export with all layers
- Add compliance annotations
- Highlight security components
- Export as PDF for audit trail

### 5. Training Materials
- Export diagram
- Add numbered steps
- Include explanatory notes
- Create simplified versions for different audiences

---

## 🔧 Technical Details

### File Format
- **Format**: draw.io XML (mxGraph format)
- **Extension**: `.drawio` (also compatible with `.xml`)
- **Encoding**: UTF-8
- **Compatibility**: draw.io v22.1.0+

### Layout Algorithm
- **Layer arrangement**: Vertical stacking (TB) or horizontal (LR)
- **Component layout**: Grid layout (4 per row)
- **Spacing**: 20px between components, 50px between layers
- **Dimensions**: 
  - Layer: 800px width, dynamic height
  - Component: 140px × 60px
  - Canvas: 1169px × 827px (A4 landscape)

### Styling
- **Components**: Rounded rectangles with fill colors
- **Layers**: Swimlanes with header
- **Edges**: Orthogonal routing with arrows
- **Fonts**: Arial, 10-14pt
- **Colors**: Preserved from visualizer

---

## 🎯 Tips & Tricks

### Tip 1: Export Specific Layers
Want to focus on a specific part of the architecture?
1. Deselect all layers in "Show Layers"
2. Select only the layers you want (e.g., "Messaging & Streaming")
3. Export - you'll get a clean diagram with just those components!

### Tip 2: Create Multiple Views
Create different diagrams for different audiences:
- **Executive View**: Entry + Orchestration + Agents only
- **Security View**: Security + Governance + Monitoring
- **Data View**: Data Layer + Support Services
- **Integration View**: External Services + MCP Tools

### Tip 3: Add Custom Annotations
After exporting:
1. Open in draw.io
2. Add text boxes with notes
3. Use different colors for different types of notes
4. Add shapes to highlight areas

### Tip 4: Version Control
- Save different versions with dates: `architecture_2024-01-15.drawio`
- Use draw.io's built-in version history (File → Revision History)
- Store in Git for team collaboration

### Tip 5: Embed in Documentation
- Export as SVG for crisp scaling
- Embed in Markdown: `![Architecture](architecture.svg)`
- Or export as PNG for compatibility

---

## 🐛 Troubleshooting

### Issue: File won't open in draw.io
**Solution**: 
- Ensure file extension is `.drawio` or `.xml`
- Try opening in browser version first (app.diagrams.net)
- Check file isn't corrupted (should be valid XML)

### Issue: Components overlap
**Solution**:
- In draw.io: Arrange → Layout → Vertical Tree
- Or manually drag components to reposition
- Use Arrange → Align to clean up

### Issue: Missing components
**Solution**:
- Check which layers were selected before export
- Re-export with all layers selected
- Verify component is in the selected layers

### Issue: Colors look different
**Solution**:
- draw.io may render colors slightly differently
- Manually adjust: Right-click → Style → Fill color
- Use hex codes from COMPONENTS in architecture_data.py

### Issue: Export button doesn't appear
**Solution**:
- Refresh the browser page
- Check you're on "Full Architecture" page
- Verify Streamlit is running (check URL works)

---

## 📚 Related Resources

### Draw.io Documentation
- Official docs: https://www.drawio.com/doc/
- Tutorials: https://www.youtube.com/c/drawio
- Templates: https://www.drawio.com/blog/diagram-templates

### Architecture Diagrams
- C4 Model: https://c4model.com/
- ArchiMate: https://www.opengroup.org/archimate-forum
- AWS Architecture Icons: https://aws.amazon.com/architecture/icons/

### Export Formats
- SVG: Scalable vector graphics for web
- PNG: Raster images for presentations
- PDF: Print-ready documents
- HTML: Interactive diagrams

---

## ✅ Summary

**Export Process:**
1. Configure diagram (layers, direction)
2. Click "📥 Export to Draw.io"
3. Click "💾 Download .drawio File"
4. Open in draw.io (app.diagrams.net)
5. Edit and customize
6. Export to your preferred format

**Benefits:**
- ✅ Full editability in professional diagram tool
- ✅ Add custom annotations and notes
- ✅ Create multiple views for different audiences
- ✅ Export to PNG, SVG, PDF for documentation
- ✅ Version control and collaboration
- ✅ Professional presentation quality

**The export feature gives you complete control over the architecture diagram for any use case!** 🎉
