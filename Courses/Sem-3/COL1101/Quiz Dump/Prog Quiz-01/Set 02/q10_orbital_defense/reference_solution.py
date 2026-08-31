import sys
import math

EPS = 1e-6


def is_equal(x, y):
    return abs(x - y) <= EPS


def is_less(x, y):
    return x < y - EPS


def is_greater(x, y):
    return x > y + EPS


def is_less_equal(x, y):
    return not is_greater(x, y)


def is_greater_equal(x, y):
    return not is_less(x, y)


def _quadratic_roots(a, b, c):
    """All real roots of a*t^2 + b*t + c = 0 (handles a==0 as linear)."""
    if is_equal(a, 0):
        if is_equal(b, 0):
            return []
        return [-c / b]
    disc = b * b - 4 * a * c
    if disc < -1e-9:
        return []
    disc = max(disc, 0.0)
    sq = math.sqrt(disc)
    return [(-b - sq) / (2 * a), (-b + sq) / (2 * a)]


class Drone:
    def __init__(self, max_speed, radius, position, velocity, arena_half_width):
        self.max_speed = max_speed
        self.radius = radius
        self.px, self.py = position
        self.vx, self.vy = velocity
        self.ax, self.ay = 0.0, 0.0
        self.B = arena_half_width
        self.t0 = 0.0
        self.finished = False

    def set_acceleration(self, t, accel):
        self._advance_to(t)
        self.ax, self.ay = accel

    def _advance_to(self, t):
        dt = t - self.t0
        if dt > 0:
            self.px += self.vx * dt + 0.5 * self.ax * dt * dt
            self.py += self.vy * dt + 0.5 * self.ay * dt * dt
            self.vx += self.ax * dt
            self.vy += self.ay * dt
        self.t0 = t

    def pos_at(self, dt):
        return (self.px + self.vx * dt + 0.5 * self.ax * dt * dt,
                self.py + self.vy * dt + 0.5 * self.ay * dt * dt)

    def vel_at(self, dt):
        return (self.vx + self.ax * dt, self.vy + self.ay * dt)

    def speed_at(self, dt):
        vx, vy = self.vel_at(dt)
        return math.sqrt(vx * vx + vy * vy)

    def boundary_breach_time(self):
        """Smallest dt >= 0 at which |x(t)| >= B or |y(t)| >= B (touching
        the wall counts as a breach), or None if it never happens."""
        roots = {0.0}
        for (p0, v0, a0) in [(self.px, self.vx, self.ax), (self.py, self.vy, self.ay)]:
            for target in (self.B, -self.B):
                for r in _quadratic_roots(0.5 * a0, v0, p0 - target):
                    if r >= -EPS:
                        roots.add(round(max(r, 0.0), 9))
        for r in sorted(roots):
            x, y = self.pos_at(r)
            if is_greater_equal(abs(x), self.B) or is_greater_equal(abs(y), self.B):
                return r
        return None

    def speed_violation_time(self):
        """Smallest dt >= 0 at which speed(t) STRICTLY exceeds max_speed,
        else None. speed(t)^2 - max_speed^2 is a quadratic in t; we take
        every non-negative root (plus dt=0 itself) and, for each (in
        ascending order), confirm the drone is genuinely in violation an
        instant after that root before accepting it (this correctly
        discards a root where the drone merely grazes the limit and
        falls back under it)."""
        A = self.ax * self.ax + self.ay * self.ay
        Bc = 2 * (self.vx * self.ax + self.vy * self.ay)
        C = self.vx * self.vx + self.vy * self.vy - self.max_speed * self.max_speed
        roots = sorted({0.0} | {max(r, 0.0) for r in _quadratic_roots(A, Bc, C) if r >= -EPS})
        for r in roots:
            if is_greater(self.speed_at(r + 1e-4), self.max_speed):
                return r
        return None


