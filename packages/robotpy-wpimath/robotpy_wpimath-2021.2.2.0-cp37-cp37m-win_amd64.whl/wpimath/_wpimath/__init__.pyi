import wpimath._wpimath
import typing

__all__ = [
    "LinearFilter",
    "MedianFilter",
    "angleModulus"
]


class LinearFilter():
    """
    This class implements a linear, digital filter. All types of FIR and IIR
    filters are supported. Static factory methods are provided to create commonly
    used types of filters.

    Filters are of the form:
    y[n] = (b0 * x[n] + b1 * x[n-1] + � + bP * x[n-P]) -
    (a0 * y[n-1] + a2 * y[n-2] + � + aQ * y[n-Q])

    Where:
    y[n] is the output at time "n"
    x[n] is the input at time "n"
    y[n-1] is the output from the LAST time step ("n-1")
    x[n-1] is the input from the LAST time step ("n-1")
    b0 � bP are the "feedforward" (FIR) gains
    a0 � aQ are the "feedback" (IIR) gains
    IMPORTANT! Note the "-" sign in front of the feedback term! This is a common
    convention in signal processing.

    What can linear filters do? Basically, they can filter, or diminish, the
    effects of undesirable input frequencies. High frequencies, or rapid changes,
    can be indicative of sensor noise or be otherwise undesirable. A "low pass"
    filter smooths out the signal, reducing the impact of these high frequency
    components.  Likewise, a "high pass" filter gets rid of slow-moving signal
    components, letting you detect large changes more easily.

    Example FRC applications of filters:
    - Getting rid of noise from an analog sensor input (note: the roboRIO's FPGA
    can do this faster in hardware)
    - Smoothing out joystick input to prevent the wheels from slipping or the
    robot from tipping
    - Smoothing motor commands so that unnecessary strain isn't put on
    electrical or mechanical components
    - If you use clever gains, you can make a PID controller out of this class!

    For more on filters, we highly recommend the following articles:
    https://en.wikipedia.org/wiki/Linear_filter
    https://en.wikipedia.org/wiki/Iir_filter
    https://en.wikipedia.org/wiki/Fir_filter

    Note 1: Calculate() should be called by the user on a known, regular period.
    You can use a Notifier for this or do it "inline" with code in a
    periodic function.

    Note 2: For ALL filters, gains are necessarily a function of frequency. If
    you make a filter that works well for you at, say, 100Hz, you will most
    definitely need to adjust the gains if you then want to run it at 200Hz!
    Combining this with Note 1 - the impetus is on YOU as a developer to make
    sure Calculate() gets called at the desired, constant frequency!
    """
    def __init__(self, ffGains: typing.List[float], fbGains: typing.List[float]) -> None: 
        """
        Create a linear FIR or IIR filter.

        :param ffGains: The "feed forward" or FIR gains.
        :param fbGains: The "feed back" or IIR gains.
        """
    def calculate(self, input: float) -> float: 
        """
        Calculates the next value of the filter.

        :param input: Current input value.

        :returns: The filtered value at this step
        """
    @staticmethod
    def highPass(timeConstant: float, period: seconds) -> LinearFilter: 
        """
        Creates a first-order high-pass filter of the form:
        y[n] = gain * x[n] + (-gain) * x[n-1] + gain * y[n-1]
        where gain = e<sup>-dt / T</sup>, T is the time constant in seconds

        This filter is stable for time constants greater than zero.

        :param timeConstant: The discrete-time time constant in seconds.
        :param period:       The period in seconds between samples taken by the
                             user.
        """
    @staticmethod
    def movingAverage(taps: int) -> LinearFilter: 
        """
        Creates a K-tap FIR moving average filter of the form:
        y[n] = 1/k * (x[k] + x[k-1] + � + x[0])

        This filter is always stable.

        :param taps: The number of samples to average over. Higher = smoother but
                     slower
        """
    def reset(self) -> None: 
        """
        Reset the filter state.
        """
    @staticmethod
    def singlePoleIIR(timeConstant: float, period: seconds) -> LinearFilter: 
        """
        Creates a one-pole IIR low-pass filter of the form:
        y[n] = (1 - gain) * x[n] + gain * y[n-1]
        where gain = e<sup>-dt / T</sup>, T is the time constant in seconds

        This filter is stable for time constants greater than zero.

        :param timeConstant: The discrete-time time constant in seconds.
        :param period:       The period in seconds between samples taken by the
                             user.
        """
    pass
class MedianFilter():
    """
    A class that implements a moving-window median filter.  Useful for reducing
    measurement noise, especially with processes that generate occasional,
    extreme outliers (such as values from vision processing, LIDAR, or ultrasonic
    sensors).
    """
    def __init__(self, size: int) -> None: 
        """
        Creates a new MedianFilter.

        :param size: The number of samples in the moving window.
        """
    def calculate(self, next: float) -> float: 
        """
        Calculates the moving-window median for the next value of the input stream.

        :param next: The next input value.

        :returns: The median of the moving window, updated to include the next value.
        """
    def reset(self) -> None: 
        """
        Resets the filter, clearing the window of all elements.
        """
    pass
def angleModulus(angle: radians) -> radians:
    """
    Wraps an angle to the range -pi to pi radians (-180 to 180 degrees).

    :param angle: Angle to wrap.
    """
