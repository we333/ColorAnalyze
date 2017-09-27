# -- coding: utf-8 --
import cv2

import color_analyzer
import emd
import utils

iroya = color_analyzer.analyzer('../global_images/test/', 50, 10)
iroya.run()
iroya_plot = utils.plot(iroya.color)
iroya_plot.show()


print ('***********************************************************')
a = color_analyzer.analyzer('./pantone/a/', 50, 10)
b = color_analyzer.analyzer('./pantone/b/', 50, 10)
a.run()
b.run()

distance = emd.calc_emd(a.color, b.color)
print (distance)