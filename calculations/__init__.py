import matplotlib.pyplot as plt
import PIL
import os


def bmi_calc(user_height, user_weight):
    BMI = user_weight / (user_height/100)**2

    child_bmi = f"\nThe child's BMI is {round(BMI, 1)}."

    healthy = False

    bmis = {'underweight': 18.4, 'healthy': 24.9, 'overweight': 29.9,
            'severly overweight': 34.9, 'obese': 39.9}

    obese = True
    child_health = 'The child is '
    for k, v in bmis.items():
        if BMI <= v:
            child_health += k + '.'
            if k == 'healthy':
                healthy = True
            obese = False
            break

    if obese:
        child_health += 'obese.'

    def weight_calc(bmi, height):
        weight = bmi * (height/100)**2
        return weight

    healthy_range = ""
    if not healthy:
        low_recommended_weight = weight_calc(bmis['underweight'], user_height)
        high_recommended_weight = weight_calc(bmis['healthy'], user_height)

        healthy_range = f'The child should be between {round(low_recommended_weight,1)} and {round(high_recommended_weight,1)} kgs'

    def height_calc(bmi, weight):
        height = ((weight / bmi)**0.5) * 100
        return height

    max_weight = 130
    max_height = 200

    data_points = 50

    def axis_calc(bmi):
        x = []
        y = []
        for i in range(data_points+1):
            i /= data_points
            weight = weight_calc(bmi, max_height*i)
            height = height_calc(bmi, weight)
            x.append(height)
            y.append(weight)

        return x, y

    fig, ax = plt.subplots()
    prev_y = [0]*(data_points+1)
    for k, v in bmis.items():
        x, y = axis_calc(v)
        if k == 'obese':
            y = [max_weight + i for i in y]

        ax.fill_between(x, y, prev_y, label=k)
        prev_y = y

    ax.scatter(user_height, user_weight, c=[[0, 0, 0]], label='child')

    ax.set_title('BMI index')
    ax.set_xlabel('Height')
    ax.set_ylabel('Weight')
    ax.legend()

    ax.set(xlim=(20, max_height), ylim=(1, max_weight))

    fig.show()

    return child_bmi, child_health, healthy_range


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


def under3_weight_calc(user_age, user_weight):

    im = PIL.Image.open(os.path.dirname(__file__) +
                        '/courbe-poids-0a3ans.jpeg')

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


def female_height_weight_calc(user_age, user_height=0, user_weight=0):

    im = PIL.Image.open(os.path.dirname(__file__) +
                        '/courbe-taille-poids-filles.jpeg')

    _, img_max_height = im.size

    x_offput = 43
    y_offput = 44.5
    x_augmentation = 30.65
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