class Arena:
    def __init__(self, half_width):
        self.B = half_width
        self.drones = {}

    def create(self, t, did, max_speed, radius, position, velocity):
        d = Drone(max_speed, radius, position, velocity, self.B)
        d.t0 = t
        self.drones[did] = d

    def update(self, t, did, accel):
        d = self.drones.get(did)
        if d is None or d.finished:
            return
        self._resolve_up_to(t)
        if d.finished:
            return
        d.set_acceleration(t, accel)

    def _self_destruct_time(self, d):
        bt = d.boundary_breach_time()
        st = d.speed_violation_time()
        cands = [x for x in (bt, st) if x is not None]
        return min(cands) if cands else None

    def _collision_time(self, d1, d2, horizon_t):
        t_start = max(d1.t0, d2.t0)
        if t_start > horizon_t + EPS:
            return None
        dt1 = t_start - d1.t0
        dt2 = t_start - d2.t0
        x1, y1 = d1.pos_at(dt1)
        x2, y2 = d2.pos_at(dt2)
        vx1, vy1 = d1.vel_at(dt1)
        vx2, vy2 = d2.vel_at(dt2)
        px, py = x1 - x2, y1 - y2
        vx, vy = vx1 - vx2, vy1 - vy2
        ax, ay = d1.ax - d2.ax, d1.ay - d2.ay
        R = d1.radius + d2.radius

        s_max = max(horizon_t - t_start, 0.0) + 1.0

        def f(s):
            rx = px + vx * s + 0.5 * ax * s * s
            ry = py + vy * s + 0.5 * ay * s * s
            return rx * rx + ry * ry - R * R

        if f(0.0) <= 1e-9:
            return t_start

        N = 600
        prev_s, prev_v = 0.0, f(0.0)
        for k in range(1, N + 1):
            s = s_max * k / N
            v = f(s)
            if v <= 1e-9:
                lo, hi = prev_s, s
                for _ in range(100):
                    mid = (lo + hi) / 2
                    if f(mid) > 0:
                        lo = mid
                    else:
                        hi = mid
                return t_start + hi
            prev_s, prev_v = s, v
        return None

    def _resolve_up_to(self, t):
        """Freeze (finalize) any drone whose self-destruction or
        collision event time is <= t, processing events in chronological
        order, self-destruction before collision whenever they tie at
        the same instant, until no more events occur at or before t."""
        while True:
            best_time = None
            best_kind = None  # "self" or ("collide", other_id)
            best_id = None
            for did, d in self.drones.items():
                if d.finished or d.t0 > t + EPS:
                    continue
                st = self._self_destruct_time(d)
                if st is not None:
                    et = d.t0 + st
                    if et <= t + EPS and (best_time is None or et < best_time - EPS):
                        best_time, best_kind, best_id = et, "self", did
            if best_time is None:
                for id1, d1 in self.drones.items():
                    if d1.finished:
                        continue
                    for id2, d2 in self.drones.items():
                        if id2 <= id1 or d2.finished:
                            continue
                        ct = self._collision_time(d1, d2, t)
                        if ct is not None and ct <= t + EPS:
                            if best_time is None or ct < best_time - EPS:
                                best_time, best_kind, best_id = ct, ("collide", id1, id2), None
            if best_time is None:
                return
            if best_kind == "self":
                d = self.drones[best_id]
                d._advance_to(best_time)
                d.finished = True
            else:
                _, id1, id2 = best_kind
                d1, d2 = self.drones[id1], self.drones[id2]
                d1._advance_to(best_time)
                d2._advance_to(best_time)
                d1.finished = True
                d2.finished = True

    def status(self, t, did):
        if did not in self.drones:
            return "does not exist"
        self._resolve_up_to(t)
        d = self.drones[did]
        return "accident" if d.finished else "flying"


def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    B = float(data[idx]); idx += 1
    q = int(data[idx]); idx += 1
    arena = Arena(B)
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "CREATE":
            _, t, did, ms, rad, x, y, vx, vy = parts
            arena.create(float(t), did, float(ms), float(rad), (float(x), float(y)), (float(vx), float(vy)))
        elif cmd == "UPDATE":
            _, t, did, ax, ay = parts
            arena.update(float(t), did, (float(ax), float(ay)))
        elif cmd == "STATUS":
            _, t, did = parts
            out.append(arena.status(float(t), did))
        else:
            raise ValueError(cmd)
    print("\n".join(out))


if __name__ == "__main__":
    solve()
