### SETUP GRASPNET6DOF

**Prerequisite**: GRASPNET6DOF repo shall already exist under graspflow_models. If not pull it from

```
git clone https://github.com/tasbolat1/pytorch_6dof-graspnet
```

Install using instructions given in the page. I used conda environment for this and it worked as charm.

### SETUP GPD

**Prerequisite**: GPD repo shall already exist under graspflow_models. If not pull it from

```
git clone https://github.com/tasbolat1/gpd.git
```

Install using instructions given in the repo. No need additional packages.

### HOW TO SAMPLE USING GRASPNET6DOF FOR ISAAC POINTCLOUDS

*Note:* for ClearLab polaris server, activate conda:

```
conda activate new_pytorch_graspnet
```

1. **Sample:** Run sampler using

```
python generate_data_from_isaac_pcs.py --cat mug --idx 2 --n 20 --refinement_method gradient --refine_steps 50
```

replace mug and 2 with respecitive category and idxs. This code does following actions:

- samples 20 grasp candidates per unique pc from camera_view1 (index 1, not 0);
- refines these grasps using refine_steps size;
- stacks pcs from different camera_views and creates one pc in world frame;
- add ``--visualize`` to visualize the grasps;
- adds necessary transformations;
- saves results to the graspflow_models/experiments/generated_grasps/;
- solves ik: all grasps are reachable in terms of ik, but does not check self-collision or table collision.

Parameters to finetune:

- TOP_DOWN_PHI - angle between grasp vector and plane on xy.  in degrees
- TABLE_HEIGHT = 0.22 # table height to specify z threshold on grasps. in cm

Check data_structure.txt for full structure of saved data into npz file.

2. **Only visulize sampled grasps:** Run following command to visualize the grasps from npz files

```
python visualize_grasps.py --classifier Sminus --method graspnet --cat scissor --idx 7
```

Check data_struture.txt for definition of classifier and method.

3. **Run all**. Use bash code to run for all objects:

```
bash run_test.bash
```

This will take some time to run.

### HOW TO SAMPLE USING GPD FOR ISAAC POINTCLOUDS

There must be stacked pc ready to be uploaded in the form of npz. If not certain, please look at gpd_prepare.py

1. **Preprocess pointclouds:** basically converts stacked pcs in world frame and saves using pcd.
First, make sure that graspflow_env is activated:

``source grasfplow_venv/bin/activate``

Then, you can achive this using two methods:

I. Directly using python command:

``python gpd_preprocess.py --cat box --idx 14``

Make sure to replace cat and idx for respective category and idx of the object. This will save Pointclouds in pcd format under the specified directory (graspflow_models/experiments/pointclouds/pcd/).

II. Use bash command to run all together:

``bash gpd_preprocess.bash``

This bash command underline runs step I repeteadly to go through all categories and idxs

2. **Sample using gpd**

For this, there is no need to activate any python env, this runs fully on cpp.

Go to the gpd folder

```
cd graspflow_models/gpd/build
```

Run gpd sampler

```
./detect_grasps ../cfg/eigen_params.cfg ../../experiments/pointclouds/pcd box 14 0 ../../experiments/gpd_raw_grasps
```

here 14 is idx and 0 refers to isaac_env (a.k.a unique pc).

or use bash file to generate all. Do not forget to indicate total_num_env!

```
bash run_gpd.bash 
```

Note that running bash file is good, because it also saves log file and sampling time can be extracted from there

Parameters to finetune (indicated in cfg/eigen_params.cfg):
    - thresh_rad - top down angle, keep it same as graspnet
    - TODO

3. **Postprocess gpd grasps**

Concatenate grasps to fit into npz file use following command:

```
python gpd_postprocess.py --cat box --idx 14
```

or all together (do not forget total_num_env!)

```
bash gpd_postprocess.bash
```


### NEW DOCUMENTATION

We will follow these docs as this is more up to date.

### GRASPNET SAMPLER

1.  Run this in terminal to run graspnet sampler. If in Polaris, use conda environment *new_pytorch_graspnet*.

```
cd grapsflow_models/pytorch_6dof-graspnet

python generate_data_from_isaac_pcs.py --batch_size 5 --cat scissor --idx 7 --num_grasp_samples 30 --refinement_method gradient --refine_steps 10 --save_dir ../experiments/generated_grasps_experiment33 --experiment_type complex
```

