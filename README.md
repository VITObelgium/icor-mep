This sample shows how to use iCOR on the PROBA-V MEP (Mission Exploitation Platform, https://proba-v-mep.esa.int/) for Sentinel2 input data.
The sample can be executed 'locally' (i.e on a MEP user VM), or it can run parallellized on the MEP Hadoop processing cluster.

# Running the code
## Locally on the user VM
Run the `run-local-s2.sh` bash script on the command line for a local test run.
This method will use the local cpu's of your MEP user VM. The script accepts a number of input files.
If needed, iCOR properties can be changed in the shell scripts.

## On the Hadoop cluster
### Log into Hadoop
Run `kinit` and provide your MEP password. (Same as VM/portal.)

### Submit your job on Hadoop
Run the `run-cluster-s2.sh` script. It will package your project and submit it to the Hadoop cluster.

### View job logs Hadoop
As your job now runs on remote servers, the output generated there is not directly visible.
You can retrieve the full logs via the MEP JobControl dashboard (https://proba-v-mep.esa.int/applications/jobdashboard/).

### Results
The results will be made available in your private MEP folder (/data/users/<username>/Private), which is accessible from the PROBA-V MEP user VM.
