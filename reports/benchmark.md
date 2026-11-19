# Benchmark report

| algorithm | input | size | repeats | min_ms | mean_ms | median_ms | growth | expected |
|---|---|---|---|---|---|---|---|---|
| insertion_sort | random | 100 | 5 | 0.080 | 0.081 | 0.081 |  | O(n^2) |
| insertion_sort | random | 1000 | 5 | 9.759 | 9.897 | 9.819 | 121.7 | O(n^2) |
| insertion_sort | random | 10000 | 5 | 1099.489 | 1102.284 | 1101.787 | 111.4 | O(n^2) |
| insertion_sort | sorted | 100 | 5 | 0.004 | 0.004 | 0.004 |  | O(n^2) |
| insertion_sort | sorted | 1000 | 5 | 0.051 | 0.052 | 0.052 | 11.6 | O(n^2) |
| insertion_sort | sorted | 10000 | 5 | 0.558 | 0.567 | 0.568 | 10.9 | O(n^2) |
| insertion_sort | reversed | 100 | 5 | 0.160 | 0.161 | 0.160 |  | O(n^2) |
| insertion_sort | reversed | 1000 | 5 | 18.756 | 18.782 | 18.762 | 116.7 | O(n^2) |
| insertion_sort | reversed | 10000 | 5 | 2316.515 | 2325.240 | 2320.255 | 123.8 | O(n^2) |
| insertion_sort | nearly_sorted | 100 | 5 | 0.016 | 0.017 | 0.017 |  | O(n^2) |
| insertion_sort | nearly_sorted | 1000 | 5 | 1.303 | 1.307 | 1.308 | 77.9 | O(n^2) |
| insertion_sort | nearly_sorted | 10000 | 5 | 134.071 | 135.210 | 134.933 | 103.5 | O(n^2) |
| insertion_sort | many_duplicates | 100 | 5 | 0.067 | 0.069 | 0.068 |  | O(n^2) |
| insertion_sort | many_duplicates | 1000 | 5 | 8.964 | 9.011 | 9.033 | 130.9 | O(n^2) |
| insertion_sort | many_duplicates | 10000 | 5 | 982.790 | 998.433 | 1002.689 | 110.8 | O(n^2) |
| merge_sort | random | 100 | 5 | 0.053 | 0.056 | 0.054 |  | O(n log n) |
| merge_sort | random | 1000 | 5 | 0.678 | 0.698 | 0.709 | 12.4 | O(n log n) |
| merge_sort | random | 10000 | 5 | 9.450 | 9.629 | 9.637 | 13.8 | O(n log n) |
| merge_sort | sorted | 100 | 5 | 0.039 | 0.040 | 0.040 |  | O(n log n) |
| merge_sort | sorted | 1000 | 5 | 0.474 | 0.485 | 0.483 | 12.2 | O(n log n) |
| merge_sort | sorted | 10000 | 5 | 6.044 | 6.163 | 6.129 | 12.7 | O(n log n) |
| merge_sort | reversed | 100 | 5 | 0.042 | 0.044 | 0.043 |  | O(n log n) |
| merge_sort | reversed | 1000 | 5 | 0.484 | 0.487 | 0.487 | 11.0 | O(n log n) |
| merge_sort | reversed | 10000 | 5 | 6.321 | 6.384 | 6.370 | 13.1 | O(n log n) |
| merge_sort | nearly_sorted | 100 | 5 | 0.044 | 0.045 | 0.045 |  | O(n log n) |
| merge_sort | nearly_sorted | 1000 | 5 | 0.601 | 0.605 | 0.605 | 13.3 | O(n log n) |
| merge_sort | nearly_sorted | 10000 | 5 | 8.229 | 8.322 | 8.291 | 13.7 | O(n log n) |
| merge_sort | many_duplicates | 100 | 5 | 0.052 | 0.055 | 0.054 |  | O(n log n) |
| merge_sort | many_duplicates | 1000 | 5 | 0.646 | 0.650 | 0.651 | 11.9 | O(n log n) |
| merge_sort | many_duplicates | 10000 | 5 | 8.641 | 8.691 | 8.655 | 13.4 | O(n log n) |

growth: how many times mean time grew from the previous size
