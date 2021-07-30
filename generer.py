import random

def generer(n):
	p,w,d = [],[],[]
	for i in range(n):
		p.append(random.randint(1,100))
		w.append(random.randint(1,10))
	ep = sum(p)
	minW = int(0.2*ep)
	maxW = int(0.6*ep)

	for i in range(n):
		d.append(random.randint(minW, maxW))
	return p,w,d