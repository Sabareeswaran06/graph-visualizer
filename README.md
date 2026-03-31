# 🔷 Graph Visualizer: Cycle + Pendant Graph with Unique Vertex Values

## 📌 Overview

This project generates and visualizes a special type of graph consisting of:

* A **cycle of n vertices**
* Each cycle vertex connected to a **pendant vertex**
* Edge weights assigned such that:

  * Every vertex gets a **computed integer value**
  * ✅ **All vertex values are unique**

This is useful for:

* Graph theory research
* Algorithm visualization
* Mathematical modeling
* Educational demonstrations

---

## 🧠 Core Idea

Each cycle vertex value is computed as:

```
Value(v_i) = (w_{i-1} + w_i + p_i) / 3
```

Where:

* `w_i` = cycle edge weight
* `p_i` = pendant edge weight

Pendant vertex value:

```
Value(p_i) = p_i
```

👉 The algorithm ensures:

* All values are integers
* All values are **unique**

---

## ⚙️ Features

✅ Automatic graph generation for any `n ≥ 2`
✅ Handles special cases (`n = 2, 3`)
✅ Random + deterministic solution fallback
✅ Ensures **unique vertex values**
✅ Multiple visualization modes:

1. Simple graph visualization
2. Graph + edge weight table
3. Interactive graph + bar chart

---

## 🛠️ Technologies Used

* Python 🐍
* Matplotlib 📊
* NetworkX 🌐
* NumPy 🔢

---

## 📂 Project Structure

```
graph-visualizer/
│
├── main.py     # Main program
├── README.md   # Documentation
```

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/graph-visualizer.git
cd graph-visualizer
```

### 2. Install dependencies

```bash
pip install matplotlib networkx numpy
```

### 3. Run the program

```bash
python main.py
```

---

## 🎮 Usage

* Enter number of cycle vertices (`n ≥ 2`)
* Choose visualization type:

  * `1` → Simple graph
  * `2` → Graph + table
  * `3` → Interactive mode

---

## 👨‍💻 Author

**Sabareeswaran S**
