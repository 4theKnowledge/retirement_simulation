"""
Basic model for Monte Carlo simulation.

"""

import pandas as pd
import numpy as np

from absl import flags
from absl import app

FLAGS = flags.FLAGS

flags.DEFINE_integer('sim_iters', 10, 'Number of Monte Carlo simulation iterations')


def basic_sim(argv):
    """
    pass in a set of timeseries data and retrieve the P25, P50, P75 information from it.
    """
    for i in range(1, FLAGS.sim_iters+1, 1):
        x = round(np.random.uniform(0,1,10).mean(), 2)
        
        yield {x}

def main(argv):
    df = pd.DataFrame(basic_sim(argv), columns=['mean'])
    print(df)
    
if __name__ == '__main__':
    print('Running in main')
    app.run(main)