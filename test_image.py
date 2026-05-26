from PIL import Image

image = Image.open("dataset/images/15970.jpg")
print(image.size)
image.show()