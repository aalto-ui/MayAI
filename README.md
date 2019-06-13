## May AI? Design Ideation with Cooperative Contextual Bandits
In the [May AI-Project](https://dl.acm.org/citation.cfm?id=3290605.3300863) we developed a Cooperative Contextual Bandits (CCB) for an
interactive design ideation tool that 1) suggests inspirational
and situationally relevant materials (“may AI?”); 2) explores
and exploits inspirational materials with the designer.

In order to do so, we adapted an online learning cooperative contextual bandit
algorithm presented by [Tekin et al.](https://ieeexplore.ieee.org/document/7103356) to address our objectives to 1) identify and propose material that is novel
and relevant for a designer yet also 2) adapt to the designer’s
changing strategy of diversification and intensification.

## Overview of the Algorithm:

<img src="https://github.com/aalto-ui/MayAI/blob/master/images/Figure1.png"/>
We first slice the potential mood board space defined as: color value (C), saturation
(S), color lightness (L), image orientation (O), and color
distance (D) into partitions (see bandit.py).
These are then handled by strategy agents (A), where each is responsible for recommendations by its suggestion agents (a).

In every discrete trial:
<ol>
  <li>a mood board is transformed into a five-dimensional
vector in the context space and is assigned to the strategy
agent of the corresponding partition;</li>
  <li>the agent queries its own suggestion agents for similar
suggestions (exploitation) and nearby strategy agents
for alternative moods (exploration);</li>
  <li>
each suggestion agent within the current strategy, and
each nearby strategy agent, provides probabilities for
making a good suggestion (Fig. 1: b);</li>
   <li>
the agent with the highest probability is selected with
respect to an exploration/exploitation criterion, c;</li>
  <li>
if a suggestion agent is selected (Fig. 1: c), it describes
the next image suggestion feature vector; otherwise
(Fig. 1: d), the corresponding strategy agent queries its
own suggestion agents to identify this vector;</li>
  <li>this vector, in combination with the association list,
is used to query a suitable image in the local database;
if not successful, it will be translated into humanreadable
features to query images online in real time;</li>
  <li>the user accepts or rejects the suggested image; and</li>
  <li>that feedback is used to update the probability distributions
of the corresponding suggestion agents and,
in case of referral, of the neighboring strategy agent.
</li>
</ol>




The code for step 1 - 5 will be provided in the following.

## Getting started:
### Dependencies
```bash
pip install functools
pip install scipy
pip install random2
pip install numpy
```
### Python version
2.7


## Usage:
Navigate to the folder.
Run:
```bash
# Install required packages
python main.py
```
It will ask for an initial image in the form of a vector: (Hue:0-360, Saturation:0-1, Lightness:0-1, Orientation:0,1, Color Distance between the most dominant colors: 0-180)
An example vector would be: (123,0.6,0.3,0,178)

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT), see the [LICENSE.txt](./LICENSE.txt) file for details.

Copyright © 2019 [User Interfaces group](https://userinterfaces.aalto.fi/), [Aalto University](https://www.aalto.fi/), Finland
