EPS = 1e-6

def is_equal(x, y):
    return abs(x-y) <= EPS

def is_less(x, y):
    return x < y-EPS

def is_greater(x, y):
    return x > y+EPS

def is_less_equal(x, y):
    return not is_greater(x, y)

def is_greater_equal(x, y):
    return not is_less(x, y)


def roots(a,b,c):
    if is_equal(a,0):
        if is_equal(b,0):
            return []
        return [-c/b]

    d=b*b-4*a*c

    if is_less(d,0):
        return []

    d=max(0,d)**0.5
    return [(-b-d)/(2*a),(-b+d)/(2*a)]


class Flight:

    def __init__(self,max_speed,position,velocity):
        self.max_speed=max_speed
        self.position=position
        self.velocity=velocity
        self.acceleration=(0,0,0)
        self.time=0
        self.complete=False
        self.finish=None

        self.check_initial()

    def current(self,time):
        t=time-self.time

        p=tuple(
            self.position[i]+
            self.velocity[i]*t+
            0.5*self.acceleration[i]*t*t
            for i in range(3)
        )

        v=tuple(
            self.velocity[i]+self.acceleration[i]*t
            for i in range(3)
        )

        return p,v

    def check_initial(self):
        speed2=sum(x*x for x in self.velocity)

        if is_greater(speed2,self.max_speed**2):
            self.complete=True
            self.finish="accident"
            return

        z=self.position[2]
        vz=self.velocity[2]

        if is_less(z,0):
            self.complete=True
            self.finish="accident"
            return

        if is_equal(z,0):

            if is_less(vz,0):
                self.complete=True
                self.finish="accident"
                return

            if (
                all(is_equal(x,0) for x in self.velocity)
                and
                all(is_equal(x,0) for x in self.acceleration)
            ):
                self.complete=True
                self.finish="landed safely"

    def next_event(self):
        if self.complete:
            return None

        vx,vy,vz=self.velocity
        ax,ay,az=self.acceleration

        events=[]

        # Speed limit
        A=ax*ax+ay*ay+az*az
        B=2*(vx*ax+vy*ay+vz*az)
        C=vx*vx+vy*vy+vz*vz-self.max_speed**2

        if is_greater(C,0):
            events.append((0,"accident"))

        else:
            for t in roots(A,B,C):
                if is_greater_equal(t,0):
                    # We need the upward crossing.
                    if is_greater(2*A*t+B,0):
                        events.append((t,"accident"))

        # Ground
        for t in roots(0.5*az,vz,self.position[2]):

            if not is_greater_equal(t,0):
                continue

            vz2=vz+az*t

            if is_less(vz2,0):
                events.append((t,"accident"))

            elif (
                is_equal(vz2,0)
                and is_equal(az,0)
                and
                is_equal(
                    self.velocity[0]+ax*t,0
                )
                and
                is_equal(
                    self.velocity[1]+ay*t,0
                )
            ):
                events.append((t,"landed safely"))

        if not events:
            return None

        # Speed/ground event at same time:
        # speed accident has priority.
        return min(
            events,
            key=lambda x:(x[0],0 if x[1]=="accident" else 1)
        )

    def finish_at(self,t,typ):
        self.position,self.velocity=self.current(t)
        self.time=t
        self.complete=True
        self.finish=typ

    def set_acceleration(self,time,acceleration):
        if self.complete:
            return

        # IMPORTANT:
        # Check whether something happened before this instruction.
        self.status(time)

        if self.complete:
            return

        self.position,self.velocity=self.current(time)
        self.time=time
        self.acceleration=acceleration

        self.check_initial()

    def status(self,time):

        if self.complete:
            return self.finish

        e=self.next_event()

        if e is not None:

            dt,typ=e
            event_time=self.time+dt

            if typ=="accident":

                p,v=self.current(event_time)
                speed2=sum(x*x for x in v)

                # Speed limit is STRICT.
                if is_greater(speed2,self.max_speed**2):

                    if is_less(event_time,time):
                        self.finish_at(event_time,"accident")

                elif is_less_equal(event_time,time):

                    # Ground crash
                    if is_equal(p[2],0) and is_less(v[2],0):
                        self.finish_at(event_time,"accident")

            elif is_less_equal(event_time,time):
                self.finish_at(event_time,typ)

        return self.finish if self.complete else "flying"


