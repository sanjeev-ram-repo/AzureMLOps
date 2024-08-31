import subprocess
import os
from pathlib import Path
import pandas as pd

data = {
    'age': {0: -1.3630106988346111, 1: 0.6057825328153826, 2: 0.908673799223074},
    'chol': {0: 0.3538030141995359,
    1: -0.2727231567788093,
    2: -0.4201410793619493},
    'oldpeak': {0: 1.6083563749375174,
    1: 0.0518824637076613,
    2: 0.4410009415151256},
    'thalach': {0: 1.3273702604124016,
    1: 0.0280924922838607,
    2: -0.7093354301674732},
    'trestbps': {0: -0.5, 1: 0.5714285714285714, 2: -1.2142857142857142},
    'ca': {0: 0.0, 1: 0.0, 2: 1.0},
    'cp': {0: 2.0, 1: 0.0, 2: 3.0},
    'exang': {0: 0.0, 1: 0.0, 2: 1.0},
    'fbs': {0: 0.0, 1: 1.0, 2: 0.0},
    'restecg': {0: 0.0, 1: 1.0, 2: 1.0},
    'sex': {0: 1.0, 1: 1.0, 2: 1.0},
    'slope': {0: 2.0, 1: 2.0, 2: 1.0},
    'thal': {0: 1.0, 1: 0.0, 2: 2.0},
    'target': {0: 0.0, 1: 0.0, 2: 1.0}
}

def test_model_training():
    
    raw = pd.DataFrame(data)
    TMP_DIR = Path('./tmp/')
    TMP_DIR.mkdir(parents = True, exist_ok = True)
    raw.to_csv(f'{TMP_DIR}/train.csv', index = False)
    raw.to_csv(f'{TMP_DIR}/test.csv', index = False)
    cmd = f"python aml/src/train/train.py --data={TMP_DIR} --max_depth=3 --scale_pos_weight=99 --model_folder={TMP_DIR}/model --feat_transformer={TMP_DIR}/feature-transformer"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate() 
    result = str(out).split('\\n')
    for line in result:
        if not line.startswith('#'):
            print(line)
    print(err)

    assert os.path.exists(f'{TMP_DIR}/model')
    assert len(os.listdir(f'{TMP_DIR}/model')) == 5

    print("¨Prep Data Unit Test Completed")
