import os

goods = ['hat']

class prepare_file(object):
    def __init__(self, kind):
        self.kind = kind
        self.path = './'+self.kind+'/'
        if self.kind not in goods:
    		print ('not found %s in goods'%self.kind)
    	if os.path.exists(self.path) == False:
    		print ('path %s not exist'%self.path)
    		
    def rename(self):
    	for _,_,files in os.walk(self.path):
			i = 0
			for name in files:
				i += 1
				os.rename(self.path+name, self.path+'hat_'+str(i)+'.jpeg')

if __name__ == '__main__':
#	op = prepare_file('hat')
#	op.rename()