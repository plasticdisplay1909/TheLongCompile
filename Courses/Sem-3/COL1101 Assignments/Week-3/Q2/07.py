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

def roots(a, b, c):
    if is_equal(a, 0):
        if is_equal(b, 0):
            return []
        return [-c/b]

    d = b*b-4*a*c
    if is_less(d, 0):
        return []

    d = max(0, d)**0.5
    
    # Numerically stable quadratic formula to prevent catastrophic cancellation
    if b > 0:
        r1 = (-b - d) / (2*a)
        r2 = (2*c) / (-b - d) if not is_equal(-b - d, 0) else 0
    elif b < 0:
        r1 = (2*c) / (-b + d) if not is_equal(-b + d, 0) else 0
        r2 = (-b + d) / (2*a)
    else:
        r1 = -d / (2*a)
        r2 = d / (2*a)

    return [r1, r2]

class Flight:

    def __init__(self, max_speed, position, velocity):
        self.max_speed = max_speed
        self.position = tuple(position)
        self.velocity = tuple(velocity)
        self.acceleration = (0,0,0)
        self.time = 0
        self.complete = False
        self.finish = None
        self.check_initial()

    def current(self, t):
        s = t-self.time
        p = tuple(
            self.position[i] +
            self.velocity[i]*s +
            .5*self.acceleration[i]*s*s
            for i in range(3)
        )
        v = tuple(
            self.velocity[i] + self.acceleration[i]*s
            for i in range(3)
        )
        return p,v

    def event(self):
        if self.complete:
            return None

        vx,vy,vz = self.velocity
        ax,ay,az = self.acceleration

        ev = []

        # speed^2 = max_speed^2
        A = ax*ax + ay*ay + az*az
        B = 2*(vx*ax + vy*ay + vz*az)
        C = vx*vx + vy*vy + vz*vz - self.max_speed**2

        if is_greater(C, 0):
            ev.append((0,"speed_accident"))
        else:
            r = roots(A,B,C)
            for t in r:
                if is_greater_equal(t,0):
                    d = 2*A*t+B
                    if is_greater_equal(d,0) and is_greater(A,0):
                        ev.append((max(0,t),"speed_accident"))
                    elif is_greater(d,0):
                        ev.append((max(0,t),"speed_accident"))

        # z = 0
        r = roots(.5*az,vz,self.position[2])
        for t in r:
            if not is_greater_equal(t,0):
                continue

            vz2 = vz+az*t
            if is_less(vz2,0):
                ev.append((t,"ground_accident"))
            elif is_equal(vz2,0) and is_less(az,0):
                ev.append((t,"ground_accident"))

        # Already safely landed
        if (
            is_equal(self.position[2],0)
            and all(is_equal(x,0) for x in self.velocity)
            and all(is_equal(x,0) for x in self.acceleration)
        ):
            ev.append((0,"landed safely"))

        if not ev:
            return None

        return min(ev,key=lambda x:x[0])

    def check_initial(self):
        speed2 = sum(x*x for x in self.velocity)

        if is_greater(speed2,self.max_speed**2):
            self.complete = True
            self.finish = "accident"
            return

        z = self.position[2]
        vz = self.velocity[2]

        if is_less(z,0):
            self.complete = True
            self.finish = "accident"
            return

        if is_equal(z,0):
            if is_less(vz,0):
                self.complete = True
                self.finish = "accident"
            elif (
                all(is_equal(x,0) for x in self.velocity)
                and all(is_equal(x,0) for x in self.acceleration)
            ):
                self.complete = True
                self.finish = "landed safely"

    def finish_at(self,t,typ):
        self.position,self.velocity = self.current(t)
        self.time = t
        self.complete = True
        self.finish = typ

    def set_acceleration(self,t,a):
        if self.complete:
            return

        self.position,self.velocity = self.current(t)
        self.time = t
        self.acceleration = tuple(a)
        self.check_initial()

    def status(self,t):
        if self.complete:
            return self.finish

        e = self.event()

        if e is not None:
            dt,typ = e

            if typ == "speed_accident":
                if is_less(self.time+dt,t):
                    self.finish_at(self.time+dt,"accident")
            elif typ == "ground_accident":
                if is_less_equal(self.time+dt,t):
                    self.finish_at(self.time+dt,"accident")
            elif is_less_equal(self.time+dt,t):
                self.finish_at(self.time+dt,typ)

        return self.finish if self.complete else "flying"

