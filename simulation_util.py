import random
from scipy.stats import truncnorm
import numpy as np
from simulation_const import REGULATION, SYNTAX_ELEMENT_COUNT_CAP


def calc_complexity(frequency):
    regulation = REGULATION
    if(frequency>=SYNTAX_ELEMENT_COUNT_CAP): return 1
    return ((frequency)**(1/regulation))/(1+((frequency)**(1/regulation))) 

def calc_frequency(complexity):
    regulation = REGULATION
    if(complexity>=1): return SYNTAX_ELEMENT_COUNT_CAP
    x = -complexity/(1-complexity)
    if(x<0): x = x*-1
    result = x**regulation
    if(result>SYNTAX_ELEMENT_COUNT_CAP): return SYNTAX_ELEMENT_COUNT_CAP
    return result

def create_random_task(dql_model: dict[str, list[str]]):
    return {key: [random.randint(0, 7) for _ in dql_model[key]] for key in dql_model}

def create_optimal_task(dql_model: dict[str, list[str]], learner_competency: dict[str, list[float]], scaffolding_bonus: dict[str, list[float]]):
    return {
        key: [
            calc_frequency(learner_competency[key][i] + scaffolding_bonus[key][i]) for i in range(len(dql_model[key]))
        ] for key in dql_model
    }
    
def calc_task_complexities(task: dict[str, list[int]]):
    return {key: calc_complexity_for_category(category) for key, category in task.items()}


def calc_complexity_for_category(category: list[int]):
    return list(calc_complexity(frequency) for frequency in category)
    


def calculate_delta(learner_competency: dict[str, list[str]], task_complexities: dict[str, list[str]], scaffolding_bonus: dict[str, list[str]]):
    result = {}
    for key in learner_competency:
        result[key] = []
        for i in range(len(learner_competency[key])):
            k = learner_competency[key][i]
            c = task_complexities[key][i]
            t = scaffolding_bonus[key][i]
            if (c <= k or c > k + t):
                result[key].append(0)
            else:
                result[key].append(c - k)
    return result


def add_delta_to_competency(competency: dict[str, list[str]], delta: dict[str, list[str]]):
    return {key: [competency[key][i] + delta[key][i] for i in range(len(competency[key]))] for key in competency}

def rgbeta(n: int, mean: float, var: float, min: float = 0, max: float = 1) -> float:
    dmin = mean - min
    dmax = max - mean

    if dmin <= 0 or dmax <= 0:
        raise ValueError(f"mean must be between min = {min} and max = {max}")

    if var >= dmin * dmax:
        raise ValueError(
            f"var must be less than (mean - min) * (max - mean) = {dmin * dmax}")

    mx = (mean - min) / (max - min)
    vx = var / (max - min) ** 2

    a = ((1 - mx) / vx - 1 / mx) * mx ** 2
    b = a * (1 / mx - 1)

    x = np.random.beta(a, b, n)
    y = (max - min) * x + min

    return y.tolist()


def create_learner_scaffolded_competence_bonuses(dql_model: dict[str, list[str]], bonus_distribution: tuple[4]):
    return {key: rgbeta(len(dql_model[key]), *bonus_distribution) for key in dql_model}


def sample_from_snd_vectorized_and_normalize(X: list[float], mean=0.5, sd=0.1):
    # Generate random normal samples and normalize
    lower, upper = 0, 1
    a, b = (lower - mean) / sd, (upper - mean) / sd
    samples = truncnorm.rvs(a, b, loc=mean, scale=sd, size=len(X))
    return (samples).tolist()


def create_learner_competencies(dql_model: dict[str, list[str]], mean: float):
    return {key: sample_from_snd_vectorized_and_normalize(dql_model[key], mean) for key in dql_model}


def create_learner_population(learner_count: int, task_count: int, dql_model: dict[str, list[str]], mean_competency: float, bonus_distribution: tuple[4]):
    population = {
        "learner_competencies": [create_learner_competencies(dql_model, mean=mean_competency) for _ in range(learner_count)],
        "scaffolding_competence_bonus_per_step_and_learner": [[create_learner_scaffolded_competence_bonuses(dql_model, bonus_distribution) for _ in range(learner_count)] for _ in range(task_count)]
    }
    return population