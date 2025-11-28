"""
Draw.io (diagrams.net) XML Exporter
Converts architecture diagram to draw.io format
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom
from architecture_data import COMPONENTS, LAYERS, FLOWS


def create_drawio_xml(show_layers: list, direction: str = "TB") -> str:
    """
    Create draw.io XML format from architecture data
    
    Args:
        show_layers: List of layer names to include
        direction: "TB" (top to bottom) or "LR" (left to right)
    
    Returns:
        XML string in draw.io format
    """
    
    # Create root mxfile element
    mxfile = ET.Element('mxfile', {
        'host': 'app.diagrams.net',
        'modified': '2024-01-01T00:00:00.000Z',
        'agent': 'Manus Architecture Visualizer',
        'version': '22.1.0',
        'type': 'device'
    })
    
    # Create diagram element
    diagram = ET.SubElement(mxfile, 'diagram', {
        'id': 'architecture-diagram',
        'name': 'Enterprise Agent Platform Architecture'
    })
    
    # Create mxGraphModel
    graph_model = ET.SubElement(diagram, 'mxGraphModel', {
        'dx': '1422',
        'dy': '794',
        'grid': '1',
        'gridSize': '10',
        'guides': '1',
        'tooltips': '1',
        'connect': '1',
        'arrows': '1',
        'fold': '1',
        'page': '1',
        'pageScale': '1',
        'pageWidth': '1169',
        'pageHeight': '827',
        'math': '0',
        'shadow': '0'
    })
    
    # Create root and parent cells
    root = ET.SubElement(graph_model, 'root')
    ET.SubElement(root, 'mxCell', {'id': '0'})
    ET.SubElement(root, 'mxCell', {'id': '1', 'parent': '0'})
    
    # Calculate layout positions
    layer_positions = {}
    component_positions = {}
    
    # Layout parameters
    layer_width = 800
    layer_height = 200
    layer_spacing = 50
    component_width = 140
    component_height = 60
    component_spacing_x = 20
    component_spacing_y = 20
    start_x = 50
    start_y = 50
    
    # Group components by layer
    components_by_layer = {}
    for comp_id, comp_data in COMPONENTS.items():
        layer_name = LAYERS[comp_data['layer']]['name']
        if layer_name in show_layers:
            if layer_name not in components_by_layer:
                components_by_layer[layer_name] = []
            components_by_layer[layer_name].append((comp_id, comp_data))
    
    # Calculate positions for each layer
    current_y = start_y
    cell_id = 2
    
    for layer_id, layer_info in sorted(LAYERS.items(), key=lambda x: x[1]['order']):
        layer_name = layer_info['name']
        if layer_name not in show_layers:
            continue
        
        components = components_by_layer.get(layer_name, [])
        if not components:
            continue
        
        # Calculate layer dimensions based on components
        components_per_row = 4
        num_rows = (len(components) + components_per_row - 1) // components_per_row
        actual_layer_height = max(layer_height, num_rows * (component_height + component_spacing_y) + 80)
        
        # Create layer container (swimlane)
        layer_cell_id = f'layer_{layer_id}'
        layer_cell = ET.SubElement(root, 'mxCell', {
            'id': layer_cell_id,
            'value': layer_name,
            'style': f'swimlane;startSize=30;fillColor={layer_info["color"]};strokeColor=#666666;fontStyle=1;fontSize=14;',
            'vertex': '1',
            'parent': '1'
        })
        ET.SubElement(layer_cell, 'mxGeometry', {
            'x': str(start_x),
            'y': str(current_y),
            'width': str(layer_width),
            'height': str(actual_layer_height),
            'as': 'geometry'
        })
        
        layer_positions[layer_name] = (start_x, current_y, layer_width, actual_layer_height)
        
        # Add components within layer
        comp_x = 20
        comp_y = 50
        col_count = 0
        
        for comp_id, comp_data in components:
            # Create component cell
            comp_cell_id = f'comp_{comp_id}'
            
            # Style with color
            style = (
                f'rounded=1;whiteSpace=wrap;html=1;'
                f'fillColor={comp_data["color"]};'
                f'strokeColor=#666666;'
                f'fontColor=#FFFFFF;'
                f'fontSize=11;'
                f'fontStyle=1;'
            )
            
            # Component label with icon and name
            label = f'{comp_data["icon"]} {comp_data["name"]}'
            
            comp_cell = ET.SubElement(root, 'mxCell', {
                'id': comp_cell_id,
                'value': label,
                'style': style,
                'vertex': '1',
                'parent': layer_cell_id
            })
            
            ET.SubElement(comp_cell, 'mxGeometry', {
                'x': str(comp_x),
                'y': str(comp_y),
                'width': str(component_width),
                'height': str(component_height),
                'as': 'geometry'
            })
            
            # Store absolute position for edges
            abs_x = start_x + comp_x + component_width / 2
            abs_y = current_y + comp_y + component_height / 2
            component_positions[comp_id] = (comp_cell_id, abs_x, abs_y)
            
            # Update position for next component
            col_count += 1
            if col_count >= components_per_row:
                col_count = 0
                comp_x = 20
                comp_y += component_height + component_spacing_y
            else:
                comp_x += component_width + component_spacing_x
        
        current_y += actual_layer_height + layer_spacing
    
    # Add edges (connections)
    edge_id = 1000
    for flow in FLOWS:
        from_layer = LAYERS[COMPONENTS[flow['from']]['layer']]['name']
        to_layer = LAYERS[COMPONENTS[flow['to']]['layer']]['name']
        
        # Only show edges if both components' layers are visible
        if from_layer in show_layers and to_layer in show_layers:
            if 'condition' not in flow:  # Skip conditional flows
                if flow['from'] in component_positions and flow['to'] in component_positions:
                    from_cell_id = component_positions[flow['from']][0]
                    to_cell_id = component_positions[flow['to']][0]
                    
                    # Create edge
                    edge_cell = ET.SubElement(root, 'mxCell', {
                        'id': f'edge_{edge_id}',
                        'value': flow['label'],
                        'style': (
                            'edgeStyle=orthogonalEdgeStyle;'
                            'rounded=1;'
                            'orthogonalLoop=1;'
                            'jettySize=auto;'
                            'html=1;'
                            'strokeColor=#6B7280;'
                            'fontSize=9;'
                            'fontColor=#6B7280;'
                            'endArrow=classic;'
                        ),
                        'edge': '1',
                        'parent': '1',
                        'source': from_cell_id,
                        'target': to_cell_id
                    })
                    
                    ET.SubElement(edge_cell, 'mxGeometry', {
                        'relative': '1',
                        'as': 'geometry'
                    })
                    
                    edge_id += 1
    
    # Convert to pretty XML string
    xml_str = ET.tostring(mxfile, encoding='unicode')
    
    # Pretty print
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    
    # Remove extra blank lines
    lines = [line for line in pretty_xml.split('\n') if line.strip()]
    return '\n'.join(lines)


def export_to_drawio(show_layers: list, direction: str = "TB", filename: str = "architecture.drawio") -> bytes:
    """
    Export architecture diagram to draw.io file
    
    Args:
        show_layers: List of layer names to include
        direction: "TB" (top to bottom) or "LR" (left to right)
        filename: Output filename
    
    Returns:
        Bytes content of the draw.io file
    """
    xml_content = create_drawio_xml(show_layers, direction)
    return xml_content.encode('utf-8')
