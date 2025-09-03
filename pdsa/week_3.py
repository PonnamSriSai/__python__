'''
week 3 of pdsa course
topics:
    1. Quick sort and its analysis
    2. Linked list:
        a. Single Linked List
        b. Double Linked List
    3. Stack
    4. Queue
    
programming assignments:
    1. Crete a class for open addressing scheme using Quadrating probing
    2. A restaurant always prepares dishes with the most orders before others 
       with a lesser number of orders. Each dish in the restaurant menu has a 
       unique integer ID. The restaurant receives n orders in a particular 
       time period. The task is to find out the order of dish IDs according to
       which the restaurant will prepare them. Assume that restaurant has the 
       following unique dish IDs in its menu:
        [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]

       Write a function DishPrepareOrder(order_list) that accepts order_list
       in the form of a list of dish IDs and returns a list of dish IDs in the 
       order in which the restaurant will prepare them. If two or more dishes 
       have the same number of orders, then the dish which has a smaller ID 
       value will be prepared first.
    3. postfix evaluation
    4. Complete the below function reverse(root) that will reverse the linked 
       list with the first node passed as an argument, and return the first 
       node of the reversed list. Each node in the linked list is an object of 
       class Node.
'''

def quick_sort(L : list[int],
               l : int = 0,
               r : int = 0)-> None:
    '''
    quick sort
    inplace 
    not stable
    complexity :
        best case : O(n log n)
        avg case : O(n log n)
        worst case : O(n^2)
    '''
    if r == 0:
        r = len(L)-1
    if l >= r:
        return L
    
    # partition algo
    pivot, lower = L[l], l
    for i in range(l + 1, r + 1):
        if L[i] <= pivot:
            lower += 1
            L[i], L[lower] = L[lower], L[i]

    L[l], L[lower] = L[lower], L[l]
    quick_sort(L, l, lower - 1)
    quick_sort(L, lower + 1, r)        
 
class SNode:
    """Node of a singly linked list"""
    def __init__(self, data: int):
        self.data = data
        self.next = None

class SinglyLinkedList:
    """Singly Linked List implementation"""
    def __init__(self):
        self.head = None

    def is_empty(self) -> bool:
        return self.head is None

    def insert_at_beginning(self, data: int) -> None:
        new_node = SNode(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data: int) -> None:
        new_node = SNode(data)
        if self.is_empty():
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def insert_after(self, prev_data: int, data: int) -> bool:
        curr = self.head
        while curr and curr.data != prev_data:
            curr = curr.next
        if not curr:
            return False  # prev_data not found
        new_node = SNode(data)
        new_node.next = curr.next
        curr.next = new_node
        return True

    def delete(self, key: int) -> bool:
        curr = self.head
        prev = None
        while curr and curr.data != key:
            prev = curr
            curr = curr.next
        if not curr:
            return False  # key not found
        if prev:
            prev.next = curr.next
        else:
            self.head = curr.next
        return True
    
    def reverse(self):
        '''Reverses a singly linked list in-place.'''
        prev = None
        temp = self.head
        while temp is not None:
            _next = temp.next
            temp.next = prev
            prev = temp
            temp = _next            
            
        self.head = prev

    def search(self, key: int) -> bool:
        curr = self.head
        while curr:
            if curr.data == key:
                return True
            curr = curr.next
        return False

    def traverse(self) -> list[int]:
        elems = []
        curr = self.head
        while curr:
            elems.append(curr.data)
            curr = curr.next
        return elems

    def __str__(self) -> str:
        return " -> ".join(map(str, self.traverse())) if not self.is_empty() else "Empty List"

