\ Model PLMO Knapsack (10, 10)
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  z - 11 w[0] - 4.75 w[1] - 7.25 w[2] - 3.5 w[3] - 7.25 w[4] - 11 w[5]
   - 4.75 w[6] - 4.75 w[7] - 4.25 w[8] - 7.75 w[9] + 12 Constant
Subject To
 u0: z + 8 w[0] + 3.5 w[1] + 6 w[2] + 4.5 w[4] + 7 w[5] + 3.5 w[6] + w[7]
   + 2 w[8] + 7.5 w[9] >= 8
 u1: z + 3 w[0] + 1.25 w[1] + 1.25 w[2] + 3.5 w[3] + 2.75 w[4] + 4 w[5]
   + 1.25 w[6] + 3.75 w[7] + 2.25 w[8] + 0.25 w[9] >= 4
 R2: 7 w[0] + 2 w[1] + 8 w[2] + 9 w[3] + 7 w[4] + 4 w[5] + 7 w[6] + 4 w[7]
   + 4 w[8] + 3 w[9] <= 27.5
Bounds
 Constant = 1
Binaries
 w[0] w[1] w[2] w[3] w[4] w[5] w[6] w[7] w[8] w[9]
End
