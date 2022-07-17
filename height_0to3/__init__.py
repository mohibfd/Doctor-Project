import matplotlib.pyplot as plt
import PIL
import os


def under3_height_calc(user_age, user_height):

    im = PIL.Image.open(os.path.dirname(__file__) +
                        '/courbe-taille-0a3ans.jpeg')

    max_age = 36
    img_max_age, img_max_height = im.size

    x_offput = 18
    y_offput = 32
    normalised_age = x_offput + \
        ((img_max_age-39)/max_age) * user_age

    normalised_height = img_max_height - (y_offput + (user_height-30)*4.75)

    plt.imshow(im)

    plt.scatter([normalised_age], [normalised_height], c=[[0, 0, 0]])

    plt.axis('off')

    plt.show()
