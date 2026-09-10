import sys
import math

# =============================================================================
# Q10: Orbital Defense Grid (continuous-time kinematics + collision detection)
# =============================================================================
# A square arena centred on the origin, from -B to +B on both axes. Drones
# move in 2D under PIECEWISE-CONSTANT acceleration (exactly like your Air
# Traffic Control lab: a drone holds whatever acceleration it was last
# given, starting at (0,0), until told otherwise):
#     p(t) = p0 + v0(t - t0) + 0.5*a*(t - t0)^2
#     v(t) = v0 + a(t - t0)
#
# A drone is instantly and permanently destroyed (status becomes
# "accident" from that moment on, and it stops moving and can no longer
# be involved in any further event) the FIRST moment any of these three
# conditions holds -- checked CONTINUOUSLY, not just at instruction
# instants:
#   1. BOUNDARY BREACH: |x(t)| >= B or |y(t)| >= B (touching a wall
#      counts, not just crossing it).
#   2. OVERSPEED: its speed strictly exceeds its own max_speed.
#   3. COLLISION: its distance to some OTHER currently-surviving drone
#      becomes <= the sum of their two radii.
# Because two of these can become true at literally the same instant, and
# because a drone that has just been destroyed cannot be involved in
# ANY collision from that instant onward (dead drones are simply not
# there to hit), you must resolve events in strict chronological order:
# whenever several destructions are simultaneous, EVERY self-destruction
# (boundary breach or overspeed) at that instant is applied before ANY
# collision at that same instant is even considered, and a drone that
# has just self-destructed cannot be the "other" drone in a
# simultaneous collision. This is exactly the same precedence rule your
# ATC lab used ("apply the first two conditions and the landing rule
# before looking for collisions").
#
# Positions/velocities/accelerations are always given as (possibly
# fractional) numbers; use the supplied is_equal / is_less / etc.
# helpers (EPS = 1e-6) for every floating point comparison, exactly as
# in your ATC lab -- never write `x == y` or `x > y` directly on a
# computed float.
#
# THE HARD PART: unlike your ATC lab (a single quadratic per drone), the
# distance between TWO moving, accelerating drones is a QUARTIC
# (degree-4) polynomial in time -- there is no clean quadratic formula.
# You are expected to find the collision instant NUMERICALLY: scan the
# candidate time window in many small steps, and the moment you detect
# the squared-distance-minus-(R1+R2)^2 quantity has crossed from
# positive to non-positive between two consecutive samples, BISECT
# within that bracket to refine the crossing point to within EPS. (Do
# not attempt to solve the quartic in closed form.) You get a working
# quadratic-root helper below for the boundary/overspeed checks, which
# genuinely are quadratics in a single drone's own motion.
# =============================================================================

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


def quadratic_roots(a, b, c):
    """
    Given here: every REAL root of a*t^2 + b*t + c = 0 (as a plain list,
    possibly empty, possibly with 1 or 2 entries; correctly falls back to
    solving a linear equation if a is ~0). Use this inside
    boundary_breach_time and speed_violation_time below.
    """
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
        """
        max_speed, radius : floats
        position, velocity : (x, y) tuples of floats
        arena_half_width : float, the B of the square arena

        Set up self.px, self.py, self.vx, self.vy, self.ax = self.ay = 0.0
        (acceleration starts at zero), self.B, self.t0 = 0.0 (will be
        overwritten by Arena.create to the creation time), and
        self.finished = False.
        """
        # TODO: implement
        raise NotImplementedError

    def set_acceleration(self, t, accel):
        """
        Advance this drone's stored (px, py, vx, vy) to time t under its
        CURRENT (about-to-be-replaced) acceleration, set self.t0 = t,
        THEN install the new acceleration. (This is the same
        "advance-then-mutate" pattern as your ATC lab's Flight class.)
        """
        # TODO: implement
        raise NotImplementedError

    def _advance_to(self, t):
        """Helper used internally (including by Arena, when it finalises
        a drone at its exact destruction instant): move (px, py, vx, vy)
        forward to time t under the CURRENT acceleration, and set
        self.t0 = t. If t <= self.t0 already, do nothing."""
        # TODO: implement
        raise NotImplementedError

    def pos_at(self, dt):
        """Return (x, y) at dt time units after self.t0, under the
        CURRENT acceleration (does not mutate anything)."""
        # TODO: implement
        raise NotImplementedError

    def vel_at(self, dt):
        """Return (vx, vy) at dt time units after self.t0 (does not
        mutate anything)."""
        # TODO: implement
        raise NotImplementedError

    def speed_at(self, dt):
        """Return the scalar speed (magnitude of velocity) at dt time
        units after self.t0."""
        # TODO: implement
        raise NotImplementedError

    def boundary_breach_time(self):
        """
        Return the SMALLEST dt >= 0 (relative to self.t0) at which
        |x(t)| >= B or |y(t)| >= B, or None if this never happens.
        There are 4 relevant quadratic equations (x(t) = B, x(t) = -B,
        y(t) = B, y(t) = -B) -- collect every non-negative root from all
        four via quadratic_roots (don't forget dt = 0 itself as a
        candidate, in case the drone is created already touching a
        wall!), then, in ascending order, return the first candidate at
        which the drone is GENUINELY at or beyond the boundary (some
        roots are just the position touching a boundary line extended
        infinitely, without actually being the nearest edge -- always
        double check with the actual position, not just "a root
        exists").
        """
        # TODO: implement
        raise NotImplementedError

    def speed_violation_time(self):
        """
        Return the SMALLEST dt >= 0 at which speed(t) STRICTLY exceeds
        max_speed, or None. speed(t)^2 - max_speed^2 is a quadratic in
        t (expand |v0 + a*t|^2); collect its non-negative roots (plus
        dt = 0), and for each candidate, in ascending order, confirm
        that the drone is ACTUALLY over the limit an instant after that
        candidate (e.g. check at dt + 1e-4) before accepting it -- this
        correctly rejects a root where the speed merely touches the
        limit and falls back under it.
        """
        # TODO: implement
        raise NotImplementedError


