\ Model PLMO Knapsack (10, 10)
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  z - 4.6 w[0] - 2 w[1] - 4.3 w[2] - 4.8 w[3] - 4.1 w[4] - 4.9 w[5]
   - 4.6 w[6] - 2.9 w[7] - 1.4 w[8] - 1.4 w[9] + 5.6 Constant
Subject To
 u0: z + 3.8 w[0] + 0.8 w[1] + 3.6 w[2] + 3 w[3] + 3 w[4] + 3.8 w[5]
   + 2.8 w[6] + 1.2 w[7] + 1.4 w[8] + 0.8 w[9] >= 3.8
 u1: z + 0.8 w[0] + 1.2 w[1] + 0.7 w[2] + 1.8 w[3] + 1.1 w[4] + 1.1 w[5]
   + 1.8 w[6] + 1.7 w[7] + 0.6 w[9] >= 1.8
 R2: 9 w[0] + 2 w[1] + 9 w[3] + 3 w[4] + 8 w[6] + 9 w[7] + w[8] + 7 w[9]
   <= 24
Bounds
 Constant = 1
Binaries
 w[0] w[1] w[2] w[3] w[4] w[5] w[6] w[7] w[8] w[9]
End
