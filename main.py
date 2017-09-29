import cv2
import color_analyzer
import matplotlib.pyplot as plt
import emd

import utils

colors = []
occupy = []

op = color_analyzer.analyzer('../image/test/', 100, 10)
op.run()

Sum = 0

for k,v in op.color.items():
    print ('%s = %d'%(k, float(v)/op.file_num))
    Sum = Sum + (v)/op.file_num
    c = utils.rgb2hex(k)
    colors.append(c)
    occupy.append(v)
print ('sum = %d'%Sum)
#cv2.waitKey()
#cv2.destroyAllWindows()

plt.bar(range(len(occupy)), occupy, color=list(colors))
plt.show()

emd.calc_emd(op)