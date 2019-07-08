"""Calculation of examination statistics."""


GRADES = [100, 100, 90, 40, 80, 100, 85, 70, 90, 65, 90, 85, 50.5]


def print_grades(grades_input):
    """Display grades on the screen."""

    for grade in grades_input:
        print grade


def grades_sum(scores):
    """Calculation of the sum of grades."""

    res = sum([grade for grade in scores])
    return res


def grades_average(grades_input):
    """Calculation of the mean of the grades."""

    average = grades_sum(grades_input) / float(len(grades_input))
    return average


def grades_variance(scores):
    """Variance calculation."""

    average = grades_average(scores)
    return sum([(average - score) ** 2 / len(scores) for score in scores])


def grades_std_deviation(variance):
    """Standard deviation"""

    return variance ** 0.5


print_grades(GRADES)
print grades_sum(GRADES)
print grades_average(GRADES)
print grades_variance(GRADES)
VARIANCE = grades_variance(GRADES)
print grades_std_deviation(VARIANCE)
