class Stack():
	def __init__(self):
		self.items = []

	def isEmpty(self):
		return self.items == []

	def push(self, item):
		self.item.append(item)

	def pop(self):
		return self.item.pop()

	def peek(self):
		return self.items[len(self.items)-1]
		
	def size(self):
		return len(self.items)