class AirTrafficControl:

    def __init__(self):
        self.flights={}
        self.now=0

    def collision_time(self,f1,f2,start):
        p1,v1=f1.current(start)
        p2,v2=f2.current(start)

        p=tuple(p1[i]-p2[i] for i in range(3))
        v=tuple(v1[i]-v2[i] for i in range(3))
        a=tuple(
            f1.acceleration[i]-f2.acceleration[i]
            for i in range(3)
        )

        equation=None

        for i in range(3):
            if not (
                is_equal(a[i],0)
                and is_equal(v[i],0)
                and is_equal(p[i],0)
            ):
                equation=(0.5*a[i],v[i],p[i])
                break

        # They are at the same position and follow
        # the same trajectory.
        if equation is None:
            return start

        for t in roots(*equation):

            if not is_greater_equal(t,0):
                continue

            ok=True

            for i in range(3):
                x=(
                    0.5*a[i]*t*t+
                    v[i]*t+
                    p[i]
                )

                if not is_equal(x,0):
                    ok=False
                    break

            if ok:
                return start+t

        return None

    def process(self,target):

        current=self.now

        while True:

            best=None
            best_type=None
            best_data=None

            active=[
                f for f in self.flights.values()
                if not f.complete
            ]

            # ----------------------------
            # Individual flight events
            # ----------------------------

            for f in active:

                e=f.next_event()

                if e is None:
                    continue

                dt,typ=e
                t=f.time+dt

                if typ=="accident":

                    p,v=f.current(t)
                    speed2=sum(x*x for x in v)

                    # Speed exceeds max only AFTER root.
                    if is_greater(
                        speed2,f.max_speed**2
                    ):
                        if not is_less(t,target):
                            continue
                    elif not is_less_equal(t,target):
                        continue

                elif not is_less_equal(t,target):
                    continue

                if best is None or is_less(t,best):
                    best=t
                    best_type="single"
                    best_data=(f,typ)

            # ----------------------------
            # Collisions
            # ----------------------------

            active=[
                f for f in self.flights.values()
                if not f.complete
            ]

            for i in range(len(active)):
                for j in range(i+1,len(active)):

                    t=self.collision_time(
                        active[i],
                        active[j],
                        current
                    )

                    if t is None:
                        continue

                    if not is_less_equal(t,target):
                        continue

                    if best is None or is_less(t,best):
                        best=t
                        best_type="collision"
                        best_data=(
                            active[i],
                            active[j]
                        )

            if best is None:
                break

            # Move everybody to the event time.
            current=best

            for f in self.flights.values():

                if not f.complete:
                    f.position,f.velocity=f.current(best)
                    f.time=best

            # Individual event wins over collision
            # when both happen at exactly the same instant.
            if best_type=="single":

                f,typ=best_data

                if not f.complete:
                    f.complete=True
                    f.finish=typ

            else:

                f1,f2=best_data

                if not f1.complete and not f2.complete:
                    f1.complete=True
                    f1.finish="accident"

                    f2.complete=True
                    f2.finish="accident"

        self.now=target

        for f in self.flights.values():

            if not f.complete:
                f.position,f.velocity=f.current(target)
                f.time=target

    def create(
        self,
        time,
        flight_id,
        max_speed,
        position,
        velocity
    ):
        if flight_id in self.flights:
            return

        self.process(time)

        f=Flight(
            max_speed,
            position,
            velocity
        )

        f.time=time
        self.flights[flight_id]=f

        self.process(time)

    def update(self,time,flight_id,acceleration):

        self.process(time)

        if flight_id not in self.flights:
            return

        self.flights[flight_id].set_acceleration(
            time,
            acceleration
        )

    def status(self,time,flight_id):

        if flight_id not in self.flights:
            return "does not exist"

        self.process(time)

        f=self.flights[flight_id]

        if f.complete:
            return f.finish

        return "flying"
