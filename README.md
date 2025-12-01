# **Martingale Simulation Framework**

A modular **object-oriented simulation framework** for exploring martingale-based betting strategies on a variety of stochastic games (Bernoulli processes, random walks, custom games, etc.).
It provides:

* **Customizable strategies** (Martingale, Fixed, Double-on-Loss, etc.)
* **Extendable game models** (Bernoulli, Random Walk, custom distributions)
* **Full history tracking** using pandas
* **Statistical analysis** of performance (EV, variance, drawdown, etc.)
* **Clean OOP design** (Strategy / Game / Simulation / History)

Perfect for students, researchers, or developers who want to explore martingales, expectation, gambler’s ruin, and stochastic processes.



## 🚀 **Features**



### Built-In Games

* **BernoulliProcess** — win/lose game with probability ( p ).
* **RandomWalkGame** — return +1 if position inside interval ([a,b]), else -1.
* Easily extendable for Markov chains, Gaussian increments, etc.

### Built-In Strategies

* **FixedBettingStrategy** — constant bet size
* **DoubleOnLossStrategy** (Martingale) — doubles after each loss
* Add your own strategies by subclassing `Strategy`.

### Analytics

* Expected value
* Maximum drawdown
* Variance of gains
* Capital curve plotting (green for gains, red for losses)



## 📦 **Installation**

Clone the repository:

```bash
git clone https://github.com/desire-del/martingale-sim.git
cd martingale-sim
```

Install dependencies:

```bash
uv sync
```

---

## 🔧 **How It Works**

### Example: Running Multiple Strategies on a Bernoulli Game

```python
from src.strategies import FixedBettingStrategy, DoubleOnLossStrategy
from src.games import BernoulliProcess
from src.models import Simulation

sim = Simulation(
    strategies=[
        FixedBettingStrategy(bet_amount=10),
        DoubleOnLossStrategy(base_bet=5)
    ],
    game=BernoulliProcess(p=0.5),
    max_bet=1_000_000,
    start_value=1000
)

results = sim.run(rounds=1000)
```

Retrieve statistics:

```python
for name, result in results.items():
    print(name, result.compute_statistics())
```

Plot gain curve:

```python
result.plot_gain_over_time()
```

---

## 🧩 **Extending the Framework**

### Creating a New Game

```python
class MyCustomGame(Game):
    def play_round(self, history):
        return np.random.choice([-1, 1], p=[0.3, 0.7])
```

### Creating a New Strategy

```python
class MyStrategy(Strategy):
    def decide_bet(self, history):
        if history.records.empty:
            return 10
        return history.last_record()["bet"] + 1
```

---

## 📁 **Project Structure**

```
.
├── LICENSE
├── pyproject.toml          # uv project configuration (PEP 621)
├── README.md               # Documentation
├── src/
│   ├── games.py            # Game processes (Bernoulli, Random Walk, etc.)
│   ├── models.py           # History, Simulation, Result, Game/Strategy base classes
│   ├── strategies.py       # Implemented strategies (Martingale, Fixed Bet, etc.)
│   └── __init__.py
├── test.ipynb              # Interactive notebook for experiments
└── uv.lock                 # uv dependency lock file

```

---

## 🧪 **Future Improvements**

* Kelly and fractional Kelly strategies
* Multivariate Markov games
* Portfolio-style allocation between strategies
* Interactive dashboard (Streamlit)

---

## 📜 **License**

MIT License — feel free to modify and use!

