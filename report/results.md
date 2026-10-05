# Experiment Results

N=8; base seed=6150; sideways limit=100 consecutive moves.

Restart limit: unlimited (until success).

Each trial count is an independent batch. Steps count queen moves across all attempts; restarts exclude the initial attempt. Rates measure complete trials. Unlimited restart runs continue until solved, so their 100% success is a consequence of the stopping rule. N/A means the group has no observations.

## Hill Climbing

| Trials | Successes | Failures | Success % | Failure % | Avg steps (all) | Avg steps (success) | Avg steps (failure) | Avg restarts (all) | Avg restarts (success) | Avg restarts (failure) |
|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 7 | 43 | 14.00 | 86.00 | 3.16 | 4.29 | 2.98 | 0.00 | 0.00 | 0.00 |
| 100 | 10 | 90 | 10.00 | 90.00 | 3.14 | 4.40 | 3.00 | 0.00 | 0.00 | 0.00 |
| 200 | 28 | 172 | 14.00 | 86.00 | 3.33 | 4.25 | 3.19 | 0.00 | 0.00 | 0.00 |
| 500 | 54 | 446 | 10.80 | 89.20 | 3.16 | 4.11 | 3.04 | 0.00 | 0.00 | 0.00 |
| 1000 | 133 | 867 | 13.30 | 86.70 | 3.18 | 4.10 | 3.04 | 0.00 | 0.00 | 0.00 |
| 1500 | 195 | 1305 | 13.00 | 87.00 | 3.20 | 4.06 | 3.07 | 0.00 | 0.00 | 0.00 |

## Hill Climbing with Sideways

| Trials | Successes | Failures | Success % | Failure % | Avg steps (all) | Avg steps (success) | Avg steps (failure) | Avg restarts (all) | Avg restarts (success) | Avg restarts (failure) |
|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 48 | 2 | 96.00 | 4.00 | 23.40 | 22.15 | 53.50 | 0.00 | 0.00 | 0.00 |
| 100 | 92 | 8 | 92.00 | 8.00 | 21.53 | 17.63 | 66.38 | 0.00 | 0.00 | 0.00 |
| 200 | 193 | 7 | 96.50 | 3.50 | 21.14 | 20.21 | 46.71 | 0.00 | 0.00 | 0.00 |
| 500 | 465 | 35 | 93.00 | 7.00 | 21.81 | 18.58 | 64.63 | 0.00 | 0.00 | 0.00 |
| 1000 | 939 | 61 | 93.90 | 6.10 | 22.27 | 19.80 | 60.26 | 0.00 | 0.00 | 0.00 |
| 1500 | 1413 | 87 | 94.20 | 5.80 | 21.79 | 19.16 | 64.49 | 0.00 | 0.00 | 0.00 |

## Random Restart

| Trials | Successes | Failures | Success % | Failure % | Avg steps (all) | Avg steps (success) | Avg steps (failure) | Avg restarts (all) | Avg restarts (success) | Avg restarts (failure) |
|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 50 | 0 | 100.00 | 0.00 | 21.92 | 21.92 | N/A | 5.74 | 5.74 | N/A |
| 100 | 100 | 0 | 100.00 | 0.00 | 22.58 | 22.58 | N/A | 5.99 | 5.99 | N/A |
| 200 | 200 | 0 | 100.00 | 0.00 | 26.05 | 26.05 | N/A | 7.21 | 7.21 | N/A |
| 500 | 500 | 0 | 100.00 | 0.00 | 21.68 | 21.68 | N/A | 5.76 | 5.76 | N/A |
| 1000 | 1000 | 0 | 100.00 | 0.00 | 22.99 | 22.99 | N/A | 6.14 | 6.14 | N/A |
| 1500 | 1500 | 0 | 100.00 | 0.00 | 23.16 | 23.16 | N/A | 6.25 | 6.25 | N/A |

## Random Restart with Sideways

| Trials | Successes | Failures | Success % | Failure % | Avg steps (all) | Avg steps (success) | Avg steps (failure) | Avg restarts (all) | Avg restarts (success) | Avg restarts (failure) |
|---|---|---|---|---|---|---|---|---|---|---|
| 50 | 50 | 0 | 100.00 | 0.00 | 24.90 | 24.90 | N/A | 0.04 | 0.04 | N/A |
| 100 | 100 | 0 | 100.00 | 0.00 | 22.38 | 22.38 | N/A | 0.05 | 0.05 | N/A |
| 200 | 200 | 0 | 100.00 | 0.00 | 23.92 | 23.92 | N/A | 0.06 | 0.06 | N/A |
| 500 | 500 | 0 | 100.00 | 0.00 | 23.63 | 23.63 | N/A | 0.07 | 0.07 | N/A |
| 1000 | 1000 | 0 | 100.00 | 0.00 | 22.05 | 22.05 | N/A | 0.05 | 0.05 | N/A |
| 1500 | 1500 | 0 | 100.00 | 0.00 | 22.51 | 22.51 | N/A | 0.06 | 0.06 | N/A |