class DNode:
    """Node of a doubly linked list"""
    def __init__(self, data: int):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """Doubly Linked List implementation"""
    def __init__(self):
        self.head = None

    def is_empty(self) -> bool:
        return self.head is None

    def insert_at_beginning(self, data: int) -> None:
        new_node = DNode(data)
        new_node.next = self.head
        if self.head:
            self.head.prev = new_node
        self.head = new_node

    def insert_at_end(self, data: int) -> None:
        new_node = DNode(data)
        if self.is_empty():
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        new_node.prev = curr

    def insert_after(self, prev_data: int, data: int) -> bool:
        curr = self.head
        while curr and curr.data != prev_data:
            curr = curr.next
        if not curr:
            return False  # prev_data not found
        new_node = DNode(data)
        new_node.next = curr.next
        new_node.prev = curr
        if curr.next:
            curr.next.prev = new_node
        curr.next = new_node
        return True

    def delete(self, key: int) -> bool:
        curr = self.head
        while curr and curr.data != key:
            curr = curr.next
        if not curr:
            return False  # key not found
        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next  # deleting head
        if curr.next:
            curr.next.prev = curr.prev
        return True

    def search(self, key: int) -> bool:
        curr = self.head
        while curr:
            if curr.data == key:
                return True
            curr = curr.next
        return False

    def traverse_forward(self) -> list[int]:
        elems = []
        curr = self.head
        while curr:
            elems.append(curr.data)
            curr = curr.next
        return elems

    def traverse_backward(self) -> list[int]:
        elems = []
        curr = self.head
        if not curr:
            return elems
        # move to tail
        while curr.next:
            curr = curr.next
        # traverse backwards
        while curr:
            elems.append(curr.data)
            curr = curr.prev
        return elems

    def __str__(self) -> str:
        return " <-> ".join(map(str, self.traverse_forward())) if not self.is_empty() else "Empty List"


class Stack:
    """Stack implemented using singly linked list"""
    def __init__(self):
        self.top = None  # head pointer for stack

    def is_empty(self) -> bool:
        return self.top is None

    def push(self, data: int) -> None:
        """Push element on top of stack (O(1))"""
        new_node = SNode(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self) -> int:
        """Pop element from top of stack (O(1))"""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        popped = self.top.data
        self.top = self.top.next
        return popped

    def peek(self) -> int:
        """Return top element without removing (O(1))"""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.top.data

    def traverse(self) -> list[int]:
        """Return list of elements from top to bottom"""
        elems = []
        curr = self.top
        while curr:
            elems.append(curr.data)
            curr = curr.next
        return elems

    def __str__(self) -> str:
        return " -> ".join(map(str, self.traverse())) if not self.is_empty() else "Empty Stack"



class Queue:
    """Queue implemented using singly linked list"""
    def __init__(self):
        self.front = None  # points to first element
        self.rear = None   # points to last element

    def is_empty(self) -> bool:
        return self.front is None

    def enqueue(self, data: int) -> None:
        """Insert element at rear (O(1))"""
        new_node = SNode(data)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self) -> int:
        """Remove element from front (O(1))"""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        removed = self.front.data
        self.front = self.front.next
        if self.front is None:  # queue became empty
            self.rear = None
        return removed

    def peek(self) -> int:
        """Return front element without removing (O(1))"""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.front.data

    def traverse(self) -> list[int]:
        """Return list of all elements from front to rear"""
        elems = []
        curr = self.front
        while curr:
            elems.append(curr.data)
            curr = curr.next
        return elems

    def __str__(self) -> str:
        return " <- ".join(map(str, self.traverse())) if not self.is_empty() else "Empty Queue"

class Hashing:
    '''
    Quadratic hashing with open addressing
    h(k) = k % m
    quadratic probing:
        h(k, i) = h(k) + c1(i) + c2(i^2)   where c1, c2 are +ve integers
                                                 i = 0, 1, ..., (m-1)
    '''
    def __init__(self,c1,c2,m):
        self.hashtable = []
        for i in range(m):
            self.hashtable.append(None)     
        self.c1 = c1
        self.c2 = c2
        self.m = m
        
    def store_data(self, data : int) -> None:
        if None not in self.hashtable:
            print(f"hashtable is full... can't insert the {data = }")
            return
        
        base_hash = data % self.m
        for i in range(self.m):
            hash_index = (base_hash + self.c1*i + self.c2*(i**2)) % self.m
            if self.hashtable[hash_index] is None:
                self.hashtable[hash_index] = data
                return
            
    def display_hashtable(self):
        return self.hashtable
    
def DishPrepareOrder(order_list : list[int]) -> list[int]:
    orders = dict()
    for order in order_list:
        orders[order] = orders.get(order, 0) + 1
        
    dish_prepare_order = []
    for order in sorted(orders, key = lambda x: (-orders[x], x)):
        dish_prepare_order.append(order)
        
    return dish_prepare_order 

