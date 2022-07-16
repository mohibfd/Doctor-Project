import matplotlib.pyplot as plt
import PIL
import os


def under3_weight_calc(user_age, user_weight):

    im = PIL.Image.open(os.path.dirname(__file__) +
                        '/courbe-poids-0a3ans-1.jpeg')

    max_age, max_weight = 36, 22
    img_max_age, img_max_weight = im.size

    # using 16 and 29 to get the point to the correct position
    x_offput = 16
    y_offput = 29
    # dk why but 47 fixes the offput issue with the y-axis
    normalised_age = x_offput + \
        ((img_max_age-max_age)/max_age) * user_age
    normalised_weight = - y_offput + img_max_weight - \
        ((img_max_weight-47)/max_weight) * user_weight

    plt.imshow(im)

    plt.scatter([normalised_age], [normalised_weight], c=[[0, 0, 0]])

    plt.axis('off')

    plt.show()
