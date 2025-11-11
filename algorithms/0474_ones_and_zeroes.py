from typing import List

class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        """
        Find the maximum number of strings that can be formed with at most
        `m` zeros and `n` ones.

        Each string in `strs` consists only of '0' and '1'.
        You can choose any subset of these strings, as long as the total number
        of zeros and ones used does not exceed (m, n).

        Approach (0/1 Knapsack with two dimensions):
            - Let dp[i][j] = the maximum number of strings that can be chosen
              with at most i zeros and j ones.
            - For each string, count its zeros (z) and ones (o).
            - Update dp in reverse order to avoid reusing the same string:
                dp[i][j] = max(dp[i][j], dp[i - z][j - o] + 1)
              for i in range(m, z-1, -1), j in range(n, o-1, -1).

        Example:
            strs = ["10", "0001", "111001", "1", "0"]
            m = 5, n = 3
            Output = 4
            Explanation:
                We can form {"10", "0001", "1", "0"}.

        Time complexity:  O(L * m * n),  where L = len(strs)
        Space complexity: O(m * n)
        """
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for s in strs:
            z = s.count('0')
            o = len(s) - z
            for i in range(m, z - 1, -1):
                for j in range(n, o - 1, -1):
                    dp[i][j] = max(dp[i][j], dp[i - z][j - o] + 1)

        return dp[m][n]