import attr
import numpy as np
from pybbda.analysis.utils import check_greater_zero
from pybbda.utils import Singleton


@attr.s(frozen=True, kw_only=True)
class BattedBallConstants:
    mass = attr.ib(
        default=5.125, validator=check_greater_zero, metadata={"units": "oz"}
    )
    circumference = attr.ib(
        default=9.125, validator=check_greater_zero, metadata={"units": "in"}
    )


@attr.s(frozen=True, kw_only=True)
class DragForceCoefficients:
    cd0 = attr.ib(default=0.3008)
    cdspin = attr.ib(default=0.0292)


@attr.s(frozen=True, kw_only=True)
class LiftForceCoefficients:
    cl0 = attr.ib(default=0.583)
    cl1 = attr.ib(default=2.333)
    cl2 = attr.ib(default=1.120)
    tau = attr.ib(default=10000, metadata={"units": "seconds"})


@attr.s(kw_only=True)
class EnvironmentalParameters:
    # environmental parameters
    g_gravity = attr.ib(default=32.174, metadata={"units": "ft_per_s_per_s"})
    vwind = attr.ib(default=0, metadata={"units": "mph"})  # mph
    phiwind = attr.ib(default=0, metadata={"units": "deg"})  # deg
    hwind = attr.ib(default=0, metadata={"units": "ft"})  # ft
    relative_humidity = attr.ib(default=50)
    pressure_in_hg = attr.ib(default=29.92)
    temperature_f = attr.ib(default=70, metadata={"units": "F"})  # F
    elevation_ft = attr.ib(default=15, metadata={"units": "ft"})
    beta = attr.ib(
        default=1.217e-4, validator=check_greater_zero, metadata={"units": "per_meter"}
    )

    def __attrs_post_init__(self):
        self.unit_conversions = UnitConversions()
        self.elevation_m = self.elevation_ft * self.unit_conversions.ft_to_m
        self.temperature_c = (self.temperature_f - 32) * 5 / 9
        self.pressure_mm_hg = self.pressure_in_hg * 1000 / 39.37
        self.SVP = 4.5841 * np.exp(
            (18.687 - self.temperature_c / 234.5)
            * self.temperature_c
            / (257.14 + self.temperature_c)
        )

        self.air_density = 1.2929 * (
            273
            / (self.temperature_c + 273)
            * (
                self.pressure_mm_hg * np.exp(-self.beta * self.elevation_m)
                - 0.3783 * self.relative_humidity * self.SVP * 0.01
            )
            / 760
        )


@attr.s(frozen=True, kw_only=True)
class UnitConversions(Singleton):
    # conversions,
    mph_to_fts = attr.ib(default=1.467)
    ft_to_m = attr.ib(default=0.3048037)
    lbft3_to_kgm3 = attr.ib(default=16.01848)
    kgm3_to_lbft3 = attr.ib(default=0.06242789)
