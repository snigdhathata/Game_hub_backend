# 🧠 Reinforcement Learning Game Suite – Backend

> An interactive game platform combining AI-based Reinforcement Learning agents and traditional multiplayer games, exposed through a Flask API.

---

## 🚀 Project Overview

This backend powers a Game Suite that demonstrates practical implementation of:

- 🎯 Q-Learning
- 🎮 Policy Gradient (REINFORCE)
- 🤝 Multiplayer game logic
- 🌐 Flask-based API integration

The backend handles AI agent training, game execution, and communication with the frontend.

---

## 🎮 Games Implemented

### 🧠 AI-Based Games

| Game         | Algorithm Used              | Description |
|-------------|----------------------------|-------------|
| GridWorld   | Q-Learning                  | Agent learns optimal path to reach goal using reward-based updates |
| FrozenLake  | Q-Learning (Gymnasium)      | Agent learns safe path in a stochastic environment |
| CartPole    | Policy Gradient (REINFORCE) | Neural network policy (PyTorch) balances pole |

---

### 🤝 Multiplayer / Logic-Based Games

- ♟ Chess
- 🔴 Four In A Row
- 🔢 Number Guess

These demonstrate classical algorithm design and multiplayer logic handling.

---

## 🏗 Tech Stack

- Python
- Flask
- Flask-CORS
- NumPy
- Gymnasium
- PyTorch
- Gunicorn (Production Server)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/rl-game-suite-backend.git
cd rl-game-suite-backend
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Server

```bash
python app.py
```

Server runs at:

```
http://localhost:5000
```

---

## 📡 Backend Responsibilities

- Train Reinforcement Learning agents
- Execute multiplayer logic
- Return training results
- Handle API requests from frontend
- Manage cross-origin requests (CORS)

---

## 🧪 Reinforcement Learning Concepts Demonstrated

- Markov Decision Process (MDP)
- Q-Table Updates
- Epsilon-Greedy Exploration
- Policy Gradient Optimization
- Reward Function Engineering
- Convergence Behaviour

---

## 🎓 Academic Purpose

Developed as a final-year undergraduate project to demonstrate:

- Strong understanding of Reinforcement Learning algorithms
- Practical AI agent implementation
- Backend-Frontend system integration
- Real-time environment interaction

---

## 📌 Future Improvements

- Deep Q-Network (DQN)
- Persistent model saving/loading
- Training performance graphs
- Leaderboard system
- Docker containerization

---

## 👨‍💻 Author

**Isaac Pranit**  
Final Year Computer Science Student  

---

## 🌟 Highlights

- Combines AI-based learning and traditional game logic
- Implements both value-based and policy-based RL methods
- Clean modular backend architecture
- Deployment-ready configuration
