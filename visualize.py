from graph.graph import build_graph

def export_graph_png(filename="call_graph.png"):
    graph = build_graph()
    
    # Generate PNG bytes from Mermaid
    png_bytes = graph.get_graph().draw_mermaid_png()
    
    # Save to file
    with open(filename, "wb") as f:
        f.write(png_bytes)

    print(f"Graph image saved as {filename}")


if __name__ == "__main__":
    export_graph_png()