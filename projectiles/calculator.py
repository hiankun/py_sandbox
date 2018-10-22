import math
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import glob

if __name__ == '__main__':

    ax = plt.gca()

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', dest='dir', type=str, nargs='+', help='directory of csv files')
    parser.add_argument('-p', '--pos', dest='pos', action='store_true', help='show position')
    args = parser.parse_args()

    dir_list = args.dir
    for directory in dir_list:
        csv_files  = glob.glob(directory + '/*.csv')
        df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True, sort=False, axis=1)

        n_col = len(df.columns)
        even_col = [i for i in range(n_col) if i%2 == 0] # x-axis
        odd_col = [i for i in range(n_col) if i%2 != 0] # y-axis

        df['avg_x'] = df[even_col].mean(axis=1)
        df['avg_y'] = df[odd_col].mean(axis=1)
        df['dx'] = df['avg_x'] - df['avg_x'].shift(1)
        df['ddx'] = df['dx'] - df['dx'].shift(1)
        df['dy'] = df['avg_y'] - df['avg_y'].shift(1)
        df['ddy'] = df['dy'] - df['dy'].shift(1)
        df['dddy'] = df['ddy'] - df['ddy'].shift(1)

        if(args.pos):
            df['avg_y'] = -df[odd_col].mean(axis=1)
            df.plot(x='avg_x',y='avg_y',style='-o',ax=ax)
        else:
            #df.plot(y='dx',style='-o',ax=ax)
            #df.plot(y='ddx',style='x-',ax=ax)
            #df.plot(y='dy',style='-o',ax=ax)
            #df.plot(y='ddy',style='x-',ax=ax)
            df.plot(y='dddy',style='*-',ax=ax)
    ax.legend().set_visible(False)
    plt.show()
