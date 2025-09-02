'''
week 2

topics:
    1. Analysis of algorithms
    2. Calculating complexity
    3. Serching in a list:
        a. naive search
        b. binary search
    4. Selection sort
    5. Insertion sort
    6. Merge sort and analysis
    
programming assignments:
    1. Write a Python function combinationSort(strList) that takes a list of 
        unique strings strList as an argument, where each string is a 
        combination of a letter from a to z and a number from to 99, the 
        initial character in string being the letter. For example a23 d5 q99 
        are some strings in this format. This function should sorts the list 
        and return two lists (11, 12) in the order mentioned below.
        L1: First list should contain all strings sorted in ascending order 
        with respect to the first character only. All strings with same initial 
        character should be in the same order as in the original list.
        12: In the list 11 above, sort the strings starting with same 
        character, in descending order with respect to the number formed by 
        the remaining characters.
    2. Complete the python function find Largest(L) below, which accepts a 
       list L of unique numbers, that are sorted(ascending) and rotated n 
       times, where n is unknown, and returns the largest number in list L. 
       Rotating list [2, 4, 5, 7, 8] one time gives us list [8, 2, 4, 5, 7],
       and rotating the second time gives list [7, 8, 2, 4, 5] and so on. Try 
       to give an O(log n) solution Hint: One of the O(log n) solutions can be 
       implemented using binary search and using 'first or last' element to 
       know, the direction of searching further.
    3. Merging two sorted arrays in place.
        Given a custom implementation of list named MyList. On MyList objects 
        you can perform read operations similar to the in-build lists in 
        Python, example use A[i] to read element at index i in MyList object
        A. The only possible operation that you can use to edit data in MyList
        objects is by calling the swap method. For instance, A. 
        swap(indexA, B, indexs) will swap values at A[indexA] and B[indexB] 
        and A. swap(index1, A, index2) will swap values at A[index1] and 
        A[index2], where indexa, indexß, indexl, index2 are all integers.
        Complete the Python function mergeInPlace (A, B) that accepts two 
        MyLists A and B containing integers that are sorted in ascending order
        and merges them in place(without using any other list) such that after 
        merging, A and B are still sorted in ascending order with the smallest 
        element of both MyLists as the first element of A.
'''

from week_1 import Timer
import random

def naive_search(L : list[int],
                v : int) -> int:
    '''
    naively searches for the target in the given list
    returns index of the target if found else -1
    Complexity :
        best case : O(1)
        avg case : O(n)
        worst case : O(n)
    '''
    for i in range(len(L)):
      if v == L[i]:
        return i
    return -1

def binary_search(L : list[int],
                 v : int) -> int:
    """
    Binary search on sorted list.
    Returns index if found, else -1 
    Complexity : 
        best case : O(1)
        avg case : O(log n)
        worst case : O(log n)
    """
    low = 0
    high = len(L) - 1
    while low <= high: 
        mid = (low + high) // 2
        if L[mid ] < v:
            low = mid  + 1
        elif L[mid ] > v:
            high = mid  - 1
        else:
            return mid
    return -1

def selection_sort(L : list[int]) -> None:
    """
    Selection sort 
    in-place
    not stable
    requires min. no. of swaps comparitively
    Complexity: 
        best case : O(n^2)
        avg case : O(n^2)
        worst case : O(n^2)
    """
    n = len(L)
    if n < 1:
        return(L)
    for i in range(n):
        minpos = i
        for j in range(i+1,n):
            if L[j] < L[minpos]:
                minpos = j
        (L[i],L[minpos]) = (L[minpos],L[i])

def insertion_sort(L):
    """
    Insertion sort 
    in-place
    stable
    good for already sorted data
    Complexity: 
        best case : O(n), already sorted list
        avg case : O(n^2)
        worst case : O(n^2)
    """
    n = len(L)
    if n < 1:
        return(L)
    for i in range(n):
        j = i
        while(j > 0 and L[j] < L[j-1]):
            (L[j],L[j-1]) = (L[j-1],L[j])
            j = j-1
            
def merge_sort(arr: list[int]) -> list[int]:
    """
    Merge sort (recursive)
    not in-place
    stable
    Complexity: 
        best case : O(n log n)
        avg case : O(n log n)
        worst case : O(n log n)
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    """Helper function for merge_sort"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result

