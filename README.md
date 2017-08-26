# Square Brawl Bot Overview:
This project was an attempt at building an agent that learns how to play the game called [Square Brawl](http://store.steampowered.com/app/394850/Square_Brawl/). The features are pulled straight from the game memory.

## Details
- Features are read from game memory.
- Agent sends actions through emulated controller.
- Agent can receive three feature states a second i.e. we can pull 3 rows of data from the game per second.
- To generate training data, a random number generator selected moves on behalf of the agent.
- 3.5M rows of data was generated (324 hours of gameplay).
- Models were trained offline on generated training data to allow for feature and model tweaking.
- Agent was given the shotgun and sniper.
- My benchmark was the random agent.
- The random agent managed to get 3 enemy kills for every 10 deaths.

[Presentation from my June 2017 Data Science meetup in Edmonton](https://docs.google.com/presentation/d/16ZBFpQT-BC_qZXr5dKvbdH96KqMWQ5ICcVfmvSZBXBs/edit?usp=sharing)

## Project Results
I was unable to get beat my benchmark.

1. Not enough information in features: four raw features, thirteen extrapolated
2. Poor quality data: features switching in memory, agent is blind for 3 seconds after deaths, agent can’t see bullets
3. I am not a reinforcement learning expert - not skilled enough to know understand the nuances of violating RL theory.

## Why did you not use images for the features instead?
Try as I might, I could not get any deep learning libraries to play nicely with my AMD GPU. Processing a 32x32 greyscale image of the game took ~4 seconds on the CPU. I will revist this project if I ever can somehow justify the cost of a new GPU.
