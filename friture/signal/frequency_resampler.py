#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 Timothée Lecomte

# This file is part of Friture.
#
# Friture is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# Friture is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Friture.  If not, see <http://www.gnu.org/licenses/>.


import logging

import numpy as np
import friture.plotting.frequency_scales as fscales

class Frequency_Resampler:

    def __init__(self, scale=fscales.Linear, minfreq: float = 20., maxfreq: float = 20000., nsamples: int = 1) -> None:
        self.logger = logging.getLogger(__name__)

        self.scale = scale 
        self.minfreq: float = minfreq
        self.maxfreq: float = maxfreq
        self.nsamples: int = nsamples
        self.freq = np.zeros((1))
        self.update_xscale()

    def setfreqrange(self, minfreq: float, maxfreq: float) -> None:
        self.logger.info("freq range changed %f %f", minfreq, maxfreq)
        self.minfreq = minfreq
        self.maxfreq = maxfreq
        self.update_xscale()

    def update_xscale(self) -> None:
        self.xscaled = self.scale.inverse(
            np.linspace(
                self.scale.transform(self.minfreq),
                self.scale.transform(self.maxfreq),
                self.nsamples))

    def setnsamples(self, nsamples):
        if self.nsamples != nsamples:
            self.nsamples = nsamples
            self.update_xscale()
            self.logger.info("nsamples changed, now: %d", nsamples)

    def setfreqscale(self, scale) -> None:
        if scale != self.scale:
            self.logger.info("freq scale changed to %s", scale.NAME)
            self.scale = scale
            self.update_xscale()
        
    def setfreq(self, freq) -> None:
        self.freq = freq
        self.update_xscale()

    def push(self, data):
        # f = interp1d(freq, data) # construct an interpolant
        # return f(self.xscaled)
        # s = UnivariateSpline(freq, data, s=0, k=1) # construct the spline
        # return s(self.xscaled)
        # Note : interp1d and UnivariateSpline are both slower than interp
        # interp is still not optimal because it involved a search whereas
        # the data is already completely sorted so an running interpolation
        # could be done faster
        n = data.shape[1]
        resampled_data = np.zeros((self.xscaled.size, n))

        for j in range(n):
            interpolated = np.interp(self.xscaled, self.freq, data[:, j])
            resampled_data[:, j] = interpolated

        return resampled_data