def EvaluatePostfixExpression(exp : str) -> float:
    '''
    infix exp = 2 + (3 * 1) - 9
    postfix exp = 2 3 1 * + 9 -
    result = -4.0
    '''
    stack = Stack()
    operators = {'+', '-', '/', '*', '**'}
    tokens = exp.split(' ')
    for token in tokens:
    
        if token in operators:
            operand2 = stack.pop()
            operand1 = stack.pop()
            if token == '+':
                result = operand1 + operand2
            elif token == '-':
                result = operand1 - operand2
            elif token == '*':
                result = operand1 * operand2
            elif token == '/':
                result = operand1 / operand2
            elif token == '**':
                result = operand1 ** operand2
            
            stack.push(result)
        else:
            try:
                stack.push(float(token))
            except ValueError:
                raise ValueError(f'invalid character is detected i.e { token = }')
    
    if stack.is_empty():
        raise ValueError("Invalid expression")
        
    return stack.pop()

def reverse(sll):
    '''Reverses a singly linked list in-place.'''
    prev = None
    temp = sll.head
    while temp is not None:
        _next = temp.next
        temp.next = prev
        prev = temp
        temp = _next            
        
    sll.head = prev

if __name__ == "__main__":
    
    sll = SinglyLinkedList()
    sll.insert_at_end(10)
    sll.insert_at_end(20)
    sll.insert_at_beginning(5)
    sll.insert_after(10, 15)  # insert 15 after 10
    print("List:", sll)

    print("Search 15:", sll.search(15))
    print("Delete 20:", sll.delete(20))
    print("List after deletion:", sll)
    print("Original List:", sll)
    sll.reverse()
    print("Reversed List:", sll)
    reverse(sll)
    print('original sll :', sll)
    
    dll = DoublyLinkedList()
    dll.insert_at_end(10)
    dll.insert_at_end(20)
    dll.insert_at_beginning(5)
    dll.insert_after(10, 15)  # insert 15 after 10
    print("List (forward):", dll.traverse_forward())
    print("List (backward):", dll.traverse_backward())

    print("Search 15:", dll.search(15))
    print("Delete 20:", dll.delete(20))
    print("List after deletion:", dll.traverse_forward())
    
    
    stack = Stack()
    stack.push(10)
    stack.push(20)
    stack.push(30)
    print("Stack:", stack)

    print("Peek:", stack.peek())
    print("Pop:", stack.pop())
    print("Stack after pop:", stack)

    print("Is empty?", stack.is_empty())
    
    q = Queue()
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print("Queue:", q)

    print("Peek:", q.peek())
    print("Dequeue:", q.dequeue())
    print("Queue after dequeue:", q)

    print("Is empty?", q.is_empty())
    
    assert DishPrepareOrder(
        [1006, 1008, 1009, 1008, 1007, 1005, 1008, 1001, 1003, 1009, 1006, 1003, 1004, 1002, 1008, 1005, 1004, 1007, 1006, 1002, 1002, 1001, 1004, 1001, 1003, 1007, 1007, 1005, 1004, 1002]
        ) == [1002, 1004, 1007, 1008, 1001, 1003, 1005, 1006, 1009]
    
    assert DishPrepareOrder(
        [1002, 1004, 1005, 1004, 1003, 1009, 1001, 1006, 1002, 1007, 1004, 1002, 1001, 1009, 1006, 1001, 1003, 1009, 1003, 1005, 1006, 1005, 1003, 1008, 1005, 1004, 1003, 1009, 1002, 1008, 1001, 1008, 1003, 1001, 1001, 1007, 1002, 1005, 1009, 1007, 1004, 1005, 1009, 1008, 1009, 1009, 1002, 1008, 1002, 1006, 1005, 1006, 1009, 1007, 1008, 1005, 1002, 1006, 1006, 1001, 1002, 1005, 1003, 1003, 1005, 1001, 1004, 1004, 1001, 1009, 1005, 1008, 1001, 1008, 1006, 1001, 1001, 1009, 1002, 1001, 1003, 1004, 1009, 1008, 1004, 1006, 1003, 1009, 1007, 1005, 1004, 1009, 1001, 1009, 1007, 1004, 1008, 1005, 1004, 1008]
        ) == [1009, 1001, 1005, 1004, 1008, 1002, 1003, 1006, 1007]
    
    assert DishPrepareOrder(
        [1009, 1001, 1005, 1004, 1008, 1002, 1003, 1006, 1007]
        ) == [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009]

    assert EvaluatePostfixExpression(
        '2 3 1 * + 9 -'
        ) == -4.0
    
    assert EvaluatePostfixExpression(
        '100 200 + 2 / 5 * 7 +'
        ) == 757.0
    
    assert EvaluatePostfixExpression(
        '3 7 + 12 2 - *'
        ) == 100.0
    
    


        
        
        
        
        