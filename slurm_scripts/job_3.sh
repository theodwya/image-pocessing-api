#!/bin/bash
#SBATCH --gres=gpu:3
#SBATCH --job-name=image_processing
#SBATCH --output=slurm-%j.out

module load cuda/10.1
source activate myenv

python -c "
from app.tasks import decode_image;
decode_image('test_images/sample1.jp2', 'output/sample1_output.jp2', 3);
"
