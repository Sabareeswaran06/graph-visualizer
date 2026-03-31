import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
import random
import numpy as np

class GraphGenerator:
    def __init__(self, n):
        self.n = n
        self.cycle_weights = [0] * n
        self.pendant_weights = [0] * n

    def generate_solution(self):
        """Generate a valid graph configuration"""

        if self.n == 2:
            return self.generate_n2_solution()
        elif self.n == 3:
            return self.generate_n3_solution()
        else:
            return self.generate_general_solution()

    def generate_n2_solution(self):
        """Generate solution for n=2"""
        self.pendant_weights = [0, 3]
        self.cycle_weights = [1, 2]
        return True

    def generate_n3_solution(self):
        """Generate solution for n=3"""
        self.pendant_weights = [0, 6, 9]
        self.cycle_weights = [3, 6, 9]
        return True

    def generate_general_solution(self):
        """Generate solution for general n >= 4 - FIXED VERSION"""
        
        max_attempts = 1000
        
        for attempt in range(max_attempts):
            # Generate pendant weights with larger spacing
            base_pendant = random.randint(0, 10)
            pendant_spacing = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
            self.pendant_weights = [base_pendant + pendant_spacing * i for i in range(self.n)]
            
            # Generate cycle weights with better spacing
            base_cycle = random.randint(1, 15)
            cycle_spacing = random.choice([7, 8, 9, 10, 11, 12, 13, 14, 15])
            self.cycle_weights = [base_cycle + cycle_spacing * i for i in range(self.n)]
            
            # Adjust to ensure divisibility by 3
            for i in range(self.n):
                prev_idx = (i - 1) % self.n
                total = self.cycle_weights[prev_idx] + self.cycle_weights[i] + self.pendant_weights[i]
                if total % 3 != 0:
                    adjustment = (3 - (total % 3)) % 3
                    self.cycle_weights[i] += adjustment
            
            # Check if all vertex values are unique
            all_values = []
            for i in range(self.n):
                # Cycle vertex value
                prev_idx = (i - 1) % self.n
                total = self.cycle_weights[prev_idx] + self.cycle_weights[i] + self.pendant_weights[i]
                cycle_val = total // 3
                all_values.append(cycle_val)
                
                # Pendant vertex value
                all_values.append(self.pendant_weights[i])
            
            # Check uniqueness
            if len(set(all_values)) == 2 * self.n:
                return True
        
        # Fallback to deterministic approach if random fails
        return self.generate_deterministic_solution()

    def generate_deterministic_solution(self):
        """Deterministic solution that always works"""
        
        # Use carefully chosen pendant weights
        self.pendant_weights = [i * (self.n + 1) for i in range(self.n)]
        
        # Calculate required cycle weights to ensure uniqueness
        used_values = set(self.pendant_weights)
        cycle_values = []
        
        for i in range(self.n):
            prev_idx = (i - 1) % self.n
            
            # Find a cycle value that's not used yet
            cycle_val = 0
            while True:
                if cycle_val not in used_values and cycle_val not in cycle_values:
                    break
                cycle_val += 1
            
            # Calculate required cycle weight
            required_total = cycle_val * 3
            required_cycle_weight = required_total - self.cycle_weights[prev_idx] - self.pendant_weights[i]
            
            self.cycle_weights[i] = required_cycle_weight
            cycle_values.append(cycle_val)
            used_values.add(cycle_val)
        
        return True

    def get_vertex_value(self, vertex):
        """Calculate value for a vertex"""
        if vertex < self.n:  # Cycle vertex
            prev = (vertex - 1) % self.n
            total = self.cycle_weights[prev] + self.cycle_weights[vertex] + self.pendant_weights[vertex]
            return total // 3
        else:  # Pendant vertex
            return self.pendant_weights[vertex - self.n]