class Arena:
    def __init__(self, half_width):
        """Store B = half_width and an empty dict of currently-known
        drones, keyed by id."""
        # TODO: implement
        raise NotImplementedError

    def create(self, t, did, max_speed, radius, position, velocity):
        """Create a new Drone with the given parameters, set its t0 = t,
        and register it under did."""
        # TODO: implement
        raise NotImplementedError

    def update(self, t, did, accel):
        """
        A no-op if did was never created. Otherwise: first resolve every
        event up to time t across the WHOLE arena (see
        _resolve_up_to below) -- an UPDATE instruction sent to a drone
        that turns out to have already met its end by time t must be
        silently ignored. If it's still flying, call its
        set_acceleration(t, accel).
        """
        # TODO: implement
        raise NotImplementedError

    def _self_destruct_time(self, d):
        """Return the smaller of d.boundary_breach_time() and
        d.speed_violation_time() (None if both are None), as a dt
        relative to d.t0."""
        # TODO: implement
        raise NotImplementedError

    def _collision_time(self, d1, d2, horizon_t):
        """
        Return the absolute time (not a dt!) at which d1 and d2 first
        collide, or None if that doesn't happen by horizon_t.

        d1 and d2 may have different t0's (different times they were
        last given an instruction) -- express their relative motion
        starting from t_start = max(d1.t0, d2.t0): compute each drone's
        position/velocity AT t_start (via pos_at/vel_at with the
        appropriate dt), and combine their (still constant, from here
        on, since neither will receive a new instruction before
        t_start... well, actually they might if you call this mid-
        resolution -- but for the window you're scanning, both
        accelerations are whatever they currently are) accelerations
        into a RELATIVE position/velocity/acceleration. Then scan dt in
        many small steps from 0 up to (horizon_t - t_start) [plus a
        little headroom], evaluating
            f(dt) = |relative_position(dt)|^2 - (r1+r2)^2
        and the first time f goes from positive to <= 0 between two
        consecutive samples, bisect within that bracket (~100
        iterations is plenty) to nail the crossing to within EPS. Return
        t_start + (that dt). If f(0) <= 0 already, they're already
        touching/overlapping -- return t_start immediately. Use a
        reasonably fine step count (a few hundred) so you don't skip
        over a brief, fast approach.
        """
        # TODO: implement
        raise NotImplementedError

    def _resolve_up_to(self, t):
        """
        The heart of the whole problem. Repeatedly find the single
        EARLIEST event (either some drone's self-destruction, or some
        pair's collision) that occurs at or before time t, among drones
        not yet finished, apply it (freeze the drone(s) involved: call
        their _advance_to(event_time) then set .finished = True), and
        repeat -- because finalising one drone can remove it from
        consideration for a collision that would otherwise have been
        "next". Stop when no more such events exist at or before t.

        Tie-breaking: if a self-destruction and a collision are tied at
        the same instant, the self-destruction must be applied FIRST
        (and, since it removes that drone from the pool, may cause a
        collision that seemed simultaneous to no longer be considered
        genuine -- recomputing from scratch after every single event, as
        described above, handles this naturally as long as you always
        pick the union of self-destructions and collisions and take the
        smallest, with self-destruction winning an exact tie).
        """
        # TODO: implement
        raise NotImplementedError

    def status(self, t, did):
        """
        Return "does not exist" if did was never created. Otherwise,
        resolve every event up to time t across the whole arena, then
        return "accident" if that drone is now finished, else "flying".
        """
        # TODO: implement
        raise NotImplementedError


# =============================================================================
# I/O driver -- given to you, do not modify.
# =============================================================================
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
