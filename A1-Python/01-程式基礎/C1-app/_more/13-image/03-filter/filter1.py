from PIL import Image
from PIL import ImageFilter

img = Image.open('../img/test.png')
imgf = img.filter(ImageFilter.FIND_EDGES)
imgf.save("testEdge.jpg")
imgf = img.filter(ImageFilter.BLUR)
imgf.save("testBlur.jpg")
imgf = img.filter(ImageFilter.CONTOUR)
imgf.save("testCoutour.jpg")
imgf = img.filter(ImageFilter.DETAIL)
imgf.save("testDetail.jpg")
imgf = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
imgf.save("testEdgeEnhanceMore.jpg")
imgf = img.filter(ImageFilter.EMBOSS)
imgf.save("testEmboss.jpg")
imgf = img.filter(ImageFilter.SHARPEN)
imgf.save("testSharpen.jpg")
imgf = img.filter(ImageFilter.SMOOTH_MORE)
imgf.save("testSmoothMore.jpg")