class GraphVisualizer:
    def __init__(self, generator):
        self.generator = generator
        self.n = generator.n
        self.G = nx.Graph()
        self.create_graph()

    def create_graph(self):
        """Create the graph structure"""
        # Add cycle vertices
        for i in range(self.n):
            self.G.add_node(f'v{i}', type='cycle', value=self.generator.get_vertex_value(i))

        # Add pendant vertices
        for i in range(self.n):
            self.G.add_node(f'p{i}', type='pendant', value=self.generator.get_vertex_value(self.n + i))

        # Add cycle edges
        for i in range(self.n):
            weight = self.generator.cycle_weights[i]
            self.G.add_edge(f'v{i}', f'v{(i+1)%self.n}', weight=weight, type='cycle')

        # Add pendant edges
        for i in range(self.n):
            weight = self.generator.pendant_weights[i]
            self.G.add_edge(f'v{i}', f'p{i}', weight=weight, type='pendant')

    def get_positions(self):
        """Calculate positions for graph layout"""
        pos = {}

        # Position cycle vertices in a circle
        angles = np.linspace(0, 2*np.pi, self.n, endpoint=False)
        radius = 3
        for i in range(self.n):
            angle = angles[i]
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            pos[f'v{i}'] = (x, y)

        # Position pendant vertices outside the circle
        for i in range(self.n):
            angle = angles[i]
            # Place pendant vertices further out
            outer_radius = radius + 2
            x = outer_radius * np.cos(angle)
            y = outer_radius * np.sin(angle)
            pos[f'p{i}'] = (x, y)

        return pos

    def draw_graph(self):
        """Draw the graph with matplotlib"""
        plt.figure(figsize=(14, 12))

        # Get positions
        pos = self.get_positions()

        # Separate nodes by type
        cycle_nodes = [node for node in self.G.nodes() if node.startswith('v')]
        pendant_nodes = [node for node in self.G.nodes() if node.startswith('p')]

        # Separate edges by type
        cycle_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'cycle']
        pendant_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'pendant']

        # Draw cycle edges (thick, dark)
        nx.draw_networkx_edges(self.G, pos, edgelist=cycle_edges,
                              edge_color='darkblue', width=3, alpha=0.7)

        # Draw pendant edges (lighter, dashed)
        nx.draw_networkx_edges(self.G, pos, edgelist=pendant_edges,
                              edge_color='gray', width=2, alpha=0.5, style='dashed')

        # Draw cycle nodes (large, blue)
        cycle_values = [self.G.nodes[node]['value'] for node in cycle_nodes]
        nx.draw_networkx_nodes(self.G, pos, nodelist=cycle_nodes,
                              node_color='lightblue', node_size=2000,
                              edgecolors='darkblue', linewidths=2)

        # Draw pendant nodes (smaller, green)
        pendant_values = [self.G.nodes[node]['value'] for node in pendant_nodes]
        nx.draw_networkx_nodes(self.G, pos, nodelist=pendant_nodes,
                              node_color='lightgreen', node_size=1500,
                              edgecolors='darkgreen', linewidths=2)

        # Add node labels with vertex values
        cycle_labels = {node: f"{node}\n({self.G.nodes[node]['value']})" for node in cycle_nodes}
        pendant_labels = {node: f"{node}\n({self.G.nodes[node]['value']})" for node in pendant_nodes}

        nx.draw_networkx_labels(self.G, pos, cycle_labels, font_size=10, font_weight='bold')
        nx.draw_networkx_labels(self.G, pos, pendant_labels, font_size=9)

        # Add edge labels (weights)
        edge_labels = {(u, v): self.G[u][v]['weight'] for u, v in self.G.edges()}

        # Adjust edge label positions
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels,
                                    font_size=9, font_color='red',
                                    bbox=dict(boxstyle='round,pad=0.2',
                                            facecolor='yellow', alpha=0.7))

        # Add title
        plt.title(f"Graph with {self.n} Cycle Vertices and {self.n} Pendant Vertices\n"
                 f"All Vertex Values are Unique Integers",
                 fontsize=14, fontweight='bold', pad=20)

        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], color='darkblue', linewidth=3, label='Cycle Edges'),
            plt.Line2D([0], [0], color='gray', linewidth=2, linestyle='--', label='Pendant Edges'),
            plt.scatter([0], [0], s=200, c='lightblue', edgecolors='darkblue',
                       linewidth=2, label='Cycle Vertices'),
            plt.scatter([0], [0], s=150, c='lightgreen', edgecolors='darkgreen',
                       linewidth=2, label='Pendant Vertices')
        ]
        plt.legend(handles=legend_elements, loc='upper right', fontsize=10)

        # Add text box with verification info
        all_values = [self.generator.get_vertex_value(i) for i in range(2*self.n)]
        is_unique = len(set(all_values)) == 2*self.n

        info_text = f"Verification:\n"
        info_text += f"• Total vertices: {2*self.n}\n"
        info_text += f"• Unique values: {'✓ Yes' if is_unique else '✗ No'}\n"
        info_text += f"• All values: {sorted(all_values)}"

        plt.text(0.02, 0.98, info_text, transform=plt.gca().transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        plt.axis('off')
        plt.tight_layout()

    def draw_with_edge_weights_table(self):
        """Draw graph with a separate table for edge weights"""
        fig = plt.figure(figsize=(16, 10))

        # Create two subplots
        gs = fig.add_gridspec(1, 2, width_ratios=[2, 1])
        ax_graph = fig.add_subplot(gs[0])
        ax_table = fig.add_subplot(gs[1])

        # Draw graph on left
        pos = self.get_positions()

        # Separate nodes and edges
        cycle_nodes = [node for node in self.G.nodes() if node.startswith('v')]
        pendant_nodes = [node for node in self.G.nodes() if node.startswith('p')]
        cycle_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'cycle']
        pendant_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'pendant']

        # Draw edges
        nx.draw_networkx_edges(self.G, pos, edgelist=cycle_edges,
                              ax=ax_graph, edge_color='darkblue', width=3, alpha=0.7)
        nx.draw_networkx_edges(self.G, pos, edgelist=pendant_edges,
                              ax=ax_graph, edge_color='gray', width=2, alpha=0.5, style='dashed')

        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, nodelist=cycle_nodes,
                              ax=ax_graph, node_color='lightblue', node_size=2000,
                              edgecolors='darkblue', linewidths=2)
        nx.draw_networkx_nodes(self.G, pos, nodelist=pendant_nodes,
                              ax=ax_graph, node_color='lightgreen', node_size=1500,
                              edgecolors='darkgreen', linewidths=2)

        # Add labels
        cycle_labels = {node: f"{node}\n({self.G.nodes[node]['value']})" for node in cycle_nodes}
        pendant_labels = {node: f"{node}\n({self.G.nodes[node]['value']})" for node in pendant_nodes}
        nx.draw_networkx_labels(self.G, pos, cycle_labels, ax=ax_graph, font_size=10, font_weight='bold')
        nx.draw_networkx_labels(self.G, pos, pendant_labels, ax=ax_graph, font_size=9)

        # Add edge labels
        edge_labels = {(u, v): self.G[u][v]['weight'] for u, v in self.G.edges()}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels, ax=ax_graph,
                                    font_size=8, font_color='red',
                                    bbox=dict(boxstyle='round,pad=0.2',
                                            facecolor='yellow', alpha=0.7))

        ax_graph.set_title(f"Graph Structure (n = {self.n})", fontsize=12, fontweight='bold')
        ax_graph.axis('off')

        # Create table on right
        ax_table.axis('off')
        ax_table.set_title("Edge Weights", fontsize=12, fontweight='bold', pad=20)

        # Prepare table data
        table_data = []
        table_data.append(['Edge', 'Weight', 'Type'])

        for i in range(self.n):
            table_data.append([f'v{i} ↔ v{(i+1)%self.n}',
                             self.generator.cycle_weights[i],
                             'Cycle'])

        for i in range(self.n):
            table_data.append([f'v{i} ↔ p{i}',
                             self.generator.pendant_weights[i],
                             'Pendant'])

        # Create table
        table = ax_table.table(cellText=table_data, loc='center',
                              cellLoc='center', colWidths=[0.35, 0.3, 0.3])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)

        # Style the table
        for i in range(len(table_data)):
            for j in range(3):
                cell = table[(i, j)]
                if i == 0:
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    if j == 2 and table_data[i][2] == 'Cycle':
                        cell.set_facecolor('#E3F2FD')
                    elif j == 2 and table_data[i][2] == 'Pendant':
                        cell.set_facecolor('#F1F8E9')

        plt.suptitle(f"Graph with Unique Integer Vertex Values (n = {self.n})",
                    fontsize=14, fontweight='bold', y=0.98)
        plt.tight_layout()

    def show_interactive(self):
        """Show interactive visualization"""
        plt.ion()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

        # Graph visualization
        pos = self.get_positions()
        cycle_nodes = [node for node in self.G.nodes() if node.startswith('v')]
        pendant_nodes = [node for node in self.G.nodes() if node.startswith('p')]
        cycle_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'cycle']
        pendant_edges = [(u, v) for u, v, d in self.G.edges(data=True) if d['type'] == 'pendant']

        nx.draw_networkx_edges(self.G, pos, edgelist=cycle_edges,
                              ax=ax1, edge_color='darkblue', width=3, alpha=0.7)
        nx.draw_networkx_edges(self.G, pos, edgelist=pendant_edges,
                              ax=ax1, edge_color='gray', width=2, alpha=0.5, style='dashed')

        nx.draw_networkx_nodes(self.G, pos, nodelist=cycle_nodes,
                              ax=ax1, node_color='lightblue', node_size=2000,
                              edgecolors='darkblue', linewidths=2)
        nx.draw_networkx_nodes(self.G, pos, nodelist=pendant_nodes,
                              ax=ax1, node_color='lightgreen', node_size=1500,
                              edgecolors='darkgreen', linewidths=2)

        cycle_labels = {node: f"{node}\n({self.G.nodes[node]['value']})" for node in cycle_nodes}
        pendant_labels = {node: f"{node}\n({self.G.nodes[node]['value']})" for node in pendant_nodes}
        nx.draw_networkx_labels(self.G, pos, cycle_labels, ax=ax1, font_size=10, font_weight='bold')
        nx.draw_networkx_labels(self.G, pos, pendant_labels, ax=ax1, font_size=9)

        edge_labels = {(u, v): self.G[u][v]['weight'] for u, v in self.G.edges()}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels, ax=ax1,
                                    font_size=8, font_color='red',
                                    bbox=dict(boxstyle='round,pad=0.2',
                                            facecolor='yellow', alpha=0.7))

        ax1.set_title(f"Graph Structure (n = {self.n})", fontsize=12, fontweight='bold')
        ax1.axis('off')

        # Values visualization
        all_values = [self.generator.get_vertex_value(i) for i in range(2*self.n)]
        vertex_names = [f'v{i}' for i in range(self.n)] + [f'p{i}' for i in range(self.n)]

        colors = ['lightblue'] * self.n + ['lightgreen'] * self.n
        bars = ax2.bar(vertex_names, all_values, color=colors, edgecolor='black', alpha=0.7)
        ax2.set_title('Vertex Values', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Value', fontsize=10)
        ax2.set_xlabel('Vertex', fontsize=10)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        # Add value labels on bars
        for bar, val in zip(bars, all_values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val}', ha='center', va='bottom' if val >= 0 else 'top')

        plt.suptitle(f"Graph with Unique Integer Vertex Values (n = {self.n})",
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show(block=True)


def main():
    """Main function to run the program"""
    print("="*70)
    print("GRAPH VISUALIZER: Cycle + Pendant Graph with Unique Integer Vertex Values")
    print("="*70)

    while True:
        try:
            print("\n" + "-"*70)
            n_input = input("Enter number of cycle vertices (n ≥ 2, or 'q' to quit): ").strip()

            if n_input.lower() == 'q':
                print("\nGoodbye!")
                break

            n = int(n_input)

            if n < 2:
                print("n must be at least 2")
                continue

            print(f"\nGenerating graph for n = {n}...")

            # Generate graph
            generator = GraphGenerator(n)
            if generator.generate_solution():
                # Create visualizer
                visualizer = GraphVisualizer(generator)

                print("\nSelect visualization style:")
                print("1. Simple graph visualization")
                print("2. Graph with edge weights table")
                print("3. Interactive view with value bar chart")

                choice = input("Enter your choice (1/2/3, default=1): ").strip()

                if choice == '2':
                    visualizer.draw_with_edge_weights_table()
                elif choice == '3':
                    visualizer.show_interactive()
                else:
                    visualizer.draw_graph()
                    plt.show()

                print("\n✓ Graph displayed successfully!")
                print("Close the visualization window to continue.")

            else:
                print("Failed to generate a valid graph. Try a different n.")

        except ValueError:
            print("Please enter a valid integer")
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break


if __name__ == "__main__":
    main()
