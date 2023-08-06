import numpy as np
import warnings

from pobm.obm.desat import desat_embedding
from pobm._ErrorHandler import _check_shape_, WrongParameter
from pobm._ResultsClasses import HypoxicBurdenMeasuresResults


class HypoxicBurdenMeasures:
    """
    Class that calculates hypoxic burden features from SpO2 time series.
    """

    def __init__(self, begin: np.array, end: np.array, CT_Threshold: float = 90, CA_Baseline: float = None):
        """

        :param begin: Numpy array of indices of beginning of each desaturation event.
        :type begin: Numpy array
        :param end: Numpy array of indices of end of each desaturation event. begin and end should have the same length.
        :type end: Numpy array
        :param CT_Threshold: Percentage of the time spent below the “CT_Threshold” % oxygen saturation level.
        :type CT_Threshold: float, optional
        :param CA_Baseline: Baseline to compute the CA feature. Default value is mean of the signal.
        :type CA_Baseline: float, optional

        """

        if isinstance(begin, int):
            begin = np.array([begin])
        if isinstance(end, int):
            end = np.array([end])

        if len(begin) != len(end):
            raise WrongParameter("The parameters begin and end should have the same length")

        self.begin = begin
        self.end = end
        self.CT_Threshold = CT_Threshold
        self.CA_Baseline = CA_Baseline

    def compute(self, signal):
        """
        Computes all the biomarkers of this category.

        :param signal: 1-d array, of shape (N,) where N is the length of the signal
        :return: HypoxicBurdenMeasuresResults class containing the following features:

            - CA: Integral SpO2 below the xx SpO2 level normalized by the total recording time
            - CT: Percentage of the time spent below the xx% oxygen saturation level
            - POD: Percentage of oxygen desaturation events
            - AODmax: The area under the oxygen desaturation event curve, using the maximum SpO2 value as baseline and normalized by the total recording time
            - AOD100: Cumulative area of desaturations under the 100% SpO2 level as baseline and normalized by the total recording time


        Example:
        
        .. code-block:: python

            from pobm.obm.burden import HypoxicBurdenMeasures

            # Initialize the class with the desired parameters
            hypoxic_class = HypoxicBurdenMeasures(results_desat.begin, results_desat.end, CT_Threshold=90, CA_Baseline=90)
            
            # Compute the biomarkers
            results_hypoxic = hypoxic_class.compute(spo2_signal)

        """

        _check_shape_(signal)
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        return self.__comp_hypoxic(signal)

    def __comp_hypoxic(self, signal):
        """
        Helper function, to calculate the hypoxic burden biomarkers from the desaturations

        :param signal: 1-d array, of shape (N,) where N is the length of the signal
        :param desaturations_signal: dict with 2 keys:
            - begin: indices of begininning of each desaturation
            - end: indices of end of each desaturation
        :return: HypoxicBurdenMeasuresResults class containing the following features:

            * CA: Integral SpO2 below the xx SpO2 level normalized by the total recording time
            * CT: Percentage of the time spent below the xx% oxygen saturation level
            * POD: Percentage of oxygen desaturation events
            * AODmax: The area under the oxygen desaturation event curve, using the maximum SpO2 value as baseline
              and normalized by the total recording time
            * AOD100: Cumulative area of desaturations under the 100% SpO2 level as baseline and normalized
              by the total recording time

        """

        desaturations, desaturation_valid, desaturation_length_all, desaturation_int_100_all, \
        desaturation_int_max_all, _, _, _, _, _ = desat_embedding(self.begin, self.end, self.end)

        time_spo2_array = np.array(range(len(signal)))
        for (i, desaturation) in enumerate(desaturations):
            desaturation_idx = (time_spo2_array >= desaturation['Start']) & (time_spo2_array <= desaturation['End'])

            if np.sum(desaturation_idx) == 0:
                continue

            signal = np.array(signal)

            desaturation_spo2 = signal[desaturation_idx]
            desaturation_max = np.nanmax(desaturation_spo2)

            desaturation_valid[i] = True
            desaturation_length_all[i] = desaturation['Duration']
            desaturation_int_100_all[i] = np.nansum(100 - desaturation_spo2)
            desaturation_int_max_all[i] = np.nansum(desaturation_max - desaturation_spo2)

        desaturation_features = HypoxicBurdenMeasuresResults(self.comp_ca(signal),
                                                             self.comp_ct(signal),
                                                             0.0, 0.0, 0.0)
        if np.sum(desaturation_valid) != 0:
            desaturation_features.POD = np.nansum(desaturation_length_all[desaturation_valid]) / len(signal)
            desaturation_features.AODmax = np.nansum(desaturation_int_max_all[desaturation_valid]) / len(signal)
            desaturation_features.AOD100 = np.nansum(desaturation_int_100_all[desaturation_valid]) / len(signal)

        return desaturation_features

    def comp_ca(self, signal):
        """
        Compute the cumulative area biomarker

        :param signal: 1-d array, of shape (N,) where N is the length of the signal
        :return: CA, the cumulative area (float)

        """

        if self.CA_Baseline is None:
            self.CA_Baseline = np.nanmean(signal)

        res = 0
        for value in signal:
            if value < self.CA_Baseline:
                res += self.CA_Baseline - value

        return res / len(signal)

    def comp_ct(self, signal):
        """
        Compute the cumulative time biomarker

        :param signal: 1-d array, of shape (N,) where N is the length of the signal
        :return: CT, the cumulative time (float)

        """
        with np.errstate(invalid='ignore'):
            return 100 * len(signal[signal <= self.CT_Threshold]) / len(signal)
