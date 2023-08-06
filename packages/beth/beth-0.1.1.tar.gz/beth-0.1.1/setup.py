# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beth', 'beth.models', 'beth.players']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.4.0,<2.0.0',
 'comet-ml>=3.3.3,<4.0.0',
 'ipykernel>=5.4.3,<6.0.0',
 'ipython>=7.20.0,<8.0.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'jupyter>=1.0.0,<2.0.0',
 'matplotlib>=3.3.4,<4.0.0',
 'numpy>=1.20.1,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'torch>=1.7.1,<2.0.0',
 'tqdm>=4.56.2,<5.0.0']

setup_kwargs = {
    'name': 'beth',
    'version': '0.1.1',
    'description': 'Open source chess AI engine',
    'long_description': '# beth\n![](https://images.chesscomfiles.com/uploads/v1/article/22924.4e040c11.668x375o.d12a4478e7d3@2x.jpeg)\nExperimenting with Game AI applied to chess\n\n## Idea\nIn this repo will be experiments around AI & chess. In particular Machine Learning applied to the chess game. <br>\nThe goal is to create: \n\n- Algorithms to play chess using Machine Learning, Reinforcement Learning & NLP\n- Auto-guide to help human learn and improve at playing chess\n- Adaptive AI to match the player ELO and make him improve\n\n> This repo is **under active development**\n\n\n## Features\n### Environment\n\n- [x] Experimenting with the [python chess](https://python-chess.readthedocs.io/en) library\n- [x] Implementing ``Game`` framework\n- [x] ``HumanPlayer`` to play chess in Jupyter notebook\n- [x] ``RandomPlayer`` the most simple bot to easily test out new ideas and debug\n- [ ] Read PGN files and load into ML algorithms\n- [ ] Measure ELO of an algorithm/AI, or any consistant metric of performance\n- [ ] Saving game as gif or video\n\n### Model utils\n- [x] Monitor algorithm performance using Comet.ml / tensorboard\n- [x] Saving algorithm weights to be reused\n- [x] Visualize probabilities to see best moves and if training worked\n- [ ] Transform game object into 3D tensor (2D dimension + one hot encoding of pieces positions)\n- [ ] Install, test, and integrate CodeCarbon\n- [ ] Train on Google Colab\n\n### Algorithms & approaches\n- [ ] AlphaGo approach: value function and policy function evaluation using Reinforcement Learning & MCTS\n- [ ] AlphaZero approach: self play competition\n- [ ] NLP approach: predicting next move using NLP techniques (LSTM, Transformers)\n  - [ ] LSTM / RNN / GRU\n  - [ ] Transformers\n  - [ ] Directly using Hugging Face ``transformers`` [library](https://huggingface.co/transformers/task_summary.html) \n- [ ] Hybrid techniques with both NLP-like + modeling the game as 3D tensor \n- [ ] GameAI techniques (minimax, rules-based)\n  - [ ] Super simple approach where at each step Random Play from a PGN file or list of moves. \n- [ ] Test connection to Game engines like stockfish\n\n## References\n- https://python-chess.readthedocs.io/en\n- https://lichess.org/\n- https://www.chess.com/games/\n\n### Sequential Deep Learning\n- https://pytorch.org/tutorials/beginner/transformer_tutorial.html\n\n### Game Databases\n- https://www.chess.com/games/\n- https://www.kaggle.com/datasnaek/chess\n\n### State of the art approaches\n- https://ai.facebook.com/blog/rebel-a-general-game-playing-ai-bot-that-excels-at-poker-and-more/\n  \n\n### Libraries\n- Deep Learning ``jax, trax, rlax, haiku and pytorch-lightning``\n- Monitoring (comet.ml, [livelossplot](https://github.com/stared/livelossplot), [tensorboard](https://pytorch.org/tutorials/recipes/recipes/tensorboard_with_pytorch.html))\n\n\n',
    'author': 'Theo Alves Da Costa',
    'author_email': 'theo.alves.da.costa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/theolvs/beth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.8,<4.0.0',
}


setup(**setup_kwargs)
