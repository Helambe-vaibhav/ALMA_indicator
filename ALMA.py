import numpy as np
import pandas as pd
from math import exp
from ta.utils import IndicatorMixin

class ALMAIndicator(IndicatorMixin):
    def __init__(
            self,
            close: pd.Series,
            window,
            fillna: bool = False):
        self._close = close
        self._window = window
        self._offset = 0.85
        self._sigma = 6
        self._fillna = fillna
        self._run()

    def _run(self):
        self._alma_weights = self.alma_weights(self._window,self._offset,self._sigma)
        self._alma = self._close.rolling(self._window).apply(self.calculate_alma)

    def alma(self) -> pd.Series:
        alma = self._check_fillna(self._alma, value=0)
        return pd.Series(alma, name=f'alma')

    def calculate_alma(self, prices: np.ndarray) -> float:
        prices_arr = prices.values
        weights = self._alma_weights
        if len(prices_arr) < self._window:
            return None
        else:
            weighted_sum = weights * prices_arr
            alma = weighted_sum.sum() / weights.sum()
            return alma


    def alma_weights(self, window, offset=0.85, sigma=6):
        """
        Calculates ALMA weights and returns array
        """
        m = int(offset * (window - 1))
        s = (window / sigma)
        k_all = np.linspace(0, window - 1, window)
        weights = np.exp(-((k_all - m) ** 2) / (2 * (s ** 2)))
        return weights
