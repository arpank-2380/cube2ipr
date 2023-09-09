#!/bin/bash
#SBATCH --job-name=ipr-s2-2hk
#SBATCH --time=2:00:00             # MAXIMUM WALLTIME
#SBATCH --partition=gagalli-brdwl     # GALLI GROUP PRIVATE PARTITION
#SBATCH --ntasks=25
##SBATCH --qos=gagalli-debug

############################## Load distribution ######################################################
export I_MPI_PMI_LIBRARY=/software/slurm-current-el7-x86_64/lib/libpmi.so
export I_MPI_FABRICS=shm:dapl
export OMP_NUM_THREADS=1

module load python

cube2ipr=/home/arpank/Scripts/cube2ipr/cube2ipr.py

cd $SLURM_SUBMIT_DIR/wf_cube_files

for i in `seq 420 444`; do
    srun -n 1 python ${cube2ipr} -prefix wf${i} &
done
wait

mv *ipr.dat $SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR  

