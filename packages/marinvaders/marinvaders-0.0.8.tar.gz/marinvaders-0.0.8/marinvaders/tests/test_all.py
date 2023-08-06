import sys
import os
import pandas as pd


sys.path.append('..')

import marinvaders.marinelife as ml  # noqa: E402
import marinvaders.readers as readers  # noqa: E402


def test_ecoregions():
    marine_ecoregions = ml.marine_ecoregions()
    assert len(marine_ecoregions) > 0
    assert ['ECO_CODE', 'ECO_CODE_X', 'ECOREGION',
            'PROVINCE', 'REALM',
            'geometry'] == list(marine_ecoregions.columns)


def test_species_class():
    ds = ml.Species(145634)
    assert ds.aphia_id == 145634
    assert len(ds.obis) > 0
    assert isinstance(ds.obis, pd.DataFrame)


def test_marine_life_class():
    marinelife = ml.MarineLife(20194)
    assert marinelife.eco_code == 20194


def test_readers():
    ecomrgidlink = readers.eco_mrgid_link()
    assert isinstance(ecomrgidlink, pd.DataFrame)
    assert len(ecomrgidlink) > 0

    taxonomy = readers.read_taxonomy()
    assert isinstance(taxonomy, pd.DataFrame)
    assert len(taxonomy) > 0

    gisd = readers.read_gisd()
    assert isinstance(gisd, pd.DataFrame)
    assert len(gisd) > 0

    molnar = readers.read_molnar()
    assert isinstance(molnar, pd.DataFrame)
    assert len(molnar) > 0

    gisd_worms_link = readers.read_gisd_worms_link()
    assert isinstance(gisd_worms_link, pd.DataFrame)
    assert len(gisd_worms_link) > 0
