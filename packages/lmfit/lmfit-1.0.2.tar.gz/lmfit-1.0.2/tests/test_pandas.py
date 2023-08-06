"""Tests for using data in pandas.[DataFrame|Series]."""
import os

import numpy as np
import pytest

import lmfit

pandas = pytest.importorskip('pandas')


def test_pandas_guess_from_peak():
    """Regression test for failure in guess_from_peak with pandas (GH #629)."""
    data = pandas.read_csv(os.path.join(os.path.dirname(__file__), '..',
                                        'examples', 'peak.csv'))
    xdat, ydat = np.loadtxt(os.path.join(os.path.dirname(__file__), '..',
                                         'examples', 'peak.csv'),
                            unpack=True, skiprows=1, delimiter=',')

    model = lmfit.models.LorentzianModel()
    guess_pd = model.guess(data['y'], x=data['x'])
    guess = model.guess(ydat, x=xdat)

    assert guess_pd == guess
