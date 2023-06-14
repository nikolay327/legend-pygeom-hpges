from __future__ import annotations

import math

from pyg4ometry import geant4

from .base import HPGe


class InvertedCoax(HPGe):
    """An inverted-coaxial point contact germanium detector."""

    def _ic_solid(self):
        # return ordered r,z lists, default unit [mm]
        r, z = self._decode_polycone_coord()

        # build generic polycone, default [mm]
        hpge_solid = geant4.solid.GenericPolycone(
            self.name, 0, 2 * math.pi, r, z, self.registry
        )

        return hpge_solid

    def _decode_polycone_coord(self) -> tuple[list[float], list[float]]:
        c = self.metadata.geometry

        def _tan(a):
            return math.tan(math.pi * a / 180)

        r = []
        z = []

        if c.pp_contact.depth_in_mm > 0:
            r += [
                0,
                c.pp_contact.radius_in_mm,
                c.pp_contact.radius_in_mm,
            ]
            z += [
                c.pp_contact.depth_in_mm,
                c.pp_contact.depth_in_mm,
                0,
            ]
        else:
            r += [0]
            z += [0]

        r += [
            c.groove.radius_in_mm.inner,
            c.groove.radius_in_mm.inner,
            c.groove.radius_in_mm.outer,
            c.groove.radius_in_mm.outer,
        ]

        z += [
            0,
            c.groove.depth_in_mm,
            c.groove.depth_in_mm,
            0,
        ]

        if c.taper.bottom.height_in_mm > 0:
            r += [
                c.radius_in_mm
                - c.taper.bottom.height_in_mm * _tan(c.taper.bottom.angle_in_deg),
                c.radius_in_mm,
            ]

            z += [
                0,
                c.taper.bottom.height_in_mm,
            ]
        else:
            r += [c.radius_in_mm]
            z += [0]

        if c.taper.top.height_in_mm > 0:
            r += [
                c.radius_in_mm,
                c.radius_in_mm
                - c.taper.top.height_in_mm * _tan(c.taper.top.angle_in_deg),
            ]

            z += [
                c.height_in_mm - c.taper.top.height_in_mm,
                c.height_in_mm,
            ]
        else:
            r += [c.radius_in_mm]
            z += [c.height_in_mm]

        if c.taper.borehole.height_in_mm > 0:
            r += [
                c.borehole.radius_in_mm
                + c.taper.borehole.height_in_mm * _tan(c.taper.borehole.angle_in_deg),
                c.borehole.radius_in_mm,
            ]

            z += [
                c.height_in_mm,
                c.height_in_mm - c.taper.borehole.height_in_mm,
            ]
        else:
            r += [c.borehole.radius_in_mm]
            z += [c.height_in_mm]

        r += [
            c.borehole.radius_in_mm,
            0,
        ]

        z += [
            c.height_in_mm - c.borehole.depth_in_mm,
            c.height_in_mm - c.borehole.depth_in_mm,
        ]

        return r, z
