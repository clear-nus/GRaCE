# Experimental Setup

## GraspFlow

GraspFlow mainly tackles single item in the environment.

 - E_TYPE: single
 - M_TYPE: GraspFlow, graspnet, metropolis
 - (cat, idx): 
    - (box,14)
    - (box,17)
    - (mug,2)
    - (mug,8)
    - (mug,14)
    - (bottle,3)
    - (bottle,12)
    - (bottle,19)
    - (bowl,1)
    - (bowl,16)
    - (cylinder,2)
    - (cylinder,11)
    - (fork, 1)
    - (fork, 11)
    - (hammer, 15)
    - (pan, 3)
    - (pan, 6)
    - (scissor, 4)
    - (scissor, 7)
    - (spatula, 1)
    - (spatula, 14)


## GoES 

GoES tackles objects in complex environments.

   - E_TYPE: shelf008
   - (cat, idx):
      - (bottle 14)
      - (bowl 8)
      - (bowl 10)
      - (pan 6)
      - (pan 12)
      - (fork 6)
      - (scissor 7)
   
   - E_TYPE: diner001
   - (cat, idx):
      - (pan, 12)
      - (spatula, 14)
      - (bottle, 0)
      - (bowl, 8)
      - (fork, 6)

For both environments, GoES can optimized using following parameters:
   - Classifiers:
      - S - Stability Classifier - assesses stability of the optimized grasps.
      - E - Executable Classifier - assesses wether grasp lies within robot's reachable map and avoids singularity.
      - C - Collision Classifier - assess collision between the grasp and environment.
      - N - Intent Classifier - assesses intent affordance for the query.
      *Note*: classifier parameter in GoES can be build using any combination of the classifiers above. E.g: SE, SC, SEC, ...
   
Use config file to indicate formula ranking and other parameters of the GoES.
   - optimizer - pytorch optimizer. Keep it as SGD.
      - eta_t - learning rate for translation.
      - eta_r - learning rate for orientation.
      - grad_normalize - boolean indicator responsible for normalization of gradients.
   - GoES
      - num_samples_per_grasp: number of additional samples per grasp
      - grad_iterations: number of lower bound local optimizations
      - t_std_dev: standard deviation for translations for ES part of GoES.
      - e_std_dev: standard deviation for orientations for ES part of GoES.
      - S_warmup_iterations: number of initial iterations for S classifier as a warmup.

