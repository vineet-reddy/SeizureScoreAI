from cogdb import CogDB
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def create_epilepsy_kg():
    kg = CogDB()
    
    # Create feature nodes
    aura_node = kg.create_node(
        label="Feature",
        properties={
            "name": "Presence of Aura",
            "type": "binary",
            "description": "Whether patient experiences aura before seizures"
        }
    )
    
    pre_seizure_node = kg.create_node(
        label="Feature",
        properties={
            "name": "Seizure Days Pre-Treatment",
            "type": "numeric",
            "description": "Baseline seizure days per year"
        }
    )
    
    post_seizure_node = kg.create_node(
        label="Feature",
        properties={
            "name": "Seizure Days Post-Treatment",
            "type": "numeric",
            "description": "Current seizure days per year"
        }
    )
    
    # Create class nodes with detailed ILAE descriptions
    class_descriptions = [
        "Completely seizure free; no auras",
        "Only auras; no other seizures",
        "1-3 seizure days per year; ± auras",
        "4 seizure days per year to 50% reduction of baseline; ± auras",
        "Less than 50% reduction of baseline seizure days; ± auras",
        "More than 100% increase of baseline seizure days; ± auras"
    ]
    
    class_nodes = []
    for i, desc in enumerate(class_descriptions, 1):
        class_node = kg.create_node(
            label="Class",
            properties={
                "name": f"Class {i}",
                "description": desc,
                "class_id": i
            }
        )
        class_nodes.append(class_node)
    
    # Updated relationship weights based on ILAE criteria
    relationships = [
        # Aura relationships - strongest influence on Class 1 (must be none) and Class 2 (must be present)
        (aura_node, "INFLUENCES", class_nodes[0], {"weight": 1.0}),  # Class 1: No auras required
        (aura_node, "INFLUENCES", class_nodes[1], {"weight": 1.0}),  # Class 2: Only auras
        (aura_node, "INFLUENCES", class_nodes[2], {"weight": 0.3}),  # Class 3: ± auras
        (aura_node, "INFLUENCES", class_nodes[3], {"weight": 0.3}),  # Class 4: ± auras
        (aura_node, "INFLUENCES", class_nodes[4], {"weight": 0.3}),  # Class 5: ± auras
        (aura_node, "INFLUENCES", class_nodes[5], {"weight": 0.3}),  # Class 6: ± auras
        
        # Pre-treatment seizure relationships (baseline)
        (pre_seizure_node, "INFLUENCES", class_nodes[0], {"weight": 0.8}),
        (pre_seizure_node, "INFLUENCES", class_nodes[1], {"weight": 0.8}),
        (pre_seizure_node, "INFLUENCES", class_nodes[2], {"weight": 0.9}),
        (pre_seizure_node, "INFLUENCES", class_nodes[3], {"weight": 1.0}),  # Important for % reduction calculation
        (pre_seizure_node, "INFLUENCES", class_nodes[4], {"weight": 1.0}),  # Important for % reduction calculation
        (pre_seizure_node, "INFLUENCES", class_nodes[5], {"weight": 1.0}),  # Important for % increase calculation
        
        # Post-treatment seizure relationships (strongest influence as it's the primary outcome measure)
        (post_seizure_node, "INFLUENCES", class_nodes[0], {"weight": 1.0}),  # Must be 0
        (post_seizure_node, "INFLUENCES", class_nodes[1], {"weight": 1.0}),  # Must be 0 (except auras)
        (post_seizure_node, "INFLUENCES", class_nodes[2], {"weight": 1.0}),  # 1-3 days/year
        (post_seizure_node, "INFLUENCES", class_nodes[3], {"weight": 1.0}),  # 4+ days to 50% reduction
        (post_seizure_node, "INFLUENCES", class_nodes[4], {"weight": 1.0}),  # <50% reduction
        (post_seizure_node, "INFLUENCES", class_nodes[5], {"weight": 1.0}),  # >100% increase
    ]
    
    # Add relationships to the graph
    for start_node, rel_type, end_node, props in relationships:
        kg.create_relationship(start_node, rel_type, end_node, properties=props)
    
    return kg

