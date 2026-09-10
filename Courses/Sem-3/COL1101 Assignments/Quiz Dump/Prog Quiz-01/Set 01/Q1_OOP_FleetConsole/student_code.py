import sys

# =========================================================================
# Q1 : The Fleet Console  (Object-Oriented Programming)
# =========================================================================
#
# You are given the class SKELETONS below. Complete every method marked
# TODO, keeping the method names and signatures EXACTLY as given -- the
# I/O driver at the bottom of this file (which you must not modify) calls
# them by name.
#
# Read the accompanying question description carefully before you start:
# it fixes every rule (what ADD/RENT/SERVICE/REPORT/COMPARE/FLEET_TOTAL/TOP
# must do, how ids that don't exist are handled, how ties are broken,
# etc). This starter file intentionally does NOT restate those rules --
# treat the description as the spec, and this file as the place you
# implement it.
#
# You are free to add extra helper methods/attributes to any class below,
# and to add small private helper functions of your own, as long as the
# six public entry points (add, rent, service, report, compare,
# fleet_total, top) keep behaving exactly as specified when called by the
# driver.


class Vehicle:
    """Base class for anything the fleet can rent out."""

    def __init__(self, vid, rate):
        """
        vid  : str, the unique identifier of this vehicle.
        rate : float, the base per-day rental rate.

        A freshly created vehicle has zero revenue, zero days rented,
        zero completed rentals, and is not under maintenance.
        """
        # TODO: store vid, rate, and initialise every piece of state a
        # vehicle needs to track (revenue so far, total days rented,
        # number of completed rentals, whether it is under maintenance).
        raise NotImplementedError

    def type_name(self):
        """Return "VEHICLE" for the base class. Subclasses override this."""
        return "VEHICLE"

    def daily_cost(self, days):
        """
        Return the cost of renting THIS vehicle for `days` days, using
        whatever pricing rule applies to this particular kind of vehicle.
        The base class charges simply rate * days; subclasses may add
        surcharges (see the description for the exact truck surcharge).

        TODO: implement this for the base class.
        """
        raise NotImplementedError

    def rent(self, days):
        """
        Process a rental of `days` days for this vehicle: update revenue,
        days_rented and rental_count accordingly -- UNLESS the vehicle is
        currently under maintenance, in which case this call must have
        no effect at all.

        TODO: implement this.
        """
        raise NotImplementedError

    def set_service(self, status):
        """
        status is the string "START" or "END". Update this vehicle's
        maintenance flag accordingly. (Calling this repeatedly with the
        same status must be harmless -- it should simply leave the flag
        as that status.)

        TODO: implement this.
        """
        raise NotImplementedError

    def __str__(self):
        """
        Return the exact string:
            "<vid> [<TYPE>] revenue=<revenue> days=<days_rented> status=<STATUS>"
        where <revenue> is formatted with exactly two digits after the
        decimal point, <TYPE> is whatever type_name() returns, and
        <STATUS> is "MAINTENANCE" or "AVAILABLE".

        TODO: implement this.
        """
        raise NotImplementedError

    def __eq__(self, other):
        """
        Two vehicles are considered equal exactly when their revenues are
        equal (to floating point precision -- use a small epsilon such as
        1e-9 rather than comparing floats with ==).

        TODO: implement this.
        """
        raise NotImplementedError

    def __lt__(self, other):
        """
        A vehicle is "less than" another exactly when its revenue is
        (strictly) smaller. This ordering is what COMPARE and TOP must be
        built on top of -- do not compare .revenue fields directly
        anywhere else in your code; use <, >, == on Vehicle objects.

        TODO: implement this.
        """
        raise NotImplementedError

    def __gt__(self, other):
        """
        TODO: implement this in terms of __lt__ (do not duplicate the
        comparison logic).
        """
        raise NotImplementedError

    def __add__(self, other):
        """
        Vehicle + Vehicle -> the sum of their two revenues (a float).
        Vehicle + (int or float) -> this vehicle's revenue plus that
        number.
        Anything else -> return NotImplemented.

        TODO: implement this.
        """
        raise NotImplementedError

    def __radd__(self, other):
        """
        Handles (int or float) + Vehicle, e.g. what Python's built-in
        sum() does internally when it starts its accumulator at 0 and
        computes 0 + vehicles[0]. This is what makes
        sum(list_of_vehicles, 0.0) work.

        TODO: implement this.
        """
        raise NotImplementedError


