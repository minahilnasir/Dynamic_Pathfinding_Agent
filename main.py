import tkinter as tk
from tkinter import ttk
import heapq
import time
import math
import random

CELL_SIZE = 28

COLORS = {
    "empty": "#ffffff",
    "wall": "#2f2f2f",
    "start": "#00c853",
    "goal": "#d50000",
    "visited": "#81d4fa",
    "frontier": "#ffeb3b",
    "path": "#00e676",
    "agent": "#00e676",
    "grid": "#cccccc"
}


class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Pathfinding Agent")
        self.root.configure(bg="#f0f0f0")

        # runtime
        self.grid = []
        self.walls = set()
        self.rows = 0
        self.cols = 0
        self.start = None
        self.goal = None
        self.path = []
        self.running = False
        self.after_id = None

        # search state (stepwise)
        self.open_set = []
        self.g = {}
        self.came = {}
        self.visited = set()
        self.start_time = None

        self._build_controls()
        self._build_metrics()
        self._build_canvas()

        # default grid
        self.rows_entry.insert(0, "20")
        self.cols_entry.insert(0, "30")
        self.create_grid()

    # -------------------- UI --------------------
    def _build_controls(self):
        ctrl = tk.Frame(self.root, bg="#f0f0f0")
        ctrl.pack(pady=8)

        tk.Label(ctrl, text="Rows:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.rows_entry = tk.Entry(ctrl, width=4)
        self.rows_entry.pack(side=tk.LEFT)

        tk.Label(ctrl, text="Cols:", bg="#f0f0f0").pack(side=tk.LEFT)
        self.cols_entry = tk.Entry(ctrl, width=4)
        self.cols_entry.pack(side=tk.LEFT)

        ttk.Button(ctrl, text="Create Grid", command=self.create_grid).pack(side=tk.LEFT, padx=4)
        ttk.Button(ctrl, text="Generate Maze", command=self.generate_maze).pack(side=tk.LEFT, padx=4)

        tk.Label(ctrl, text="Algorithm:", bg="#f0f0f0").pack(side=tk.LEFT, padx=4)
        self.algorithm_var = tk.StringVar(value="A*")
        ttk.Combobox(ctrl, textvariable=self.algorithm_var,
                    values=["A*", "Greedy"],
                    state="readonly", width=8).pack(side=tk.LEFT)

        tk.Label(ctrl, text="Heuristic:", bg="#f0f0f0").pack(side=tk.LEFT, padx=4)
        self.heuristic_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(ctrl, textvariable=self.heuristic_var,
                    values=["Manhattan", "Euclidean"],
                    state="readonly", width=12).pack(side=tk.LEFT)

        self.dynamic_var = tk.BooleanVar()
        tk.Checkbutton(ctrl, text="Dynamic Mode", variable=self.dynamic_var,
                       bg="#f0f0f0").pack(side=tk.LEFT, padx=6)

        self.density_var = tk.DoubleVar(value=0.3)
        tk.Label(ctrl, text="Density:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Scale(ctrl, variable=self.density_var, from_=0, to=1,
                 resolution=0.05, orient=tk.HORIZONTAL, length=100).pack(side=tk.LEFT)

        ttk.Button(ctrl, text="Start Search", command=self.start_search).pack(side=tk.LEFT, padx=6)
        ttk.Button(ctrl, text="Stop", command=self.stop).pack(side=tk.LEFT)

    def _build_metrics(self):
        self.metrics = tk.Label(
            self.root,
            text="Nodes: 0 | Cost: 0 | Time: 0 ms | Status: Idle",
            bg="#f0f0f0"
        )
        self.metrics.pack()

    def _build_canvas(self):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(frame, bg=COLORS["empty"])
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.on_click)

    # -------------------- GRID --------------------
    def create_grid(self):
        self.stop()
        self.canvas.delete("all")

        self.rows = int(self.rows_entry.get())
        self.cols = int(self.cols_entry.get())

        self.grid = []
        self.walls = set()

        width = self.cols * CELL_SIZE
        height = self.rows * CELL_SIZE
        self.canvas.config(width=width, height=height)

        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=COLORS["empty"],
                    outline=COLORS["grid"]
                )
                row.append(rect)
            self.grid.append(row)

        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)

        self.color(self.start, COLORS["start"])
        self.color(self.goal, COLORS["goal"])

    def color(self, pos, color):
        r, c = pos
        self.canvas.itemconfig(self.grid[r][c], fill=color)

    # -------------------- WALL TOGGLE --------------------
    def on_click(self, event):
        if self.running:
            return
        c = event.x // CELL_SIZE
        r = event.y // CELL_SIZE

        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return

        pos = (r, c)
        if pos in (self.start, self.goal):
            return

        if pos in self.walls:
            self.walls.remove(pos)
            self.color(pos, COLORS["empty"])
        else:
            self.walls.add(pos)
            self.color(pos, COLORS["wall"])

    # -------------------- MAZE --------------------
    def generate_maze(self):
        if not self.grid:
            return
        self.stop()
        self.walls = set()

        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if pos in (self.start, self.goal):
                    continue
                if random.random() < self.density_var.get():
                    self.walls.add(pos)
                    self.color(pos, COLORS["wall"])
                else:
                    self.color(pos, COLORS["empty"])

    # -------------------- HEURISTIC --------------------
    def heuristic(self, a, b):
        if self.heuristic_var.get() == "Manhattan":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    # -------------------- NEIGHBORS --------------------
    def neighbors(self, node):
        r, c = node
        result = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if (nr, nc) not in self.walls:
                    result.append((nr, nc))
        return result

    # -------------------- STEPWISE SEARCH --------------------
    def start_search(self):
        if self.running:
            return

        self._soft_reset()

        self.open_set = [(0, self.start)]
        self.g = {self.start: 0}
        self.came = {}
        self.visited = set()
        self.running = True
        self.start_time = time.perf_counter()

        self._step_search()

    def _step_search(self):
        if not self.running:
            return

        if not self.open_set:
            elapsed = round((time.perf_counter() - self.start_time) * 1000, 2)
            self._update_metrics(len(self.visited), 0, elapsed, "No Path")
            self.running = False
            return

        _, current = heapq.heappop(self.open_set)

        if current in self.visited:
            self.after_id = self.root.after(80, self._step_search)
            return

        self.visited.add(current)

        elapsed = round((time.perf_counter() - self.start_time) * 1000, 2)
        self._update_metrics(len(self.visited), 0, elapsed, "Searching")

        if current not in (self.start, self.goal):
            self.color(current, COLORS["visited"])

        if current == self.goal:
            self.path = self.reconstruct(self.came)
            self._anim_agent(self.path, len(self.visited), len(self.path) - 1, elapsed)
            return

        for nb in self.neighbors(current):
            ng = self.g[current] + 1
            if ng < self.g.get(nb, float("inf")):
                self.g[nb] = ng
                self.came[nb] = current
                f = ng + self.heuristic(nb, self.goal)
                heapq.heappush(self.open_set, (f, nb))

                if nb not in (self.start, self.goal):
                    self.color(nb, COLORS["frontier"])

        self.after_id = self.root.after(80, self._step_search)

    def reconstruct(self, came):
        path = []
        cur = self.goal
        while cur in came:
            path.append(cur)
            cur = came[cur]
        path.append(self.start)
        path.reverse()
        return path

    # -------------------- MOVEMENT --------------------
    def _anim_agent(self, path, nodes, cost, elapsed):
        idx = [0]

        def step():
            if not self.running:
                return
            if idx[0] >= len(path):
                self.running = False
                self._update_metrics(nodes, cost, elapsed, "Goal Reached")
                return

            pos = path[idx[0]]

            self.spawn_dynamic()

            if pos in self.walls:
                new = self._replan(pos)
                if not new:
                    self._update_metrics(nodes, 0, elapsed, "Blocked")
                    self.running = False
                    return
                path[:] = new
                idx[0] = 0
                return

            self.canvas.create_rectangle(
                pos[1] * CELL_SIZE + 4,
                pos[0] * CELL_SIZE + 4,
                (pos[1] + 1) * CELL_SIZE - 4,
                (pos[0] + 1) * CELL_SIZE - 4,
                fill=COLORS["agent"],
                outline=""
            )

            if idx[0] > 0:
                prev = path[idx[0] - 1]
                if prev not in (self.start, self.goal):
                    self.color(prev, COLORS["path"])

            idx[0] += 1
            self.after_id = self.root.after(120, step)

        step()

    def _replan(self, start):
        return self._run_astar_from(start)[0] if self.algorithm_var.get() == "A*" else self._run_gbfs_from(start)

    # -------------------- DYNAMIC --------------------
    def spawn_dynamic(self):
        if not self.dynamic_var.get():
            return
        if random.random() < 0.05:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            pos = (r, c)
            if pos in (self.start, self.goal):
                return
            self.walls.add(pos)
            self.color(pos, COLORS["wall"])

    def _run_astar_from(self, start):
        open_set = [(0, start)]
        g = {start: 0}
        came = {}
        seen = set()

        while open_set:
            _, cur = heapq.heappop(open_set)
            if cur in seen:
                continue
            seen.add(cur)

            if cur == self.goal:
                return self.reconstruct(came), list(seen)

            for nb in self.neighbors(cur):
                ng = g[cur] + 1
                if ng < g.get(nb, float("inf")):
                    g[nb] = ng
                    came[nb] = cur
                    heapq.heappush(open_set, (ng + self.heuristic(nb, self.goal), nb))

        return None, list(seen)

    def _run_gbfs_from(self, start):
        open_set = [(self.heuristic(start, self.goal), start)]
        came = {}
        seen = set()

        while open_set:
            _, cur = heapq.heappop(open_set)
            if cur in seen:
                continue
            seen.add(cur)

            if cur == self.goal:
                return self.reconstruct(came)

            for nb in self.neighbors(cur):
                if nb not in seen:
                    came[nb] = cur
                    heapq.heappush(open_set, (self.heuristic(nb, self.goal), nb))

        return None

    # -------------------- HELPERS --------------------
    def _soft_reset(self):
        for r in range(self.rows):
            for c in range(self.cols):
                pos = (r, c)
                if pos not in self.walls:
                    self.color(pos, COLORS["empty"])

    def stop(self):
        self.running = False
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

    def _update_metrics(self, nodes, cost, ms, status):
        self.metrics.config(
            text=f"Nodes: {nodes} | Cost: {cost} | Time: {ms} ms | Status: {status}"
        )


def main():
    root = tk.Tk()
    root.geometry("1100x700")
    PathfindingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()