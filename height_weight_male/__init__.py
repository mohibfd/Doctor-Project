import matplotlib.pyplot as plt
import PIL
import os


def male_height_weight_calc(user_age, user_height=0, user_weight=0):

    im = PIL.Image.open(os.path.dirname(__file__) +
                        '/courbe-taille-poids-garcons.jpeg')

    _, img_max_height = im.size

    x_offput = 42
    y_offput = 43
    x_augmentation = 30.7
    y_augmentation = 6.02
    normalised_age = x_offput + user_age * x_augmentation

    normalised_height = img_max_height - \
        (y_offput + (user_height - 30) * y_augmentation)

    normalised_weight = img_max_height - \
        (y_offput + (user_weight) * y_augmentation)

    plt.imshow(im)

    if user_height:
        plt.scatter([normalised_age], [normalised_height],
                    c=[[0, 0, 0]], label='Height')
    if user_weight:
        plt.scatter([normalised_age], [normalised_weight],
                    c=[[0.4, 0.4, 0.4]], label='Weight')
    plt.axis('off')

    plt.legend()

    plt.show()
