from PIL import Image

im = Image.open('q5.png') # Can be many different formats.
pix = im.load()

color_base = pix[0,0]
print(im.size)
for i in range(im.size[0]):
    for j in range(im.size[1]):
        if color_base != pix[i,j]:
            print('different color at', i, j, 'color is', pix[i,j])