class Car(Vehicle):
    """A car: no surcharge, just rate * days."""

    def type_name(self):
        return "CAR"

    # TODO: does Car need to override daily_cost, or does the base
    # class implementation already do the right thing for cars?
    # (Think before you write any code here -- you may not need to
    # add anything at all in this class body.)


class Truck(Vehicle):
    """
    A truck additionally carries cargo, and charges a per-day-per-ton
    surcharge of 5 on top of its base rate (see the description for the
    precise formula).
    """

    def __init__(self, vid, rate, cargo):
        """
        cargo : float, the truck's cargo capacity in tons.

        TODO: call the base class constructor appropriately, then store
        the cargo capacity.
        """
        raise NotImplementedError

    def type_name(self):
        return "TRUCK"

    def daily_cost(self, days):
        """
        TODO: implement the truck's pricing rule (base rate plus the
        per-ton-per-day surcharge), as specified in the description.
        """
        raise NotImplementedError


class FleetManager:
    """Owns every vehicle and answers every query about the fleet."""

    def __init__(self):
        # TODO: set up whatever storage you need for the fleet
        # (there is no rule anywhere that says you must use a dict --
        # but think about what data structure keeps every operation
        # below simple and correct).
        raise NotImplementedError

    def add(self, kind, vid, rate, cargo=None):
        """
        kind is "CAR" or "TRUCK". Create and register a new vehicle with
        this id UNLESS a vehicle with this id already exists, in which
        case this call has no effect (it is not an error).

        TODO: implement this.
        """
        raise NotImplementedError

    def rent(self, vid, days):
        """
        Look up the vehicle with this id and rent it out for the given
        number of days. An id that was never created, or that does not
        currently exist, is not an error -- it simply has no effect.

        TODO: implement this.
        """
        raise NotImplementedError

    def service(self, vid, status):
        """
        TODO: implement this (again, an unknown id has no effect).
        """
        raise NotImplementedError

    def report(self, vid):
        """
        Return the string form of the vehicle with this id (i.e. exactly
        what str(vehicle) would produce), or the literal string
        "NOT FOUND" if no such vehicle exists.

        TODO: implement this.
        """
        raise NotImplementedError

    def compare(self, id1, id2):
        """
        Return the id of whichever of the two vehicles has the strictly
        higher revenue, using the < and > operators on Vehicle objects
        (do not compare revenue numbers directly here). If either id does
        not exist, return "NOT FOUND". If the two vehicles have equal
        revenue, return "TIE".

        TODO: implement this.
        """
        raise NotImplementedError

    def fleet_total(self):
        """
        Return, as a string formatted to exactly two decimal places, the
        combined revenue of every vehicle in the fleet, computed using
        Python's built-in sum() over your vehicles (which will only work
        once __add__/__radd__ above are implemented correctly). If the
        fleet is empty, this must be "0.00".

        TODO: implement this.
        """
        raise NotImplementedError

    def top(self):
        """
        Return the id of the vehicle with the strictly highest revenue in
        the fleet, using comparisons between Vehicle objects (not raw
        revenue numbers). Break ties by returning the lexicographically
        smallest id among the tied vehicles. If the fleet is empty,
        return "NONE".

        TODO: implement this.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------
# I/O driver -- given to you, do not modify.
# ---------------------------------------------------------------------
def solve():
    data = sys.stdin.read().split("\n")
    idx = 0
    q = int(data[idx]); idx += 1
    fm = FleetManager()
    out = []
    for _ in range(q):
        parts = data[idx].split(); idx += 1
        cmd = parts[0]
        if cmd == "ADD":
            if parts[1] == "CAR":
                fm.add("CAR", parts[2], float(parts[3]))
            else:
                fm.add("TRUCK", parts[2], float(parts[3]), float(parts[4]))
        elif cmd == "RENT":
            fm.rent(parts[1], int(parts[2]))
        elif cmd == "SERVICE":
            fm.service(parts[1], parts[2])
        elif cmd == "REPORT":
            out.append(fm.report(parts[1]))
        elif cmd == "COMPARE":
            out.append(fm.compare(parts[1], parts[2]))
        elif cmd == "FLEET_TOTAL":
            out.append(fm.fleet_total())
        elif cmd == "TOP":
            out.append(fm.top())
    print("\n".join(out))


if __name__ == "__main__":
    solve()
