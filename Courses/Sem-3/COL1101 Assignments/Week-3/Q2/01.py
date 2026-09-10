EPS = 1e-6

### No need to edit parts
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
        
        self.max_speed=max_speed
        self.position=position
        self.velocity=velocity
        
        ## Initally zero already 
        self.acceleration=(0,0,0)
        self.time=0
        
        ## Terminal Status
        self.complete=False

         
    def current(self,time):
        "Returns position and velcity at given time"
        t=time-self.time
            
        ## Applying x_t = x_0 + v*t + 1/2*a*t**2
        px=self.position[0] + self.velocity[0] * t +0.5*self.acceleration[0] *t*t
        py=self.position[1] + self.velocity[1] * t +0.5*self.acceleration[1] *t*t
        pz=self.position[2] + self.velocity[2] * t +0.5*self.acceleration[2] *t*t
        
        
        ## Applying v_t = v_0 + a*t
        vx=self.velocity[0] + self.acceleration[0] * t
        vy=self.velocity[1] + self.acceleration[1] * t
        vz=self.velocity[2] + self.acceleration[2] * t
        
        
        pos=(px,py,pz)
        vel=(vx,vy,vz)
        return pos,vel

    def set_acceleration(self, time, acceleration):
        """
        time : the instant from which the new acceleration applies
        acceleration : a tuple (ax, ay, az) of integers
        
        A flight that has already finished ignores this instruction.
        """
        if self.complete:   return
        
        self.position, self.velocity = self.current(time)
        
        ## Time now updates itself to current state
        self.time=time
        self.acceleration=acceleration
        
        
        
    def status(self, time):
        """
        Return this flight’s status at the given instant: "flying",
        "accident" or "landed safely".
        """
        
        vx,vy,vz=self.velocity
        ax,ay,az=self.acceleration
        
        
        
        vel=(vx*vx + vy*vy + vz*vz)**0.5
        acc=(ax*ax + ay*ay + az*az)**0.5
        
        ## First case of accident
        if is_greater(vel, self.max_speed):   return "accident"
        
        ## Second case of accident
        z=self.position[2]
        if (is_equal(z,0) and not(is_greater(vel,0) or is_greater(acc,0))):    return "accident"
        
        return "flying"


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














