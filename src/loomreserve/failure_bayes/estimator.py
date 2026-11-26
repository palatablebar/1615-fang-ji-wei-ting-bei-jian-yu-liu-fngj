from dataclasses import dataclass
from math import exp, log
import numpy as np

from .contracts import LearningRow, Probe


@dataclass(frozen=True)
class WeftEvidence:
    means: np.ndarray
    variance: np.ndarray
    prior: float
    press_prior: dict[str, float]
    samples: tuple[int, int]

    def predict(self, probe: Probe) -> float:
        measured = np.asarray(probe.standard)
        probability = self.press_prior.get(probe.region, self.prior)
        likelihood = -.5 * np.sum(np.log(self.variance) + (measured - self.means) ** 2 / self.variance, axis=1)
        posterior = float(likelihood[1] - likelihood[0]) + log(probability/(1-probability))
        if posterior >= 0:
            return 1/(1 + exp(-posterior))
        likelihood_factor = exp(posterior)
        return likelihood_factor/(1 + likelihood_factor)

    def describe(self) -> dict:
        return {'stop_class_counts': list(self.samples), 'means': self.means.tolist(), 'variance_floor': .115,
                'regional_failure_prior': self.press_prior, 'overall_failure_prior': self.prior,
                'class_variance': self.variance.tolist()}


def fit_estimator(rows: tuple[LearningRow, ...]) -> WeftEvidence:
    measured = np.asarray([r.probe.standard for r in rows])
    failed = np.asarray([bool(r.outcome) for r in rows])
    size = len(rows)
    prior = (sum(failed)+2)/(size+6)
    anchor = np.median(measured, axis=0)
    spread = np.maximum(.115, measured.var(axis=0))
    means = []
    variance = []
    counts = []
    for outcome in (False, True):
        cluster = measured[failed == outcome]
        counts.append(len(cluster))
        shrunk = (cluster.sum(axis=0) + 3 * anchor)/(len(cluster)+3)
        deviations = ((cluster-shrunk) ** 2).sum(axis=0)
        means.append(shrunk)
        variance.append(np.maximum(.115, (deviations+5*spread)/(len(cluster)+5)))
    family = {}
    for region in sorted({row.probe.region for row in rows}):
        local = [bool(row.outcome) for row in rows if row.probe.region == region]
        family[region] = float((sum(local)+prior*10)/(len(local)+10))
    return WeftEvidence(np.asarray(means), np.asarray(variance), float(prior), family, tuple(counts))
