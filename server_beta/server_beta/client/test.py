import multiprocessing

def func1(mq):
	print("func1")
	print(mq)
	data = [11,22,33,44]
	for i in data:
		mq.put(i)

def func2(mq):
	print("func1")
	print(mq)
	lstResult = []
	while True:
		if mq.empty():
			break

		data = mq.get()
		lstResult.append(data)

	print(lstResult)

def main():
	q=multiprocessing.Queue()
	p1=multiprocessing.Process(target=func1, args=(q, ))
	p2=multiprocessing.Process(target=func2, args=(q, ))
	p1.start()
	p2.start()

if __name__ == '__main__':
	main()
	
	
	