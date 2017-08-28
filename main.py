from color_analyzer import analyzer

op = analyzer('./hat--old/')
op.run()

print ('there are %d images'%len(op.images))

for k,v in op.color.items():
    print ('%s = %d%%'%(k,v/len(op.images)))

cv2.destroyAllWindows()