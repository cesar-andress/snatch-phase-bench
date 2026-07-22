# MS-TCN failure analysis (M3)

## Seed 42
- Over-segmentation videos: 0
- Missing short-phase videos: 23
- Extra fragments (total): 2
- Lowest recall classes: [('5', 0.8675496688741722), ('7', 0.885009030704395), ('3', 0.8888888888888888)]
- Highest boundary MAE transitions: [('catch->recovery', 7.92), ('turnover->catch', 1.2592592592592593), ('setup->first_pull', 1.125), ('second_pull->turnover', 0.8181818181818182), ('first_pull->transition', 0.6060606060606061)]

## Seed 123
- Over-segmentation videos: 0
- Missing short-phase videos: 27
- Extra fragments (total): 0
- Lowest recall classes: [('2', 0.8513853904282116), ('6', 0.8803191489361702), ('4', 0.8823529411764706)]
- Highest boundary MAE transitions: [('catch->recovery', 2.36), ('setup->first_pull', 1.5), ('turnover->catch', 1.4230769230769231), ('transition->second_pull', 0.696969696969697), ('first_pull->transition', 0.6666666666666666)]

## Seed 456
- Over-segmentation videos: 1
- Missing short-phase videos: 3
- Extra fragments (total): 8
- Lowest recall classes: [('3', 0.8888888888888888), ('5', 0.890728476821192), ('2', 0.8967254408060453)]
- Highest boundary MAE transitions: [('catch->recovery', 3.28), ('setup->first_pull', 1.28125), ('turnover->catch', 1.1481481481481481), ('second_pull->turnover', 0.6363636363636364), ('first_pull->transition', 0.6060606060606061)]

## Cross-seed instability
- Unstable videos: 33
