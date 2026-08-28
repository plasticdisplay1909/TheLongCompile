EPS = 1e-6

def is_equal(x,y):
    return abs(x-y) <= EPS

def is_less(x,y):
    return x < y-EPS

def is_greater(x,y):
    return x > y+EPS

def is_less_equal(x,y):
    return not is_greater(x,y)

def is_greater_equal(x,y):
    return not is_less(x,y)


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

        self._initial()

    def current(self,time):
        t=time-self.time

        p=tuple(
            self.position[i]+
            self.velocity[i]*t+
            .5*self.acceleration[i]*t*t
            for i in range(3)
        )

        v=tuple(
            self.velocity[i]+self.acceleration[i]*t
            for i in range(3)
        )

        return p,v

    def _initial(self):

        s=sum(x*x for x in self.velocity)

        if is_greater(s,self.max_speed*self.max_speed):
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

    def _event(self):

        if self.complete:
            return None

        vx,vy,vz=self.velocity
        ax,ay,az=self.acceleration

        ev=[]

        # ---------- SPEED ----------

        A=ax*ax+ay*ay+az*az
        B=2*(vx*ax+vy*ay+vz*az)
        C=vx*vx+vy*vy+vz*vz-self.max_speed**2

        if is_greater(C,0):
            ev.append((0,"speed"))

        else:
            for t in roots(A,B,C):
                if is_greater_equal(t,0):

                    d=2*A*t+B

                    # Crossing from <= max to > max
                    if is_greater(d,0):
                        ev.append((max(0,t),"speed"))

                    # Exactly tangent at max but immediately
                    # becomes greater afterwards.
                    elif is_equal(d,0) and is_greater(A,0):
                        ev.append((max(0,t),"speed"))

        # ---------- GROUND ----------

        for t in roots(.5*az,vz,self.position[2]):

            if not is_greater_equal(t,0):
                continue

            vz2=vz+az*t

            if is_less(vz2,0):
                ev.append((t,"ground"))

            elif (
                is_equal(vz2,0)
                and is_less(az,0)
            ):
                ev.append((t,"ground"))

            elif (
                is_equal(vz2,0)
                and is_equal(az,0)
                and
                is_equal(vx+ax*t,0)
                and
                is_equal(vy+ay*t,0)
            ):
                ev.append((t,"land"))

        if not ev:
            return None

        # Accident before landing if same instant
        return min(
            ev,
            key=lambda x:(x[0],0 if x[1]!="land" else 1)
        )

    def _finish(self,t,typ):

        self.position,self.velocity=self.current(t)
        self.time=t
        self.complete=True

        if typ=="land":
            self.finish="landed safely"
        else:
            self.finish="accident"

    def set_acceleration(self,time,acceleration):

        if self.complete:
            return

        self.status(time)

        if self.complete:
            return

        self.position,self.velocity=self.current(time)
        self.time=time
        self.acceleration=acceleration

        self._initial()

    def status(self,time):

        if self.complete:
            return self.finish

        e=self._event()

        if e is not None:

            dt,typ=e
            t=self.time+dt

            if typ=="speed":

                # Exactly max speed is OK.
                if is_less(t,time):
                    self._finish(t,"speed")

            else:

                if is_less_equal(t,time):
                    self._finish(t,typ)

        if not self.complete:
            self.position,self.velocity=self.current(time)
            self.time=time

        return self.finish if self.complete else "flying"


class AirTrafficControl:

    def __init__(self):
        self.flights={}
        self.time=0

    def _collision_time(self,f,g):

        p1,v1=f.current(self.time)
        p2,v2=g.current(self.time)

        p=tuple(p1[i]-p2[i] for i in range(3))
        v=tuple(v1[i]-v2[i] for i in range(3))
        a=tuple(
            f.acceleration[i]-g.acceleration[i]
            for i in range(3)
        )

        eq=None

        for i in range(3):
            if not (
                is_equal(a[i],0)
                and is_equal(v[i],0)
                and is_equal(p[i],0)
            ):
                eq=(.5*a[i],v[i],p[i])
                break

        # Same trajectory and same current position
        if eq is None:
            return self.time

        for t in roots(*eq):

            if not is_greater_equal(t,0):
                continue

            ok=True

            for i in range(3):

                x=(
                    .5*a[i]*t*t+
                    v[i]*t+
                    p[i]
                )

                if not is_equal(x,0):
                    ok=False
                    break

            if ok:
                return self.time+t

        return None

    def _process(self,target):

        while True:

            active=[
                f for f in self.flights.values()
                if not f.complete
            ]

            best=None
            single=[]

            # Find earliest individual event
            for f in active:

                e=f._event()

                if e is None:
                    continue

                dt,typ=e
                t=self.time+dt

                if typ=="speed":
                    if not is_less(t,target):
                        continue
                else:
                    if not is_less_equal(t,target):
                        continue

                if best is None or is_less(t,best):
                    best=t
                    single=[(f,typ)]

                elif is_equal(t,best):
                    single.append((f,typ))

            # Find earliest collision
            collision_time=None

            for i in range(len(active)):
                for j in range(i+1,len(active)):

                    t=self._collision_time(
                        active[i],active[j]
                    )

                    if t is None:
                        continue

                    if not is_less_equal(t,target):
                        continue

                    if (
                        collision_time is None
                        or is_less(t,collision_time)
                    ):
                        collision_time=t

            # Collision is considered only after
            # single-flight events at the same time.
            if (
                collision_time is not None
                and
                (
                    best is None
                    or is_less(collision_time,best)
                )
            ):
                best=collision_time
                single=[]

            if best is None:
                break

            # Move every surviving flight to event time
            self.time=best

            for f in self.flights.values():
                if not f.complete:
                    f.position,f.velocity=f.current(best)
                    f.time=best

            # FIRST: individual events
            for f,typ in single:

                if f.complete:
                    continue

                e=f._event()

                if e is not None and is_equal(
                    f.time+e[0],best
                ):
                    f._finish(best,typ)

            # SECOND: collisions
            # Recompute using only surviving flights.
            active=[
                f for f in self.flights.values()
                if not f.complete
            ]

            groups=[]

            for f in active:

                found=False

                for group in groups:

                    if is_equal(
                        f.position[0],
                        group[0].position[0]
                    ) and is_equal(
                        f.position[1],
                        group[0].position[1]
                    ) and is_equal(
                        f.position[2],
                        group[0].position[2]
                    ):
                        group.append(f)
                        found=True
                        break

                if not found:
                    groups.append([f])

            for group in groups:

                if len(group)>=2:
                    for f in group:
                        f.complete=True
                        f.finish="accident"

        self.time=target

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

        self._process(time)

        f=Flight(
            max_speed,
            position,
            velocity
        )

        f.time=time
        self.flights[flight_id]=f

        # Check collision immediately after creation
        self._process(time)

    def update(self,time,flight_id,acceleration):

        self._process(time)

        if flight_id not in self.flights:
            return

        self.flights[flight_id].set_acceleration(
            time,acceleration
        )

        # New acceleration can cause immediate event
        self._process(time)

    def status(self,time,flight_id):

        if flight_id not in self.flights:
            return "does not exist"

        self._process(time)

        f=self.flights[flight_id]

        return f.finish if f.complete else "flying"
