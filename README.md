# Alpha-Toe-Zero

An implementation of DeepMind's AlphaZero algorithm for Tic-Tac-Toe and 4×4×4 Qubic (3D Tic-Tac-Toe). This project combines Monte Carlo Tree Search (MCTS) with deep neural networks for self-play reinforcement learning—no human data required.

## Project Structure

```
alpha-toe/
├── 2d/                  # 3×3 Tic-Tac-Toe implementation
│   ├── main.py          # Training pipeline & AlphaZero core
│   ├── play.py          # Interactive CLI game
│   ├── tournament.py    # Elo tournament between models
│   └── export_onnx.py   # Export models to ONNX format
├── 3d/                  # 4×4×4 Qubic implementation
│   ├── qubic.py         # 3D AlphaZero with 3D conv net
│   └── qubic_export.py  # Export 3D models to ONNX
├── teach/               # Interactive web application
│   ├── src/             # JavaScript modules (game, MCTS, UI)
│   └── public/          # ONNX models for browser inference
├── docs/                # Documentation & notebooks
│   ├── TECHNICAL_DOCUMENTATION.md
│   ├── report.md
│   └── *.ipynb          # Interactive explainers
└── models/              # Trained model checkpoints
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/nottherealsanta/alpha-toe.git
cd alpha-toe

# Install dependencies (requires Python 3.11+)
pip install -e .
# or with uv
uv sync
```

### Train a Model

```bash
# Train 3×3 Tic-Tac-Toe
cd 2d
python main.py

# Train 4×4×4 Qubic
cd 3d
python qubic.py
```

### Play Against the AI

```bash
# CLI game against trained model
cd 2d
python play.py --model-path ../models/alphazero_iter_40.pth
```

### Run the Web Demo

```bash
cd teach
npm install
npm run dev
```

Then open http://localhost:5173 to play 4×4×4 Qubic against the AI in your browser.

## How It Works

### AlphaZero Algorithm

The implementation follows the AlphaZero approach:

1. **Neural Network** - A ResNet predicts:
   - **Value head**: Expected game outcome (-1 to +1)
   - **Policy head**: Move probabilities for each action

2. **Monte Carlo Tree Search** - Guided by the neural network:
   - Selection via PUCT formula balancing exploration/exploitation
   - Expansion using policy network priors
   - Backup propagating values through the tree

3. **Self-Play Training**:
   - Generate games using MCTS
   - Train network on (state, policy, value) tuples
   - Repeat with improved network

### Key Hyperparameters

| Parameter | 3×3 Value | 4×4×4 Value | Description |
|-----------|-----------|-------------|-------------|
| `N_SIMULATIONS` | 100 | 100 | MCTS simulations per move |
| `N_GAMES` | 200 | 64 | Self-play games per iteration |
| `C_PUCT` | 1.0 | 1.0 | Exploration constant |
| `NUM_RES_BLOCKS` | 4 | 4 | Residual blocks in network |
| `REPLAY_CAPACITY` | 50,000 | 200,000 | Training sample buffer |

### Data Augmentation

- **3×3**: 8 dihedral symmetries (rotations + reflections)
- **4×4×4**: 24 or 48 cube symmetries (rotations ± reflections)

## Tournament & Evaluation

Compare models via Elo-rated round-robin tournaments:

```bash
cd 2d
python tournament.py \
    --models ../models/alphazero_iter_0.pth ../models/alphazero_iter_40.pth \
    --games-per-pair 20 \
    --mcts-simulations 200
```

Results are saved to CSV for analysis.

Based on the AlphaZero algorithm by DeepMind:
- [Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm](https://arxiv.org/abs/1712.01815)
- [Mastering the game of Go without human knowledge](https://www.nature.com/articles/nature24270)
