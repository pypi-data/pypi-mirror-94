<!--
SPDX-License-Identifier: GPL-3.0-only
SPDX-FileCopyrightText: 2020 Vincent Lequertier <vi.le@autistici.org>
-->

# A fair PyTorch loss function

[![REUSE status](https://api.reuse.software/badge/gitlab.com/vi.le/fair-loss)](https://api.reuse.software/info/gitlab.com/vi.le/fair-loss)
[![PyPI version](https://img.shields.io/pypi/v/fair-loss.svg)](https://pypi.python.org/pypi/fair-loss)

The goal of this loss function is to take fairness into account during the training of a
PyTorch model. It works by adding a fairness measure to a regular loss value,
following this equation:

<img src="https://latex.codecogs.com/svg.latex?\Large&space;loss%20=%20loss%20+%20\lambda{{\sum_{i=0}^{k}w_i%20f_i(y_{pred},%20y_{true})}%20\over%20\min\limits_{%20\forall%20i\in%20[0,k[}%20f_i(y_{pred},%20y_{true})}" />

## Installation

```bash
pip install fair-loss
```

## Example

```python
import torch
from fair_loss import FairLoss

model = torch.nn.Sequential(torch.nn.Linear(5, 1), torch.nn.ReLU())
data = torch.randint(0, 5, (100, 5), dtype=torch.float, requires_grad=True)
y_true = torch.randint(0, 5, (100, 1), dtype=torch.float)
y_pred = model(data)
# Let's say the sensitive attribute is in the second dimension
dim = 1
criterion = FairLoss(torch.nn.MSELoss(), data[:, dim].detach().unique(), accuracy)
loss = criterion(data[:, dim], y_pred, y_true)
loss.backward()
```

## Documentation

See [the documentation](http://vi.le.gitlab.io/fair-loss/).
