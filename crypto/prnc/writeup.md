# Challenge Solution

## Understand the Code

1. `permute(seed, flag)` is an implementation of a Lehmer code. It converts the given `seed` to a permutation then permutes `flag` with that permutation.
- permutes `flag` based on `seed` deterministically; the same `seed` maps to the same permutation

2. `permute_n_times(n, flag)` runs `permute(seed, flag)` `n` times, each time generating a random number `seed` using a `linear_congruential_generator` (LCG) which is initially seeded using a `random_device`.
- permutes `flag` `n` times pseudo-randomly; if the LCG outputs the same `seed`, it will apply the same permutation to `flag`

3. `check(n, flag)` runs `permute_n_times(n, flag)` 10 times. If, after all 10 function calls, `flag` remains unchanged, it outputs the flag.
- due to the random nature of the problem, to ensure the user's value of `n` definitely works (or works with high probability), it is checked 10 times
- it remains to find a positive number `n` such that we can guarantee `permute_n_times(n, flag)` leaves `flag` unchanged

## Understand the Problem

1. `random_device` cannot be predicted, so the LCG's initial seed cannot be either. However, note that the LCG has a period of 358; regardless of initial seed, it will output the same numbers -- and hence apply the same permutations to `flag` -- every 358 calls. So, if we consider composing these first 358 permutations into one permutation `P`, for `n = 358 * k`, `permute_n_times(n, flag)` will apply `P` `k` times to `flag`. In particular, `P` is the same each of the `k` times, although random (depending on the initial seed).

2. Notice that if you repeatedly apply `P` to `flag`, it will eventually return to its original state, regardless of what `P` is (pigeonhole principle). Let `p` be the smallest positive number for which applying `P` `p` times to `flag` returns it to its original state. Since applying `P` `p` times leaves `flag` unchanged, applying `P` to `flag` any multiple of `p` times also leaves it unchanged. So, we should set `k` to some multiple of `p`.

3. Due to the randomness of the initial seed and thus `P`, we can never know `p` exactly. However, assume we know that `p` can only take on the values 4, 5, or 6. Then, setting `k` to `lcm(4, 5, 6) = 60` would work. In general, we should set `k` to a number which is divisible by all possible values of `p`. It remains to find these values.

4. Consider the following permutation of 6 elements (1-indexed): `1 -> 1`, `2 -> 3`, `3 -> 2`, `4 -> 5`, `5 -> 6`, `6 -> 4`, where `i -> j` means, after applying this permutation, the character at index `i` is now at index `j`. For example, permuting "ABCDEF" yields "ACBFDE". Notice that we can decompose this permutation into 3 cycles -- `1 -> 1`, `2 -> 3 -> 2` and `4 -> 5 -> 6 -> 4`-- of length 1, 2 and 3 respectively, where a cycle's length is the number of distinct indices it contains. Notice now that within a cycle, its period is equal to its length. Now, when multiple cycles are considered in parallel, the combined period of these cycles is the lcm of their lengths. So, this permutation's period is `lcm(1, 2, 3) = 6`. In general, a permutation's period is the lcm of the lengths of all cycles it contains.

4. Running the program with some random `n` (probably) yields a permutation of `flag`. In particular, its length is now known to be 12, and the sum of the lengths of all cycles within `P` must sum to 12. More specifically, every cycle length is between 1 to 12, inclusive. So, across all possible `P`, the cycle lengths will attain every value from 1 to 12, so the lcm of all possible `p` is `lcm(1, 2, 3, ..., 12)`.

5. Inputting `n = 358 * lcm(1, 2, 3, ..., 12) = 9923760` and waiting yields the flag.

# Comments

1. The exact mapping in `permute(seed, flag)` of `seed` to `flag` does not matter.

2. The choice of an LCG does not matter. All pseudorandom number generators (even mt19937) have a period and will eventually give the same numbers. However, an LCG allows the period to be set to something small so the solution does not take too long to run.

3. The solution should take at most a minute to run.