# Python3 program to merge sort of linked list

# create Node using class Node.
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f'{self.data}'


class LinkedList:
    def __init__(self):
        self.head = None

    # push new value to linked list
    # using append method
    def append(self, new_value):

        # Allocate new node
        new_node = Node(new_value)

        # if head is None, initialize it to new node
        if self.head is None:
            self.head = new_node
            return
        curr_node = self.head
        while curr_node.next is not None:
            curr_node = curr_node.next

        # Append the new node at the end
        # of the linked list
        curr_node.next = new_node

    def sorted_merge(self, node_a, node_b):

        # Base cases
        if node_a is None:
            return node_b
        if node_b is None:
            return node_a

        # pick either a or b and recur..
        if node_a.data <= node_b.data:
            result = node_a
            result.next = self.sorted_merge(node_a.next, node_b)
        else:
            result = node_b
            result.next = self.sorted_merge(node_a, node_b.next)
        return result

    def merge_sort(self, head):

        # Base case if head is None
        if head is None or head.next is None:
            return head

        # get the middle of the list 
        middle = self.get_middle(head)
        next_to_middle = middle.next

        # set the next of middle node to None
        middle.next = None

        # Apply mergeSort on left list 
        left = self.merge_sort(head)

        # Apply mergeSort on right list
        right = self.merge_sort(next_to_middle)

        # Merge the left and right lists 
        sorted_list = self.sorted_merge(left, right)
        return sorted_list

    # Utility function to get the middle 
    # of the linked list
    @staticmethod
    def get_middle(head):
        if head is None:
            return head

        slow = head
        fast = head

        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        return slow

    def __repr__(self):
        # Utility function to print the linked list
        represent = ''
        if self.head is None:
            print(' ')
            return
        curr_node = self.head
        while curr_node:
            represent += f'{curr_node.data} -> '
            curr_node = curr_node.next
        return represent[:-4]


# Driver Code
if __name__ == '__main__':
    li = LinkedList()

    li.append(15)
    li.append(10)
    li.append(5)
    li.append(20)
    li.append(3)
    li.append(2)

    print(li)

    # Apply merge Sort 
    li.head = li.merge_sort(li.head)
    print("Sorted Linked List is:")
    print(li)


