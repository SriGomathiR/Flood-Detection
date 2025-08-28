# ga.py
import random
from typing import Dict, Tuple
from dataclasses import dataclass

@dataclass
class GAConfig:
    pop_size: int = 30
    gens: int = 40
    elite: int = 2
    tournament_k: int = 4
    mutation_rate: float = 0.2
    mutation_scale: float = 2.0
    seed: int = 42

class ThresholdGA:
    """GA that evolves thresholds for flood-risk rules with realistic weights."""
    def __init__(self, config: GAConfig):
        self.cfg = config
        random.seed(self.cfg.seed)

        # Reasonable ranges for thresholds
        self.bounds = {
            "rain_th": (0.5, 20.0),      # mm in last hour, lowered min to catch light rain
            "hum_th": (50.0, 100.0),     # % humidity
            "temp_max_th": (25.0, 40.0), # deg C
            "wind_th": (3.0, 15.0),      # m/s, lower to catch moderate wind
        }

        # Weights reflect importance for flood detection
        self.weights = {
            "rain": 3.0,    # rainfall dominates
            "hum": 2.0,     # humidity important
            "temp": 1.0,    
            "wind": 1.0,
        }

    def _rand_individual(self) -> Dict[str, float]:
        return {k: random.uniform(lo, hi) for k, (lo, hi) in self.bounds.items()}

    def _mutate(self, indiv: Dict[str, float]) -> Dict[str, float]:
        if random.random() < self.cfg.mutation_rate:
            gene = random.choice(list(indiv.keys()))
            lo, hi = self.bounds[gene]
            indiv[gene] += random.uniform(-self.cfg.mutation_scale, self.cfg.mutation_scale)
            indiv[gene] = max(lo, min(hi, indiv[gene]))
        return indiv

    def _crossover(self, p1: Dict[str, float], p2: Dict[str, float]) -> Tuple[Dict[str, float], Dict[str, float]]:
        child1, child2 = {}, {}
        for k in p1.keys():
            if random.random() < 0.5:
                child1[k], child2[k] = p1[k], p2[k]
            else:
                child1[k], child2[k] = p2[k], p1[k]
        return child1, child2

    def _fitness(self, indiv: Dict[str, float], feats: Dict[str, float]) -> float:
        score = 0.0
        if feats.get("rain_1h", 0.0) > indiv["rain_th"]:
            score += self.weights["rain"]
        if feats.get("humidity", 0.0) > indiv["hum_th"]:
            score += self.weights["hum"]
        if feats.get("temp_c", 0.0) < indiv["temp_max_th"]:
            score += self.weights["temp"]
        if feats.get("wind_speed", 0.0) > indiv["wind_th"]:
            score += self.weights["wind"]
        return score

    def evolve(self, feats: Dict[str, float], progress: bool=True) -> Dict[str, float]:
        pop = [self._rand_individual() for _ in range(self.cfg.pop_size)]
        def fitness(ind): return self._fitness(ind, feats)

        for g in range(self.cfg.gens):
            pop.sort(key=fitness, reverse=True)
            if progress and (g % 5 == 0 or g == self.cfg.gens - 1):
                best = pop[0]
                print(f"[Gen {g:02d}] best fitness={fitness(best):.2f} thresholds={best}")

            new_pop = pop[:self.cfg.elite]
            while len(new_pop) < self.cfg.pop_size:
                cand = random.sample(pop[: max(self.cfg.tournament_k * 2, 8)], self.cfg.tournament_k)
                cand2 = random.sample(pop[: max(self.cfg.tournament_k * 2, 8)], self.cfg.tournament_k)
                p1, p2 = max(cand, key=fitness), max(cand2, key=fitness)
                c1, c2 = self._crossover(p1, p2)
                new_pop.append(self._mutate(c1))
                if len(new_pop) < self.cfg.pop_size:
                    new_pop.append(self._mutate(c2))
            pop = new_pop

        pop.sort(key=fitness, reverse=True)
        return pop[0]

def classify_risk(feats: Dict[str, float], th: Dict[str, float]) -> Tuple[str, float]:
    """Return (label, score_fraction) with rain dominating the decision."""
    rain = feats.get("rain_1h", 0.0)
    hum = feats.get("humidity", 0.0)
    temp = feats.get("temp_c", 0.0)
    wind = feats.get("wind_speed", 0.0)

    # 0 rainfall → LOW risk immediately
    if rain < 1.0:
        return "LOW", 0.0

    satisfied = 0
    total = 4

    if rain > th.get("rain_th", 5.0):
        satisfied += 1
    if hum > th.get("hum_th", 80.0):
        satisfied += 1
    if temp < th.get("temp_max_th", 30.0):
        satisfied += 1
    if wind > th.get("wind_th", 6.0):
        satisfied += 1

    frac = satisfied / total

    if frac >= 0.75:
        return "HIGH", frac
    elif frac >= 0.5:
        return "MEDIUM", frac
    else:
        return "LOW", frac

