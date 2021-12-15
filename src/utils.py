from collections import Counter

from src.parameters import PersonParameters


def count_people(colors):
    counts = Counter(colors)
    return {
        "healthy": (counts[PersonParameters.HEALTHY_COLOR], PersonParameters.HEALTHY_COLOR),
        "sick": (counts[PersonParameters.SICK_COLOR], PersonParameters.SICK_COLOR),
        "recovered": (counts[PersonParameters.RECOVERED_COLOR], PersonParameters.RECOVERED_COLOR),
    }
