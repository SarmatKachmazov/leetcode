from typing import List, Dict
from collections import defaultdict
import heapq

class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:
        """
        Sliding window over length k. For each window we keep:
          - freq[v]: current frequency of value v in the window
          - L: top-x distinct values by (freq DESC, value DESC), as a min-heap (freq, value, v)
               (the "worst" among the top-x sits on top and can be evicted)
          - R: the rest, as a max-heap (-freq, -value, v)
          - inL[v]: whether v currently belongs to L
          - sumL: sum of v * freq[v] over all v in L
          - distinctCount: number of v with freq[v] > 0

        Tie-breaking rule: larger value is considered "more frequent" on equal freq.
        So ordering key is (freq, value) ascending in L, and (-freq, -value) in R.
        """

        n = len(nums)
        if k > n:
            return []

        # --- state ---
        freq: Dict[int, int] = defaultdict(int)
        inL: Dict[int, bool] = defaultdict(bool)
        L = []   # (freq, value, v)  -> min-heap (worst of the top-x on top)
        R = []   # (-freq, -value, v)-> max-heap (best of the rest on top)
        sumL = 0
        sizeL = 0
        distinctCount = 0

        # ---------- helpers ----------

        def push_L(v: int):
            """Push current snapshot of v into L (if freq>0 and not already in L)."""
            nonlocal sizeL, sumL
            if freq[v] <= 0 or inL[v]:
                return
            inL[v] = True
            sizeL += 1
            sumL += v * freq[v]
            heapq.heappush(L, (freq[v], v, v))

        def push_L_updated(v: int):
            """If v is already in L and its freq changed, push updated snapshot."""
            nonlocal sumL
            if not inL[v] or freq[v] <= 0:
                return
            # update contribution by +/- v is handled by callers
            heapq.heappush(L, (freq[v], v, v))

        def push_R(v: int):
            """Push current snapshot of v into R (if freq>0 and not in L)."""
            if freq[v] <= 0 or inL[v]:
                return
            heapq.heappush(R, (-freq[v], -v, v))

        def clean_L_top():
            """Return valid top of L or None (lazy deletion)."""
            while L:
                f, val, v = L[0]
                if not inL[v] or freq[v] != f or val != v:
                    heapq.heappop(L)
                    continue
                return (f, val, v)
            return None

        def clean_R_top():
            """Return valid top of R or None (lazy deletion)."""
            while R:
                nf, nv, v = R[0]
                f, val = -nf, -nv
                if inL[v] or freq[v] != f or val != v or f <= 0:
                    heapq.heappop(R)
                    continue
                return (nf, nv, v)  # stored negatives
            return None

        def move_best_R_to_L():
            """Move the best element from R to L (if any)."""
            nonlocal sizeL, sumL
            topR = clean_R_top()
            if not topR:
                return False
            heapq.heappop(R)
            _, _, v = topR
            # move v into L
            inL[v] = True
            sizeL += 1
            sumL += v * freq[v]
            heapq.heappush(L, (freq[v], v, v))
            return True

        def evict_worst_from_L():
            """Evict the worst element from L to R."""
            nonlocal sizeL, sumL
            topL = clean_L_top()
            if not topL:
                return False
            heapq.heappop(L)
            _, _, v = topL
            if inL[v]:  # still valid member
                inL[v] = False
                sizeL -= 1
                sumL -= v * freq[v]
                push_R(v)
            return True

        def swap_if_needed():
            """Ensure max(R) <= min(L) by (freq, value)."""
            while True:
                tL = clean_L_top()
                tR = clean_R_top()
                if not tL or not tR:
                    return
                fL, valL, vL = tL
                nfR, nvR, vR = tR
                fR, valR = -nfR, -nvR
                # If R's best is strictly better than L's worst → swap them
                if (fR, valR) > (fL, valL):
                    heapq.heappop(L)
                    heapq.heappop(R)
                    # move vL -> R
                    if inL[vL]:
                        inL[vL] = False
                        nonlocal sumL, sizeL
                        sumL -= vL * freq[vL]
                        sizeL -= 1
                        push_R(vL)
                    # move vR -> L
                    if not inL[vR] and freq[vR] > 0:
                        inL[vR] = True
                        sumL += vR * freq[vR]
                        sizeL += 1
                        heapq.heappush(L, (freq[vR], vR, vR))
                else:
                    return

        def rebalance():
            """Keep |L| = min(x, distinctCount) and order property."""
            need = min(x, distinctCount)
            # fill L
            while sizeL < need and move_best_R_to_L():
                pass
            # evict extras
            while sizeL > need:
                evict_worst_from_L()
            # order property
            swap_if_needed()

        def add_value(v: int):
            """Increase freq[v] by 1 and update structures."""
            nonlocal distinctCount, sumL
            prev = freq[v]
            if prev == 0:
                distinctCount += 1
            freq[v] = prev + 1
            if inL[v]:
                # contribution increases by v
                sumL += v
                push_L_updated(v)  # push updated snapshot
            else:
                # stays or goes to R for now
                push_R(v)
            rebalance()

        def remove_value(v: int):
            """Decrease freq[v] by 1 and update structures."""
            nonlocal distinctCount, sumL, sizeL
            prev = freq[v]
            if prev == 0:
                return  # shouldn't happen
            freq[v] = prev - 1
            if inL[v]:
                # contribution decreases by v
                sumL -= v
                if freq[v] == 0:
                    # fully leaves L
                    inL[v] = False
                    sizeL -= 1
                    distinctCount -= 1
                else:
                    # still in L, push updated snapshot
                    push_L_updated(v)
            else:
                if freq[v] == 0:
                    distinctCount -= 1
                else:
                    push_R(v)
            rebalance()

        # --- initialize first window ---
        for i in range(k):
            add_value(nums[i])
        ans = [sumL]

        # --- slide the window ---
        for i in range(k, n):
            out_v = nums[i - k]
            in_v = nums[i]
            if out_v == in_v:
                ans.append(sumL)
                continue
            remove_value(out_v)
            add_value(in_v)
            ans.append(sumL)

        return ans