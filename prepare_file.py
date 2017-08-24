import os

goods = ['hat']

class analyze_color(object):
    def __init__(self, kind):
        self.kind = kind
        self.path = './'+self.kind+'/'

    def rename(self):
    	if self.kind not in goods:
    		print ('not found %s in goods'%self.kind)
    		return

    	if os.path.exists(self.path) == False:
    		print ('path %s not exist'%self.path)
    		return

    	for _,_,files in os.walk(self.path):
			i = 0
			for name in files:
				i += 1
				os.rename(self.path+name, self.path+'hat_'+str(i)+'.jpeg')

if __name__ == '__main__':
	op = analyze_color(str('hat'))
	op.rename()