use `-h` to find out how to use arguments.

### GPD SAMPLER

1. Pre-process pointclouds to create pcds. If in Polaris, use conda environment *new_pytorch_graspnet*.

```
cd grapsflow_models/pytorch_6dof-graspnet

python gpd_preprocess.py --cat box --idx 14
```

2. In new terminal without activating any python environment

```
cd graspflow_models/gpd/build

./detect_grasps ../cfg/eigen_params.cfg ../../experiments/pointclouds/pcd box 14 0 ../../experiments/gpd_raw_grasps
```

3. In new terminal run postprocess: (If in Polaris, use conda environment *new_pytorch_graspnet*.)

```
python gpd_postprocess.py --cat box --idx 14
```

### Visualizing grasps

To visualize any grasp (original, refined), please run:

```
cd grapsflow_models/pytorch_6dof-graspnet

python visualize_grasps.py --cat scissor --idx 7 --data_dir ../experiments/generated_grasps_experiment33 --experiment_type complex --method GraspOpt --classifier N --grasp_space SO3 
```

Note: in polaris you can use any environment conda *new_pytorch_graspnet* or pyvenv *graspflow_venv*.

### Debugging refinement methods

To debug refined methods, please run the following code:

```
cd grapsflow_models/graspflow

python debug_refined_grasps.py --cat scissor --idx 7 --sampler graspnet --classifier N --method GraspOpt --grasp_space SO3 --grasp_folder ../experiments/generated_grasps_experiment33
```

### Refinement using GraspFlow (legacy method)

To refine using GraspFlow go to:

```
cd grapsflow_models/graspflow
```
Here, there are two options to refine grasps using GraspFlow. All of the methods follow instructions from config file given in ``grapsflow_models/graspflow/configs/graspflow_isaac_params.yaml``:

1. If optimizer option is chosen to be ``MTAdam``, individual ``eta_t`` and ``eta_r`` for each classifier has no effect. Use ``eta_t`` and ``eta_r`` under optimizer option to finetune.

2. If optimizer option is chose to be ``Adam`` or ``SGD``,  only individual ``eta_t`` and ``eta_r`` for each classifier matter. Those are used to finetune the optimizer.

To run refinement using GraspFlow, run:

```
python refine_isaac_grasps5.py --cat scissor --idx 7 --grasp_folder ../experiments/generated_grasps_experiment33 --sampler graspnet --grasp_space SO3 --device 1 --max_iteration 30 --method GraspFlow --classifier SEC --experiment_type complex
```

### Refine using GraspOpt

```
cd grapsflow_models/graspflow
```
GraspOpt also follows instructions given in ``grapsflow_models/graspflow/configs/graspflow_isaac_params.yaml``, under ``GraspOpt`` section.

GraspOpt follows ranking system. If classifier is put into rank 1, it's expected that those classifiers have higher priorities to be satisfied.

The usage of GrapsOpt is also simple, just run:

```
python refine_isaac_grasps5.py --cat scissor --idx 7 --grasp_folder ../experiments/generated_grasps_experiment33 --sampler graspnet --grasp_space SO3 --device 0 --max_iterations 30 --method GraspOpt --classifier SEC --experiment_type complex
```

Note: make sure that all classifiers in argument is specified in config file. Otherwise the result is incorrect.

### Running a planner

All moveit related graspflow packages are located under ``/ws_moveit``

1. In new terminal start ros:

``roscore``

2. From now on every new terminal run rossy things. Do not activate any conda or pyenv. It's designed to work with Python2.7:

``source /opt/ros/noetic/setup.bash``

``source ~/ws_moveit/devel/setup.bash``

3. Run robot controller:

``roslaunch graspflow_plan robot_bringup.launch``


4. Run the following planner for **single items**:

``rosrun graspflow_plan test_robot.py cylinder 11 gpd metropolis S Euler /home/tasbolat/some_python_examples/graspflow_models/experiments/generated_grasps_experiment7 0``

5. Run the following planner for **complex scene**:

``rosrun graspflow_plan test_robot_complex_modified.py scissor 7 graspnet N N N  /home/tasbolat/some_python_examples/graspflow_models/experiments/generated_grasps_experiment32 1``


