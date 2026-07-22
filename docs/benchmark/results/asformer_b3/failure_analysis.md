# ASFormer failure analysis (B3)

## Seed 42
- Over-segmentation videos: 0
- Missing short-phase videos: 18
- Extra fragments (total): 5
- Lowest recall classes: [('3', 0.8717948717948718), ('5', 0.8741721854304636), ('2', 0.9168765743073047)]
- Highest boundary MAE transitions: [('catch->recovery', 2.76), ('setup->first_pull', 1.15625), ('turnover->catch', 1.1538461538461537), ('first_pull->transition', 0.5454545454545454), ('transition->second_pull', 0.48484848484848486)]

## Seed 123
- Over-segmentation videos: 1
- Missing short-phase videos: 5
- Extra fragments (total): 3
- Lowest recall classes: [('6', 0.8776595744680851), ('5', 0.8807947019867549), ('2', 0.8866498740554156)]
- Highest boundary MAE transitions: [('catch->recovery', 2.4), ('setup->first_pull', 1.28125), ('turnover->catch', 1.08), ('first_pull->transition', 0.6060606060606061), ('transition->second_pull', 0.3939393939393939)]

## Seed 456
- Over-segmentation videos: 0
- Missing short-phase videos: 29
- Extra fragments (total): 0
- Lowest recall classes: [('3', 0.8461538461538461), ('6', 0.848404255319149), ('5', 0.8807947019867549)]
- Highest boundary MAE transitions: [('catch->recovery', 2.32), ('setup->first_pull', 1.46875), ('turnover->catch', 1.12), ('second_pull->turnover', 0.7575757575757576), ('first_pull->transition', 0.6363636363636364)]

## Cross-seed instability
- Unstable videos: 33
