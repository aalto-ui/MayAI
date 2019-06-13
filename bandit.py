__author__ = 'Janin Koch'
import functools
import operator
from helper import *
from scipy import stats
import math
import colorsys
import numpy as np


class ContextBandit():
    def __init__(self, arms):
        # Initiate arms with equal distribution
        self.size = arms
        self.bandits = np.random.random_sample(arms)

        # Store the maximum probability, used for regret calculation
        self.max_prob = np.amax(self.bandits)


    def __repr__(self):
        return 'Bandits: ' + self.bandits.__str__()


    def __str__(self):
        return self.__repr__()


def regret(bandit_obj, expected_reward):
    #Cost of the expected and max probability
    return bandit_obj.bandits.max_prob - expected_reward


def draw_bandit_distribution(stats):
    #Draws a random beta distribution depending on wins or loses
    a = stats[0]
    b = stats[1]

    if b < 0:
        b = 0

    return np.random.beta(a + 1, b + 1)


class ContextualBandit:
    def __init__(self, arm_dimensions, decision_dimension, context_dimension, task_data, prior_data):
        self.exploration_parameter = 0
        contexts = functools.reduce(operator.mul, context_dimension)
        decision = functools.reduce(operator.mul, decision_dimension)
        arms = functools.reduce(operator.mul, arm_dimensions)
        self.bandits = ContextBandit(contexts * decision * arms)

        self.key_selected = []
        self.last_selected = []
        self.already_seen = []
        self.mb_list = []

        # define context space
        color_space = 360
        saturation_space = 1.0
        light_space = 1.0

        # color devision
        colors = range(0, color_space, 5)
        color_slicing_A = (color_space / 6)
        color_slicing_a = color_slicing_A / 5
        sliced_colors = [colors[i:i + color_slicing_a] for i in range(0, len(colors), color_slicing_a)]
        decision_colors_sliced = []
        for el in sliced_colors:
            decision_colors_sliced.append([el[i:i + 4] for i in range(0, len(el), 4)])

        # light devision
        lights = np.arange(0, light_space + 0.2, 0.2)  ## 0.2 is the smallest instance
        light_slicing_parameter = 3
        sliced_lights = [lights[i:i + light_slicing_parameter] for i in range(0, len(lights), light_slicing_parameter)]
        decision_light_sliced = []
        for el in sliced_lights:
            decision_light_sliced.append([[round(i, 1)] for i in np.arange(el[0], el[2], 0.25)])


        # saturations devision
        saturations = np.arange(0, saturation_space + 0.2, 0.2)  ## 0.2 is the smallest instance
        saturation_slicing_parameter = 3
        sliced_saturation = [saturations[i:i + saturation_slicing_parameter] for i in
                             range(0, len(saturations), saturation_slicing_parameter)]
        decision_saturation_sliced = []
        for el in sliced_saturation:
            decision_saturation_sliced.append([[round(i, 1)] for i in np.arange(el[0], el[2], 0.25)])

        # orientation
        orientation = [[[0]], [[1]]]

        # color contrast
        distance = [[[0]], [[60]], [[120]]]

        color_A_list = []
        for color in decision_colors_sliced:
            color_A_list.append(color[0][0])

        sat_A_list = []
        for el in decision_saturation_sliced:
            sat_A_list.append(el[0][0])

        light_A_list = []
        for el in decision_light_sliced:
            light_A_list.append(el[0][0])

        orientation_A_list = []
        for el in orientation:
            orientation_A_list.append(el[0][0])

        distance_A_list = []
        for el in distance:
            distance_A_list.append(el[0][0])

        self.contextSpace = {}
        for color_A in decision_colors_sliced:
            for sat_A in decision_saturation_sliced:
                for light_A in decision_light_sliced:
                    for orientation_A in orientation:
                        for distance_A in distance:
                            """
                            Initializing the Context Space and the context 
                            or mood board is lies in 1 of these Context spaces
                            and is assigned 1 agent to it.
                            """
                            self.contextSpace[
                                (color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0], distance_A[0][0])] = {
                                'best_y': (0, 0, 0, 0, 0), 'y_val': 0.0,
                                'as': {}, 'neighbours': {}}
                            """
                            Initializing the Neighbors of vector space with probabilities (0,0) Win/Lose

                            """
                            for c in color_A_list:
                                if c != color_A[0][0]:
                                    self.contextSpace[(
                                        color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0],
                                        distance_A[0][0])][
                                        'neighbours'][
                                        (c, sat_A[0][0], light_A[0][0], orientation_A[0][0], distance_A[0][0])] = (0, 0)

                            for s in sat_A_list:
                                if s != sat_A[0][0]:
                                    self.contextSpace[(
                                        color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0],
                                        distance_A[0][0])][
                                        'neighbours'][
                                        (color_A[0][0], s, light_A[0][0], orientation_A[0][0], distance_A[0][0])] = (
                                        0, 0)

                            for l in light_A_list:
                                if l != light_A[0][0]:
                                    self.contextSpace[(
                                        color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0],
                                        distance_A[0][0])][
                                        'neighbours'][
                                        (color_A[0][0], sat_A[0][0], l, orientation_A[0][0], distance_A[0][0])] = (0, 0)

                            for o in orientation_A_list:
                                if o != orientation_A[0][0]:
                                    self.contextSpace[(
                                        color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0],
                                        distance_A[0][0])][
                                        'neighbours'][
                                        (color_A[0][0], sat_A[0][0], light_A[0][0], o, distance_A[0][0])] = (0, 0)

                            for d in distance_A_list:
                                if d != distance_A[0][0]:
                                    self.contextSpace[(
                                        color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0],
                                        distance_A[0][0])][
                                        'neighbours'][
                                        (color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0], d)] = (0, 0)
                            """
                            Defining the elements within the 
                            context space suggestion agents.
                            """
                            for color_a in color_A:
                                for sat_a in sat_A:
                                    for light_a in light_A:
                                        for orientation_a in orientation_A:
                                            for distance_a in distance_A:
                                                self.contextSpace[(
                                                    color_A[0][0], sat_A[0][0], light_A[0][0], orientation_A[0][0],
                                                    distance_A[0][0])]['as'][
                                                    (color_a[0], sat_a[0], light_a[0], orientation_a[0],
                                                     distance_a[0])] = {'best_y': (0, 0, 0, 0, 0), 'y_val': 0.0,
                                                                        'ys': {}}
        
                                                for color_y in color_a:
                                                    for sat_y in sat_a:
                                                        for light_y in light_a:
                                                            for orientation_y in orientation_a:
                                                                for distance_y in distance_a:
                                                                    self.contextSpace[(
                                                                        color_A[0][0], sat_A[0][0], light_A[0][0],
                                                                        orientation_A[0][0], distance_A[0][0])]['as'][
                                                                        (color_a[0], sat_a[0], light_a[0],
                                                                         orientation_a[0], distance_a[0])]['ys'][(
                                                                        color_y, sat_y, light_y, orientation_y,
                                                                        distance_y)] = (
                                                                        0, 0)


        #self.fill_dict(prior_data)
        #self.fill_dict(task_data)



    #def fill_dict(self, task_data):
        #Filling the user data / task data with the given data from main function i.e. 
        #User History

        #for row in task_data:
            #bandit = (h,s,l,o,dis)
            #context = (h,s,l,o,dis)
            #set_success(self, bandit, win, loss)

            #vc, current_context = get_A(self, context)
            #vb, current_bandit = get_A(self, bandit)
            #if current_context != current_bandit:
            #    set_A(self, current_context, current_bandit, win, loss)


    def select_bandit(self, bandit_obj, next_selected_context):
        #Returns the A, Best Bandits and the Best Values
        best_bandits = []
        best_values = []

        A, kA = get_A(bandit_obj, next_selected_context)
        for ka, va in A['as'].iteritems():
            arms = []
            draws = []
            for ky, vy in va['ys'].iteritems():
                arms.append(ky)
                draws.append(draw_bandit_distribution(vy))

            selected_bandit_id = np.argmax(draws)
            va['best_y'] = arms[selected_bandit_id]
            va['y_val'] = draws[selected_bandit_id]

            best_bandits.append(va['best_y'])
            best_values.append(va['y_val'])

        return A, best_bandits, best_values


    def suggest_images(self):
        if self.key_selected:
            r = 0
            g = 0
            b = 0
            o = []
            dist = 0
            counter = 0

            for el in self.key_selected:
                color_rgb = colorsys.hls_to_rgb(int(el[0]) / 360.0, el[2], el[1])
                r += color_rgb[0] * color_rgb[0]
                g += color_rgb[1] * color_rgb[1]
                b += color_rgb[2] * color_rgb[2]
                o.append(el[3])
                dist += el[4]
                counter += 1

            color_hls = colorsys.rgb_to_hls(math.sqrt(r/ counter), math.sqrt(g / counter), math.sqrt(b / counter))
            next_selected_context = (int(color_hls[0]*360),color_hls[2],color_hls[1], stats.mode(o).mode[0], dist / counter)

            # Draw from the existing model distribution from each bandit.
            # get highest reward per decision bandit
            A, best_bandits, best_values = self.select_bandit(self, next_selected_context)

            neighbours = []
            for kA, vA in A['neighbours'].iteritems():
                neighbours.append(kA)
                best_bandits.append(kA)
                best_values.append(draw_bandit_distribution(vA) + self.exploration_parameter)

            # Find the one with the highest value and select it
            selected_best_bandit_id = np.argmax(best_values)
            A['best_y'] = best_bandits[selected_best_bandit_id]
            A['y_val'] = best_values[selected_best_bandit_id]
            best_y = A['best_y']
            y_val = A['y_val']

            if A['best_y'] in neighbours:
                print 'a neighbour: exploration'
                A, best_bandits, best_values = self.select_bandit(self, A['best_y'])
                selected_best_bandit_id2 = np.argmax(best_values)
                best_y = best_bandits[selected_best_bandit_id2]
                y_val = best_values[selected_best_bandit_id2]
            else:
                print "exploitation"

            next_selected_bandit_clear = stragtegy_to_rawContext(best_y)
            return self, next_selected_context, next_selected_bandit_clear, y_val

        else:
            print "Missing context"


def update_bandit(bandit_obj, designer_decision, current_context):
    #Updates
    if current_context:
        #Get the last image and map into an agent.
        vc, context = get_A(bandit_obj, current_context[-1])

    if designer_decision == 0:
        # Failed!
        image_data = current_context[-1]
        if image_data:
            vb, bandit = get_A(bandit_obj, image_data)

        set_success(bandit_obj, image_data, win=0, loss=1)

        if context != bandit:
            set_A(bandit_obj, context, bandit, win=0, loss=1)
        current_context.pop(-1)



    elif designer_decision == 1:
        # Reward!
        image_data = current_context[-1]
        if image_data:
            vb, bandit = get_A(bandit_obj, image_data)

        set_success(bandit_obj, image_data, win=1, loss=0)  # selected_bandit replaced with image_data
        bandit_obj.key_selected.append(image_data)

        if context != bandit:
            set_A(bandit_obj, context, bandit, win=1, loss=0)

    return bandit_obj

