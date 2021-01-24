from typing import List

import pandas as pd
import subsurface as ss
from striplog import Component

formations = ["topo",
              "etchegoin",
              "macoma",
              "chanac",
              "mclure",
              "santa_margarita",
              "fruitvale",
              "round_mountain",
              "olcese",
              "freeman_jewett",
              "vedder",
              "eocene",
              "cretaceous",
              "basement",
              "null"]

colors = dict([
    ("topo", "#cecece"),
    ("etchegoin", "#00c9d1"),
    ("macoma", "#007c79"),
    ("chanac", "#78007a"),
    ("mclure", "#5263c4"),
    ("santa_margarita", "#005c2a"),
    ("fruitvale", "#da4f1f"),
    ("round_mountain", "#3d270e"),
    ("olcese", "#cc212d"),
    ("freeman_jewett", "#ff74a8"),
    ("vedder", "#ffff00"),
    ("eocene", "#dc7c62"),
    ("cretaceous", "#736d1c"),
    ("basement", "#00b930")
])

#components = [Component({'lith': l, 'colour': c}) for l, c in zip(formations,
# list(colors.values()))]
components = [Component({'lith': l}) for l in formations]


def read_borehole_file(path, fix_df=True):
    """Returns the df with the depths for each borehole in one single row instead
     instead being each chunck a new row"""
    df = pd.read_table(path,
                       skiprows=41,
                       header=None,
                       sep='\t',
                       )

    df.rename(columns={1: 'x', 2: 'y', 3: 'name',
                       4: 'num', 5: 'z', 6: 'year', 10: 'altitude'},
              inplace=True)

    if fix_df:
        df['name'] = df['name'] + df['num']



        n_fixed_columns = 11
        n_segments_per_well = 15

        n_wells = df.shape[0]


        # Repeat fixed rows (collar name and so)
        df_fixed = df.iloc[:, :n_fixed_columns]
        df_fixed = df_fixed.loc[df_fixed.index.repeat(
            n_segments_per_well)]

        # Add a formation to each segment
        tiled_formations = pd.np.tile(formations, (n_wells))
        df_fixed['formation'] = tiled_formations

        # Add the segments base to the df
        df_bottoms = df.iloc[:,
                     n_fixed_columns:n_fixed_columns + n_segments_per_well]

        df_fixed['base'] = df_bottoms.values.reshape(-1, 1, order='C')

        # Adding tops column from collar and base
        df_fixed = ss.io.wells.add_tops_from_base_and_altitude_in_place(
            df_fixed,
            'name',
            'base',
            'altitude'
        )

        # Fixing boreholes that have the base higher than the top
        top_base_error = df_fixed["top"] > df_fixed["base"]
        df_fixed["base"][top_base_error] = df_fixed["top"] + 0.01

        # Add real coord
        df_fixed['z'] = df_fixed['altitude'] - df_fixed['md']

        df = df_fixed
    return df


def pandas_to_subsurface(df: pd.DataFrame, table: List = None):
    """

    :param df:
    :param table List[Striplog.Components]:
    :return:
    """
    from io import StringIO
    df_buffer = df.to_csv()

    unstruc = ss.io.read_wells_to_unstruct(
        collar_file=StringIO(df_buffer),
        read_collar_kwargs={
            'usecols': ['name', 'x', 'y', 'altitude'],
            'index_col': 'name',
            'header': 0,
            'is_json': False
        },
        survey_file=StringIO(df_buffer),
        read_survey_kwargs={
            'index_col': 'name',
            'usecols': ['name', 'md'],  # if incl and azi not given -> well vertical
            'is_json': False
        },
        lith_file=StringIO(df_buffer),
        read_lith_kwargs={
            'index_col': 'name',
            'usecols': ['name', 'top', 'base', 'formation'],
            'columns_map': {'top': 'top',
                            'base': 'base',
                            'formation': 'component lith',
                            }
        }
        , n_points=40, return_welly=False, table=components)

    return unstruc


def pandas_to_collars(df: pd.DataFrame):
    from io import StringIO
    df_buffer = df.to_csv()
    unstruct = ss.io.borehole_location_to_unstruct(
        collar_file=StringIO(df_buffer),
        read_collar_kwargs={
            'usecols': ['name', 'x', 'y', 'altitude'],
            'header': 0,
            'index_col': 'name'
        },
        add_number_segments=True
    )
    return unstruct


