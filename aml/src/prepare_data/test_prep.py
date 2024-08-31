import subprocess
import os
from pathlib import Path
import pandas as pd

data = {
    'age': {0: 63, 1: 67, 2: 67, 3: 37, 4: 41},
    'sex': {0: 1, 1: 1, 2: 1, 3: 1, 4: 0},
    'cp': {0: 1, 1: 4, 2: 4, 3: 3, 4: 2},
    'trestbps': {0: 145, 1: 160, 2: 120, 3: 130, 4: 130},
    'chol': {0: 233, 1: 286, 2: 229, 3: 250, 4: 204},
    'fbs': {0: 1, 1: 0, 2: 0, 3: 0, 4: 0},
    'restecg': {0: 2, 1: 2, 2: 2, 3: 0, 4: 2},
    'thalach': {0: 150, 1: 108, 2: 129, 3: 187, 4: 172},
    'exang': {0: 0, 1: 1, 2: 1, 3: 0, 4: 0},
    'oldpeak': {0: 2.3, 1: 1.5, 2: 2.6, 3: 3.5, 4: 1.4},
    'slope': {0: 3, 1: 2, 2: 2, 3: 3, 4: 1},
    'ca': {0: 0, 1: 3, 2: 2, 3: 0, 4: 0},
    'thal': {0: 'fixed', 1: 'normal', 2: 'reversible', 3: 'normal', 4: 'normal'},
    'target': {0: 0, 1: 1, 2: 1, 3: 0, 4: 0}
 }

def test_data_preparation():
    raw = pd.DataFrame(data)
    TMP_DIR = Path('./tmp/')
    TMP_DIR.mkdir(parents = True, exist_ok = True)
    CE = 'ordinal'
    RATIO = 0.3
    LOG = 0
    raw.to_csv(f'{TMP_DIR}/raw.csv', index = False)
    cmd = f"python aml/src/prepare_data/prep.py --raw_data={TMP_DIR}/'raw.csv' --categorical_encoding={CE} --test_size={RATIO} --prepared_data={TMP_DIR} --transformations_output={TMP_DIR}/feature-transformer --log={LOG}"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate() 
    result = str(out).split('\\n')
    for lin in result:
        if not lin.startswith('#'):
            print(lin)

    assert os.path.exists(f'{TMP_DIR}/raw.csv')
    assert os.path.exists(f'{TMP_DIR}/train.csv')
    assert os.path.exists(f'{TMP_DIR}/test.csv')
    assert os.path.exists(f'{TMP_DIR}/feature-transformer')

    print("¨Prep Data Unit Test Completed")