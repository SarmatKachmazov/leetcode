from typing import List, Optional, Set

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def modifiedList(self, nums: List[int], head: Optional['ListNode']) -> Optional['ListNode']:
        """
        Remove all nodes from the linked list whose values appear in `nums`,
        and return the head of the modified list.

        Idea (simple and robust):
            - Put all values from `nums` into a hash set for O(1) lookups.
            - Use a dummy node pointing to head. This safely handles cases where
              the original head must be removed.
            - Walk the list with a pointer `cur` starting at dummy:
                * If `cur.next.val` is in the set, skip that node:
                    cur.next = cur.next.next
                * else move `cur` forward.

        Example:
            nums = [1,2,3], head = 1 -> 2 -> 3 -> 4 -> 5
            remove 1,2,3  =>  4 -> 5

            nums = [1], head = 1 -> 2 -> 1 -> 2 -> 1 -> 2
            remove 1s     =>  2 -> 2 -> 2

        Time complexity:  O(n + m)
            n = length of the list, m = length of nums.
            Building the set is O(m), one pass over the list is O(n).
        Space complexity: O(m)
            For the hash set of values to delete.
        """
        to_delete: Set[int] = set(nums)

        dummy = ListNode(0, head)
        cur = dummy
        while cur.next:
            if cur.next.val in to_delete:
                cur.next = cur.next.next   # remove node
            else:
                cur = cur.next
        return dummy.next