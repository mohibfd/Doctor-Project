import matplotlib.pyplot as plt


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
