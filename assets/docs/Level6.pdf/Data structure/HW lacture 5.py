def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]
        merge_sort(left)
        merge_sort(right)
        arr[:] = sorted(left + right)
        
arr = [12, 4, 7, 3, 15, 8, 1, 10, 6, 14, 2, 9]
print("Original array:", arr)

merge_sort(arr)
print("Sorted array:", arr)
