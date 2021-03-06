from collections import Counter, defaultdict

from src.parameters import PersonParameters


def count_people(colors):
    counts = Counter(colors)
    return {
        "healthy": (counts[PersonParameters.HEALTHY_COLOR], PersonParameters.HEALTHY_COLOR),
        "sick": (counts[PersonParameters.SICK_COLOR], PersonParameters.SICK_COLOR),
        "recovered": (counts[PersonParameters.RECOVERED_COLOR], PersonParameters.RECOVERED_COLOR),
    }

def count_peeps(colors):
    counts = Counter(colors)
    peeps = defaultdict(int)
    peeps["healthy"] = counts[PersonParameters.HEALTHY_COLOR]
    peeps["sick"] = counts[PersonParameters.SICK_COLOR]
    peeps["recovered"] = counts[PersonParameters.RECOVERED_COLOR]
    return peeps
    
def get_population_health_status(colors):
    counts = Counter(colors)
    return (
        counts[PersonParameters.HEALTHY_COLOR],
        counts[PersonParameters.SICK_COLOR],
        counts[PersonParameters.RECOVERED_COLOR],
    )

def get_population_health_status_keys():
    return "healthy", "sick", "recovered"
