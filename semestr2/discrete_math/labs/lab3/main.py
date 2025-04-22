import tkinter as tk
from tkinter import filedialog, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def read_matrix_from_file(filename):

    with open(filename, 'r') as f: return [list(map(int, line.strip().split())) for line in f]

def shortest_paths_toposort(matrix, start):

    n = len(matrix)
    G = nx.DiGraph()
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != 0 and matrix[i][j] != float('inf'):
                G.add_edge(i, j, weight=matrix[i][j])

    try: top_order = list(nx.topological_sort(G))
    except nx.NetworkXUnfeasible: raise ValueError("Граф містить цикл. Алгоритм працює тільки для DAG.")
    
    print(top_order)

    dist = [float('inf')] * n
    dist[start] = 0
    path = [-1] * n

    for u in top_order:
        for v in G.successors(u):
            weight = G[u][v]['weight']
            if dist[v] > dist[u] + weight:
                dist[v] = dist[u] + weight
                path[v] = u

    return G, dist, path

def reconstruct_path(path, start, end):

    if path[end] == -1: return []
    result = [end]

    while result[-1] != start: result.append(path[result[-1]])

    return result[::-1]

def draw_graph(G, shortest_path):
    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=600)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)

def run_toposort_from_input():
    try:
        matrix = eval(entry_matrix.get("1.0", "end"))
        start = int(entry_start.get())
        end = int(entry_end.get())
        G, dist, path = shortest_paths_toposort(matrix, start)
        path_seq = reconstruct_path(path, start, end)
        ax.clear()
        draw_graph(G, path_seq)
        canvas.draw()
        label_result.config(text=f"Найкоротша відстань: {dist[end]}\nШлях: {path_seq}")
    except Exception as e:
        messagebox.showerror("Помилка", str(e))

def load_matrix_from_file():

    filename = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if filename:
        try:
            matrix = read_matrix_from_file(filename)
            entry_matrix.delete("1.0", "end")
            entry_matrix.insert("1.0", str(matrix))
        except Exception as e:
            messagebox.showerror("Помилка", str(e))

# GUI
root = tk.Tk()
root.title("Найкоротший шлях (топологічне сортування)")

tk.Label(root, text="Матриця ваг (наприклад: [[0,5,0],[0,0,3],[0,0,0]])").pack()
entry_matrix = tk.Text(root, height=5, width=40)
entry_matrix.pack()

# Додати підтримку Ctrl+C, Ctrl+V, Ctrl+X
entry_matrix.bind("<Control-c>", lambda e: entry_matrix.event_generate("<<Copy>>"))
entry_matrix.bind("<Control-C>", lambda e: entry_matrix.event_generate("<<Copy>>"))
entry_matrix.bind("<Control-v>", lambda e: entry_matrix.event_generate("<<Paste>>"))
entry_matrix.bind("<Control-V>", lambda e: entry_matrix.event_generate("<<Paste>>"))
entry_matrix.bind("<Control-x>", lambda e: entry_matrix.event_generate("<<Cut>>"))
entry_matrix.bind("<Control-X>", lambda e: entry_matrix.event_generate("<<Cut>>"))

tk.Button(root, text="Завантажити з файлу", command=load_matrix_from_file).pack()

frame_inputs = tk.Frame(root)
frame_inputs.pack()
tk.Label(frame_inputs, text="Початкова вершина: ").grid(row=0, column=0)
entry_start = tk.Entry(frame_inputs, width=5)
entry_start.grid(row=0, column=1)

tk.Label(frame_inputs, text="Кінцева вершина: ").grid(row=0, column=2)
entry_end = tk.Entry(frame_inputs, width=5)
entry_end.grid(row=0, column=3)

tk.Button(root, text="Знайти найкоротший шлях", command=run_toposort_from_input).pack()

label_result = tk.Label(root, text="")
label_result.pack()

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

root.mainloop()