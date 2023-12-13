# ClusterFinder
Project aiming to find clusters in data streaming from CMS experiment CERN

To produced data for 1000 events, use the command:

```
python3 data_generator.py 1000
```

### Starting the Setup:

Currently, we are using the existing setup at BASE_PATH mentioned below. We can run the notebooks and models present here using the information below.

#### Using server@hep.wisc.edu

```
conda activate ml-env
jupyter notebook list
export BASE_PATH=/nfs_scratch/hsharma/MachineLearning/ClusterFinder
```

if no notebook is already running, then start the jupyter notebook server using the command below:

```
cd $BASE_PATH
nohup jupyter notebook --no-browser --port 3000
jupyter notebook list
```

Use the command below to connect to the jupyter notebook locally in your machine. If the ports are busy, then try using a different set of port values."

```
ssh -L 1234:localhost:9999 hsharma@login.hep.wisc.edu ssh -L 9999:localhost:3000 -N cmsgpu01
```

#### Using Docker:
Coming Soon


### HLS4ML Conversion

For performing your experiment with different settings of HLS4ML, duplicate the HLS4ML_Interface_Template and run the notebook accordingly. The project output folder can be set by setting the desired folder name in `cfg['OutputDir']` in hls4ml config part.

The list of models trained, along with their specifications can be found in models.json. The JSON is also loaded in the Template for anyone to look at.

Once the Vivado project folder is produced using the interface notebook, it can be synthesized using the command below:

```
nohup vivado_hls -f build_prj.tcl "reset=1 synth=1 csim=0 cosim=0 validation=0 export=0 vsynth=0" > vhls_synth.out &
```

Note:
- The current template uses io_stream method for passing data between layers. We must switch to io_parallel.


For more information on the the documentation and development of HLS4ML visit:
https://fastmachinelearning.org/hls4ml

### Future works:

- Build a rectangular I/P network for the working problem statement
- From Classification to Regression Task
- Regenerate i/p - o/p pairs for new task problem
