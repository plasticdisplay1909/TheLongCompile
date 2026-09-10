EPS = 1e-6

def is_equal(x, y):
    """Return True when x and y should be treated as equal."""
    return abs(x - y) <= EPS


def is_less(x, y):
    """Return True when x is definitely smaller than y."""
    return x < y - EPS

def is_greater(x, y):
    """Return True when x is definitely greater than y."""
    return x > y + EPS
    
def is_less_equal(x, y):
    """Return True when x should be treated as less than or equal to y."""
    return not is_greater(x, y)
    
def is_greater_equal(x, y):
    """Return True when x should be treated as greater than or equal to y."""
    return not is_less(x, y)
    
class Flight:
    """A single aircraft."""
    def __init__(self, max_speed, position, velocity):
        """
        max_speed : int, the highest speed this flight may hold
        position : a tuple (x, y, z) of integers, where it starts
        velocity : a tuple (vx, vy, vz) of integers, its initial velocity
        
        A newly created flight has the given initial velocity and acceleration
        (0, 0, 0). Its status must already be correct at the moment it is
        created.
        """

    def set_acceleration(self, time, acceleration):
        """
        time : the instant from which the new acceleration applies
        acceleration : a tuple (ax, ay, az) of integers
        
        A flight that has already finished ignores this instruction.
        """
        
    def status(self, time):
        """
        Return this flight’s status at the given instant: "flying",
        "accident" or "landed safely".
        """
        return ""


class AirTrafficControl:
    """The controller, which owns every flight."""

    def __init__(self):
        """Start a new session, with no flights, at time 0."""

    def create(self, time, flight_id, max_speed, position, velocity):
        """Create a flight with the given position and initial velocity."""

    def update(self, time, flight_id, acceleration):
        """Send an acceleration instruction to a flight at the given instant."""

    def status(self, time, flight_id):
        """
        Return the status of the given flight at the given instant: "flying",
        "accident", "landed safely", or "does not exist" if no flight with
        that identifier has ever been created.
        """
        return ""