def calculate_ilae_score(kg, patient_data):
    """
    Calculate ILAE score based on strict ILAE classification criteria
    """
    pre_seizures = patient_data["pre_seizure_days"]
    post_seizures = patient_data["post_seizure_days"]
    has_aura = patient_data["aura"]
    
    # Calculate percentage change in seizure frequency
    if pre_seizures > 0:
        percent_change = ((post_seizures - pre_seizures) / pre_seizures) * 100
    else:
        percent_change = 0 if post_seizures == 0 else float('inf')
    
    # Determine ILAE class based on strict criteria
    if post_seizures == 0 and not has_aura:
        return 1, 1.0  # Class 1: Completely seizure free, no auras
    elif post_seizures == 0 and has_aura:
        return 2, 1.0  # Class 2: Only auras
    elif 1 <= post_seizures <= 3:
        return 3, 1.0  # Class 3: 1-3 seizure days per year
    elif post_seizures >= 4 and percent_change <= -50:
        return 4, 0.8  # Class 4: 4+ days to 50% reduction
    elif percent_change > -50:
        return 5, 0.8  # Class 5: Less than 50% reduction
    elif percent_change > 100:
        return 6, 1.0  # Class 6: More than 100% increase
    
    # Default case with confidence calculation
    return 5, 0.6

def visualize_knowledge_graph(kg):
    """[Previous visualization code remains the same]"""
    # Create NetworkX graph
    G = nx.DiGraph()
    
    # Add nodes
    feature_nodes = kg.find_nodes(label="Feature")
    class_nodes = kg.find_nodes(label="Class")
    
    # Position calculations
    feature_x = {"Presence of Aura": 0, 
                "Seizure Days Pre-Treatment": 0.5,
                "Seizure Days Post-Treatment": 1}
    
    # Add feature nodes
    for node in feature_nodes:
        name = node.properties["name"]
        G.add_node(name, 
                  node_type="feature",
                  pos=(feature_x[name], 1))
    
    # Add class nodes with descriptions
    for i, node in enumerate(class_nodes):
        name = f'{node.properties["name"]}\n{node.properties["description"]}'
        G.add_node(name,
                  node_type="class",
                  pos=(i * 0.2, 0))
    
    # Add edges with weights
    for feature in feature_nodes:
        feature_name = feature.properties["name"]
        for class_node in class_nodes:
            class_name = f'{class_node.properties["name"]}\n{class_node.properties["description"]}'
            rel = kg.get_relationships(feature, class_node)[0]
            weight = rel.properties["weight"]
            G.add_edge(feature_name, class_name, weight=weight)
    
    plt.figure(figsize=(15, 10))
    
    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')
    
    # Draw nodes
    feature_nodes = [n for n, attr in G.nodes(data=True) if attr['node_type'] == 'feature']
    class_nodes = [n for n, attr in G.nodes(data=True) if attr['node_type'] == 'class']
    
    nx.draw_networkx_nodes(G, pos, nodelist=feature_nodes, 
                          node_color='lightcoral',
                          node_size=2000,
                          node_shape='s')
    
    nx.draw_networkx_nodes(G, pos, nodelist=class_nodes,
                          node_color='lavender',
                          node_size=3000,
                          node_shape='o')
    
    # Draw edges with weights
    edges = G.edges(data=True)
    weights = [e[2]['weight'] * 2 for e in edges]
    nx.draw_networkx_edges(G, pos, width=weights, edge_color='gray',
                          arrowsize=20, alpha=0.5)
    
    # Add labels with smaller font for class descriptions
    nx.draw_networkx_labels(G, pos, font_size=8)
    
    # Add legend
    legend_elements = [
        Rectangle((0, 0), 1, 1, facecolor='lightcoral', label='Features'),
        Rectangle((0, 0), 1, 1, facecolor='lavender', label='ILAE Classes')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    plt.title("ILAE Outcome Scale Knowledge Graph", pad=20)
    plt.axis('off')
    plt.tight_layout()
    
    return plt

# Example usage
if __name__ == "__main__":
    kg = create_epilepsy_kg()
    
    # Test cases for different ILAE classes
    test_cases = [
        {"aura": 0, "pre_seizure_days": 24, "post_seizure_days": 0},  # Class 1
        {"aura": 1, "pre_seizure_days": 24, "post_seizure_days": 0},  # Class 2
        {"aura": 1, "pre_seizure_days": 24, "post_seizure_days": 2},  # Class 3
        {"aura": 1, "pre_seizure_days": 24, "post_seizure_days": 10}, # Class 4
        {"aura": 0, "pre_seizure_days": 24, "post_seizure_days": 20}, # Class 5
        {"aura": 1, "pre_seizure_days": 24, "post_seizure_days": 50}  # Class 6
    ]
    
    # Test classification
    for i, case in enumerate(test_cases, 1):
        predicted_class, confidence = calculate_ilae_score(kg, case)
        print(f"\nTest Case {i}:")
        print(f"Input: {case}")
        print(f"Predicted ILAE Class: {predicted_class}")
        print(f"Confidence Score: {confidence:.2f}")
    
    # Visualize the graph
    plt = visualize_knowledge_graph(kg)
    plt.show()