#! /usr/bin/env python3

import pandas as pd
import pkg_resources


def load(file):
    # Ensure file has .zip extension
    file += '.zip' * (not file.endswith('.zip'))

    # Path to desired file
    resource_path = f'data/{file}'

    return pd.read_csv(pkg_resources.resource_filename(__name__, resource_path))
