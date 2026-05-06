# 🧠 Interactive Gradient Descent

An interactive 3D visualization tool to understand **gradient descent optimization** on complex loss landscapes — directly in your browser.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maxalaar/Interactive_Gradient_Descent/blob/main/main.ipynb)


---

## ✨ Features

- **3D loss surface** — visualize classic and custom loss landscapes in real time
- **Click-to-optimize** — place a starting point and watch the optimizer run
- **Multi-optimizer comparison** — SGD, Adam, RMSProp and more, side by side
- **Benchmark functions** — Rosenbrock, Rastrigin, Himmelblau, and others

---

## ▶️ Quickstart — Google Colab

The fastest way to run the project, no installation required:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Maxalaar/Interactive_Gradient_Descent/blob/main/main.ipynb)

> Click the badge above → the notebook opens directly in Google Colab → run all cells.

---

## 💻 Run Locally

For the best performance (faster rendering, full responsiveness), run locally:

```bash
# 1. Clone the repo
git clone https://github.com/Maxalaar/Interactive_Gradient_Descent.git
cd Interactive_Gradient_Descent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
python main.py
```

Then open your browser at: [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## 🗂️ Project Structure

```
├── main.ipynb                    # Jupyter notebook (Colab-ready)
├── main.py                       # Dash app entry point
├── loss_function.py              # Loss function definitions
├── compute_loss_landscape.py     # Landscape grid computation
├── compute_optimization_path.py  # Optimizer trajectory computation
├── build_surface.py              # 3D surface builder
├── create_loss_landscape_figure.py
├── optimizer.py                  # Optimizer wrappers
├── callbacks/                    # Dash callbacks
├── layout/                       # Dash layout components
├── assets/                       # Static assets
└── requirements.txt
```

---

## 📦 Requirements

See [`requirements.txt`](requirements.txt). Main dependencies:

- `dash` / `plotly` — interactive web UI
- `numpy` — numerical computations
- `torch` — autograd for optimizer trajectories

---

## 📄 License

MIT — feel free to use, share, and contribute.