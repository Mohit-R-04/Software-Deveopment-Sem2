class _Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_end(self, data):
        if not self.head:
            self.head = _Node(data)
        else:
            current_node = self.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = _Node(data)

    def remove_at(self, index):
        if index == 0:
            self.head = self.head.next
            return
        current_node = self.head
        count = 0
        while current_node:
            if count == index - 1:
                current_node.next = current_node.next.next
                break
            current_node = current_node.next
            count += 1

    def clear(self):
        self.head = None

    def insert_at_beginning(self, data):
        node = _Node(data, self.head)
        self.head = node

    def insert_at(self, index, data):
        '''inserts data at specific index'''

        if index == 0:
            self.insert_at_beginning(data)
            return

        count = 0
        itr = self.head

        while itr:
            if count == index - 1:
                node = _Node(data, itr.next)
                itr.next = node
                break

            itr = itr.next
            count += 1

        print("Index out of range")
        return

    def get_length(self):
        count = 0
        itr = self.head

        while itr:
            count += 1
            itr = itr.next

        return count

    def __len__(self):
        current = self.head
        count = 0
        while current:
          count += 1
          current = current.next
        return count

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def __repr__(self):
        if self.head is None:
            return "Linked List is empty"

        itr = self.head
        llstr = ''

        while itr:
            llstr += str(itr.data) + ' --> ' if itr.next else str(itr.data)
            itr = itr.next

        return llstr

    def __iter__(self):
        self._current = self.head
        return self

    def __next__(self):
        if self._current:
            data = self._current.data
            self._current = self._current.next
            return data
        else:
            raise StopIteration

# [medicine code, medicine name, expiry date, quantity, location, actual price, selling price, GST]


ll=LinkedList()
import csv
f=open('medicine_data.csv', 'r', newline='')
csv_reader=csv.reader(f)
ll.insert_values(csv_reader)
meds_dict={}
for med in ll:
    if int(med[4]) not in meds_dict.keys():
        meds_dict[int(med[4])]=[med[1]]
    elif int(med[4]) in meds_dict.keys():
        meds_dict[int(med[4])].append(med[1])