class AirTrafficControl:

    def __init__(self):
        self.flights = {}
        self.now = 0

    def collision(self,f1,f2):
        p1,v1 = f1.current(self.now)
        p2,v2 = f2.current(self.now)

        p = tuple(p1[i]-p2[i] for i in range(3))
        v = tuple(v1[i]-v2[i] for i in range(3))
        a = tuple(
            f1.acceleration[i]-f2.acceleration[i]
            for i in range(3)
        )

        eq = None

        for i in range(3):
            if not (
                is_equal(a[i],0)
                and is_equal(v[i],0)
                and is_equal(p[i],0)
            ):
                eq = (.5*a[i],v[i],p[i])
                break

        if eq is None:
            return self.now

        for t in roots(*eq):
            if not is_greater_equal(t,0):
                continue

            ok = True

            for i in range(3):
                x = (
                    .5*a[i]*t*t +
                    v[i]*t +
                    p[i]
                )
                if not is_equal(x,0):
                    ok = False
                    break

            if ok:
                return self.now+t

        return None

    def process(self,t):
        while True:
            best = None
            typ = None
            data = None

            # Single-flight events
            for f in self.flights.values():
                if f.complete:
                    continue

                e = f.event()
                if e is None:
                    continue

                dt,k = e
                et = self.now+dt

                # Distinguish strict bound for speed accident and inclusive for ground
                if k == "speed_accident":
                    if not is_less(et,t):
                        continue
                else:
                    if not is_less_equal(et,t):
                        continue

                if best is None or is_less(et,best):
                    best,typ,data = et,"single",(f,k)

            # Collisions
            fs = [f for f in self.flights.values() if not f.complete]

            for i in range(len(fs)):
                for j in range(i+1,len(fs)):
                    ct = self.collision(fs[i],fs[j])

                    if ct is None or not is_less_equal(ct,t):
                        continue

                    if best is None or is_less(ct,best):
                        best,typ,data = ct,"collision",(fs[i],fs[j])

            if best is None:
                break

            # Move everyone to event time
            for f in self.flights.values():
                if not f.complete:
                    f.position,f.velocity = f.current(best)
                    f.time = best

            if typ == "single":
                f,k = data

                if not f.complete:
                    f.complete = True
                    f.finish = "accident" if "accident" in k else k

            else:
                f1,f2 = data

                if not f1.complete and not f2.complete:
                    f1.complete = True
                    f1.finish = "accident"
                    f2.complete = True
                    f2.finish = "accident"

        # Advance surviving flights
        self.now = t

        for f in self.flights.values():
            if not f.complete:
                f.position,f.velocity = f.current(t)
                f.time = t

    def create(self,t,flight_id,max_speed,position,velocity):
        if flight_id in self.flights:
            return

        self.process(t)

        self.flights[flight_id] = Flight(
            max_speed,position,velocity
        )
        self.flights[flight_id].time = t

        # New flight can collide immediately
        self.process(t)

    def update(self,t,flight_id,acceleration):
        self.process(t)

        if flight_id not in self.flights:
            return

        self.flights[flight_id].set_acceleration(
            t,acceleration
        )

    def status(self,t,flight_id):
        if flight_id not in self.flights:
            return "does not exist"

        self.process(t)

        return self.flights[flight_id].finish \
            if self.flights[flight_id].complete \
            else "flying"
