import cv2
import color_analyzer

op = color_analyzer.analyzer('./hat/', 50, 10)
op.run()

print ('there are %d images'%op.file_num)

for k,v in op.color.items():
    print ('%s = %.2f%%'%(k,float(v)/op.file_num))

cv2.waitKey()
cv2.destroyAllWindows()