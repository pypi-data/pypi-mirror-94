"""
replica_exchange.py

author: C. Lockhart <chris@lockhartlab.org>
language: Python3
"""


import numpy as np


# Create a temperature schedule
def temp_schedule(temp_min=300, temp_max=440, n_temps=40, mode='geometric'):
    r"""
    Create a temperature schedule that could be used, for instance, with replica exchange.

    There are several choices for `mode`. Note that :math:`T` refers to the temperature at :math:`i = 1 ... R`, where
    :math:`T_1` is `temp_min` and :math:`T_R` is `temp_max`. In total, there are :math:`R` temperatures (= `n_temps`).

    * "geometric" [#]_

    .. math :: T_i = T_1 \left( \frac{T_R}{T_1} \right)^{\frac{i-1}{R-1}}

    * "linear"

    .. math :: T_i = T_1 + (i-1) \frac{T_R-T_1}{R-1}

    * "parabolic" (Note if `n_temps` is even, `temp_max` won't directly be sampled).

    .. math :: T_i = T_1 - \frac{T_R-T_1}{\left( \frac{R-1}{2} \right) ^2} (i-1) (i-R)

    Parameters
    ----------
    temp_min : float
        Lowest temperature
    temp_max : float
        Highest temperature
    n_temps : int
        Number of temperatures
    mode : str
        Mode to produce schedule. Valid options include "geometric", "linear", "parabolic". Any substring will match,
        but the preference should be to use the full option label. (Default: "geometric")

    Returns
    -------
    numpy.ndarray
        Temperature schedule

    Examples
    --------
    .. plot::
       :include-source:

       import matplotlib.pyplot as plt
       import molecular as mol

       n_temps = 10
       geometric = mol.temp_schedule(300, 440, n_temps, 'geometric')
       linear = mol.temp_schedule(300, 440, n_temps, 'linear')
       parabolic = mol.temp_schedule(300, 440, n_temps, 'parabolic')

       plt.figure()
       plt.plot(range(n_temps), geometric, label='geometric')
       plt.plot(range(n_temps), linear, label='linear')
       plt.plot(range(n_temps), parabolic, label='parabolic')
       plt.xlabel('index')
       plt.ylabel('temperature')
       plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
       plt.show()

    References
    ----------
    .. [#] Nymeyer, H., Gnanakaran, S., & García, A. E. (2004) Atomistic simulations of protein folding, using the
       replica exchange algorithm. *Methods Enzymol.* **383**: 119-149.
    """

    mode = mode.lower()

    if mode in 'geometric':
        schedule = temp_min * np.power(temp_max / temp_min, np.arange(n_temps) / (n_temps - 1.), dtype=np.float64)

    elif mode in 'linear':
        schedule = np.linspace(start=temp_min, stop=temp_max, num=n_temps)

    elif mode in 'parabolic':
        temp_range = temp_max - temp_min
        temp_ind = np.arange(n_temps)
        schedule = temp_min - (temp_range / np.square((n_temps - 1.) / 2.)) * temp_ind * (temp_ind - n_temps + 1.)

    else:
        raise AttributeError(f'mode {mode} not supported')

    return schedule


if __name__ == '__main__':
    print(temp_schedule(temp_min=300, temp_max=440, n_temps=5, mode='geometric'))
    # print(temp_schedule(temp_min=310, temp_max=500, n_temps=5, mode='parabolic'))