def combinationSort(strList : list[str]) -> tuple[list[str], list[str]]:
    '''programming assignment - 1'''
    l1 = sorted(strList, key = lambda x: x[0])
    l2 = sorted(strList, key = lambda x: (x[0], -int(x[1:])))
    return (l1, l2)

def findLargest(L : list[int]) -> int:
    '''programming assignment - 2'''
    low = 0
    high = len(L) - 1

    if L[low] <= L[high]:
        return L[high]

    while low <= high:
        mid = (low + high) // 2

        if mid < high and L[mid] > L[mid + 1]:
            return L[mid]
        if mid > low and L[mid] < L[mid - 1]:
            return L[mid - 1]

        if L[mid] >= L[low]:
            low = mid + 1
        else:
            high = mid - 1

    return -1

def mergeInPlace(A : list[int],
                 B : list[int]) -> None:
    '''programming assignment - 3'''
    for i in range(len(A)):
        if A[i] > B[0]:
            A.swap(i, B, 0)
            
        for j in range(len(B)-1):
            if B[j] > B[j+1]:
                B.swap(j, B, j+1)
            else:
                break



if __name__ == "__main__":
    def test_naive_search():
        L = [1, 3, 5, 7, 9]
        assert naive_search(L, 1) == 0
        assert naive_search(L, 9) == 4
        assert naive_search(L, 4) == -1
        print("naive_search passed!")

    def test_binary_search():
        L = [1, 3, 5, 7, 9]
        assert binary_search(L, 1) == 0
        assert binary_search(L, 7) == 3
        assert binary_search(L, 10) == -1
        print("binary_search passed!")

    def test_selection_sort():
        L = [64, 25, 12, 22, 11]
        selection_sort(L)
        assert L == [11, 12, 22, 25, 64]
        print("selection_sort passed!")

    def test_insertion_sort():
        L = [5, 2, 9, 1, 5, 6]
        insertion_sort(L)
        assert L == [1, 2, 5, 5, 6, 9]
        print("insertion_sort passed!")

    def test_merge_sort():
        arr = [38, 27, 43, 3, 9, 82, 10]
        sorted_arr = merge_sort(arr)
        assert sorted_arr == sorted(arr)
        print("merge_sort passed!")

    def test_combinationSort():
        strs = ["a23", "a12", "b99", "b5", "c10"]
        L1, L2 = combinationSort(strs)
        assert L1 == ["a23", "a12", "b99", "b5", "c10"]  # sorted by letter, stable
        assert L2 == ["a23", "a12", "b99", "b5", "c10"]  # within each letter, numbers desc
        print("combinationSort passed!")

    def test_findLargest():
        L = [7, 8, 2, 4, 5]
        assert findLargest(L) == 8
        L = [2, 4, 5, 7, 8]
        assert findLargest(L) == 8
        L = [8, 2, 4, 5, 7]
        assert findLargest(L) == 8
        print("findLargest passed!")

    def test_mergeInPlace():
        class MyList(list):
            def swap(self, i, other, j):
                self[i], other[j] = other[j], self[i]

        A = MyList([1, 5, 9])
        B = MyList([2, 3, 7, 10])
        mergeInPlace(A, B)
        assert A == [1, 2, 3]
        assert B == [5, 7, 9, 10]
        print("mergeInPlace passed!")
    
    def compare_week2_performance():
        n = 2000
        data = [random.randint(1, 10000) for _ in range(n)]
        sorted_data = sorted(data)
        target = data[n // 2]  # pick a mid element
    
        tests = [
            ("naive_search", lambda: naive_search(data, target)),
            ("binary_search", lambda: binary_search(sorted_data, target)),
            ("selection_sort", lambda: selection_sort(data)),
            ("insertion_sort", lambda: insertion_sort(data)),
            ("merge_sort", lambda: merge_sort(data)),
        ]
    
        for name, func in tests:
            timer = Timer()
            timer.start()
            result = func()
            timer.stop()
            print(f"{name:<15} | Time: {timer} | Sample Output: {str(result)[:50]}...")

    # Run all tests
    test_naive_search()
    test_binary_search()
    test_selection_sort()
    test_insertion_sort()
    test_merge_sort()
    test_combinationSort()
    test_findLargest()
    test_mergeInPlace()
    compare_week2_performance()
    print("\nAll tests passed successfully!")
