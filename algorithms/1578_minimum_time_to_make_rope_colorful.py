from typing import List

class Solution:
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        """
        Returns the minimum total time needed so that
        no two adjacent balloons have the same color.

        Approach:
        - Traverse the string and track the total time of the current same-color group
          and the maximum time inside that group.
        - When the color changes, add (group_sum - group_max) to the answer.
        - Do the same for the last group.

        Time: O(n)
        Space: O(1)
        """
        n = len(colors)
        if n <= 1:
            return 0

        total_time = 0
        group_sum = neededTime[0]
        group_max = neededTime[0]

        for i in range(1, n):
            if colors[i] == colors[i - 1]:
                # Still in the same color group
                group_sum += neededTime[i]
                group_max = max(group_max, neededTime[i])
            else:
                # End of the current group
                total_time += group_sum - group_max
                # Start a new group
                group_sum = neededTime[i]
                group_max = neededTime[i]

        # Add the last group
        total_time += group_sum - group_max
        return total_time