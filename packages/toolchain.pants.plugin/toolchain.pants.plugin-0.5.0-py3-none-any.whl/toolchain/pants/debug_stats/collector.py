# Copyright © 2021 Toolchain Labs, Inc. All rights reserved.
#
# Toolchain Labs, Inc. CONFIDENTIAL
#
# This file includes unpublished proprietary source code of Toolchain Labs, Inc.
# The copyright notice above does not evidence any actual or intended publication of such source code.
# Disclosure of this source code or any related proprietary information is strictly prohibited without
# the express written permission of Toolchain Labs, Inc.
import base64
import logging
import textwrap
from collections import Counter
from io import BytesIO
from typing import Tuple

from pants.engine.internals.scheduler import Workunit
from pants.engine.rules import collect_rules, rule
from pants.engine.streaming_workunit_handler import (
    StreamingWorkunitContext,
    WorkunitsCallback,
    WorkunitsCallbackFactory,
    WorkunitsCallbackFactoryRequest,
)
from pants.engine.unions import UnionRule
from pants.option.subsystem import Subsystem

has_histogram_module = False
try:
    from hdrh.histogram import HdrHistogram

    has_histogram_module = True
except ImportError:
    pass


logger = logging.getLogger(__name__)


class StatsCollectorSubsystem(Subsystem):
    options_scope = "debug-stats"
    help = """Configuration for stats collector subsystem."""

    @classmethod
    def register_options(cls, register):
        register(
            "--enable",
            advanced=True,
            type=bool,
            default=False,
            help="Enable aggregating and displaying Pants-internal stats.",
        )

    @property
    def enabled(self) -> bool:
        return self.options.enable


class StatsCollectorCallback(WorkunitsCallback):
    def __init__(self, enabled: bool):
        self.enabled = enabled
        self.counters: Counter = Counter()

    def __call__(
        self,
        *,
        started_workunits: Tuple[Workunit, ...],
        completed_workunits: Tuple[Workunit, ...],
        finished: bool,
        context: StreamingWorkunitContext,
    ) -> None:
        if not self.enabled:
            return

        # Aggregate counters on completed workunits.
        for workunit in completed_workunits:
            if "counters" in workunit:
                for name, value in workunit["counters"].items():
                    self.counters[name] += value

        # When done, print out information on counters and observation histograms.
        if not finished:
            return

        # Log aggregated counters.
        logger.info("Counters:")
        for name in sorted(self.counters.keys()):
            logger.info(f"  {name}: {self.counters[name]}")

        # Retrieve all of the observation histograms.
        histogram_info = context.get_observation_histograms()
        logger.info("Observation Histograms:")
        for name, encoded_histogram in histogram_info["histograms"].items():
            # Note: The Python library for HDR Histogram will only decode compressed histograms that are
            # further encoded with base64. See https://github.com/HdrHistogram/HdrHistogram_py/issues/29.
            histogram = HdrHistogram.decode(base64.b64encode(encoded_histogram))
            buffer = BytesIO()
            histogram.output_percentile_distribution(buffer, 1)
            logger.info(f"  Histogram for `{name}`:\n{textwrap.indent(buffer.getvalue().decode(), '    ')}")


class StatsCollectorCallbackFactoryRequest:
    """A unique request type that is installed to trigger construction of our WorkunitsCallback."""


@rule
def construct_callback(
    _: StatsCollectorCallbackFactoryRequest,
    stats_collector: StatsCollectorSubsystem,
) -> WorkunitsCallbackFactory:
    enabled = stats_collector.enabled
    if enabled and not has_histogram_module:
        enabled = False
        logger.warning(
            "The `hdrhistogram` package from PyPi is required to use the debug_stats plugin. "
            "Please add hdrhistogram to the --plugins config option."
        )

    return WorkunitsCallbackFactory(
        lambda: StatsCollectorCallback(enabled),
    )


def rules():
    return [
        UnionRule(WorkunitsCallbackFactoryRequest, StatsCollectorCallbackFactoryRequest),
        *collect_rules(),
    ]
