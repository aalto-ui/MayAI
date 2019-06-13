import random
import numpy as np


def stragtegy_to_rawContext(context_cube):
    # idea input (280, 0.9, 0.3, 0, 90)
    r = random.choice(range(5))
    l = np.arange(0.0, 0.3, 0.1)
    s = np.arange(0.0, 0.2, 0.1)
    d = random.choice(range(59))

    # get color
    color = context_cube[0] + r

    # get saturation
    if context_cube[1] in [0.0, 0.3, 0.6]:
        sat = context_cube[1] + random.choice(l)
    elif context_cube[1] == 0.9:
        sat = context_cube[1] + random.choice(s)

    # get light
    if context_cube[2] in [0.0, 0.3, 0.6]:
        t = context_cube[2] + random.choice(l)
    elif context_cube[2] == 0.9:
        t = context_cube[2] + random.choice(s)

    #get distance
    distance = min(context_cube[4] + d, 180)

    return (color, round(sat, 1), round(t, 1), context_cube[3], distance)


def get_index(bandit_obj, value):
   index = bandit_obj.decisionSpace[value]
   return index


def get_success(bandit_obj, bandit):
    #Get the value of bandit success
    if bandit[0] == 360:
        dA=360
    else:
        dA = bandit[0] % 60

    sA = bandit[1] % 0.6
    lA = bandit[2] % 0.6
    cA = get_contrast(bandit[4])

    da = bandit[0] % 20
    sa = bandit[1] % 0.3
    la = bandit[2] % 0.3
    ca = get_contrast(bandit[4])

    dy = bandit[0] % 5
    sy = bandit[1] % 0.3
    ly = bandit[2] % 0.3
    cy = get_contrast(bandit[4])

    value =  bandit_obj.contextSpace[(bandit[0] - dA, round(bandit[1] - sA, 1), round(bandit[2] - lA, 1), bandit[3], cA)]['as'][
        (bandit[0] - da, round(bandit[1] - sa, 1), round(bandit[2] - la, 1), bandit[3], ca)][
        'ys'][(bandit[0] - dy, round(bandit[1] - sy, 1), round(bandit[2] - ly, 1), bandit[3], cy)]

    return (bandit[0] - dA, round(bandit[1] - sA, 1), round(bandit[2] - lA, 1), bandit[3], cA), value


def set_success(bandit_obj, bandit_origin, win, loss):
    #Add win or loss for a bandit
    if bandit_origin[0] !=360:
        bandit = bandit_origin

    else:
        bandit = [0,bandit_origin[1],bandit_origin[2],bandit_origin[3],bandit_origin[4]]

    dA = bandit[0] % 60
    sA = bandit[1] % 0.6
    lA = bandit[2] % 0.6
    cA = get_contrast(bandit[4])

    da = bandit[0] % 20
    sa = bandit[1] % 0.3
    la = bandit[2] % 0.3
    ca = get_contrast(bandit[4])

    dy = bandit[0] % 5
    sy = bandit[1] % 0.3
    ly = bandit[2] % 0.3
    cy = get_contrast(bandit[4])

    to_add = (win, loss)

    old = bandit_obj.contextSpace[(bandit[0] - dA, round(bandit[1] - sA, 1), round(bandit[2] - lA, 1), bandit[3], cA)]['as'][
        (bandit[0] - da, round(bandit[1] - sa, 1), round(bandit[2] - la, 1), bandit[3], ca)][
        'ys'][(bandit[0] - dy, round(bandit[1] - sy, 1), round(bandit[2] - ly, 1), bandit[3], cy)]
    z = tuple(map(sum, zip(to_add, old)))

    bandit_obj.contextSpace[
        (bandit[0] - dA, round(bandit[1] - sA, 1), round(bandit[2] - lA, 1), bandit[3], cA)]['as'][
        (bandit[0] - da, round(bandit[1] - sa, 1), round(bandit[2] - la, 1), bandit[3], ca)][
        'ys'][(bandit[0] - dy, round(bandit[1] - sy, 1), round(bandit[2] - ly, 1), bandit[3], cy)] = z
    return True


def get_contrast(value):
    if 0 <= value < 60:
        cA = 0
    elif 60 <= value < 120:
        cA = 60
    elif 120<= value <=180:
        cA =120
    else:
        print "Contrast is wrong"
        print value

    return cA


def set_A(bandit_obj, context, bandit, win, loss):

    to_add = (win, loss)
    neighbour_list = bandit_obj.contextSpace[context]['neighbours']

    if bandit in neighbour_list:
        old = bandit_obj.contextSpace[context]['neighbours'][bandit]

        z = tuple(map(sum, zip(to_add, old)))
        bandit_obj.contextSpace[context]['neighbours'][bandit] = z
    else:
        pass

    return True


def get_a(bandit_obj, bandit):
    #Gets the Suggestion Agent small a
    if bandit[0] == 360:
        dA=360
    else:
        dA = bandit[0] % 60

    sA = bandit[1] % 0.6
    lA = bandit[2] % 0.6
    cA = get_contrast(bandit[4])

    da = bandit[0] % 20
    sa = bandit[1] % 0.3
    la = bandit[2] % 0.3
    ca = get_contrast(bandit[4])

    a = bandit_obj.contextSpace[(bandit[0] - dA, round(bandit[1] - sA, 1), round(bandit[2] - lA, 1), bandit[3], cA)]['as'][
        (bandit[0] - da, round(bandit[1] - sa, 1), round(bandit[2] - la, 1), bandit[3], ca)]['ys']
    return a


def get_A(bandit_obj, bandit_origin):
    #Gets the Strategy Agent big A
    if bandit_origin[0] != 360:
        bandit = bandit_origin

    else:
        bandit = [0, bandit_origin[1], bandit_origin[2], bandit_origin[3], bandit_origin[4]]

    dA = bandit[0] % 60
    sA = bandit[1] % 0.6
    lA = bandit[2] % 0.6
    cA = get_contrast(bandit[4])

    orientation = 0
    if bandit[3] >= 0.5:
        orientation = 1

    bandit = (bandit[0] - dA, round(bandit[1] - sA, 1), round(bandit[2] - lA, 1), orientation, cA)
    A = bandit_obj.contextSpace[bandit]

    return A, bandit


def get_all(bandit_obj):
    #Get the context space
    all_context = []

    for A, v in bandit_obj.contextSpace.iteritems():
        for a, va in v['as'].iteritems():
            for y in va['ys'].iteritems():
                all_context.append(y[0])
    return all_context


def data2feature_vector(hue1, hue2, width, height, sat1, bright1):
    #Return data to feature map of each data element
    # calculate color distance
    new_contrast = color_distance(hue1, hue2)

    # calculate orientation
    wh_relation = width / height
    orientation = 0
    if wh_relation >= 1:
        orientation = 1

    # actual feature vector of the selected image
    return (hue1, sat1, bright1, orientation, new_contrast)

#calculates a color distance between 0 and 180
def color_distance(hue1, hue2):
    return min(abs(hue1 - hue2), 360 - abs(hue1 - hue2))
