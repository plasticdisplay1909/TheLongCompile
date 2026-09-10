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
        
        self.max_speed= max_speed
        self.position=position
        self.velocity=velocity
        
        ## Zero initial
        self.acceleration=(0,0,0)
        self.time=0
        
        #Terminal condition
        self.complete=False
        self.finish=None

    "Return current state position and speed"
    def current(self,time):
        t= time- self.time
        
        ## Applying x_t =x_0 + v*t + 1/2 * a*t**2
        px=self.position[0] + self.velocity[0]*t + 0.5 * self.acceleration[0] *t*t
        py=self.position[1] + self.velocity[1]*t + 0.5 * self.acceleration[1] *t*t
        pz=self.position[2] + self.velocity[2]*t + 0.5 * self.acceleration[2] *t*t
    
    
        ## Flight creshes mid acceleration
        if (is_less (self.velocity[2] * self.acceleration[2] ,0)):
            t1= - (self.velocity[2] / self.acceleration[2])
            z= self.position[2] +self.velocity[2] * t1 + 0.5 *self.acceleration[2]*t*t
            
            if (is_less(z,0)):
                self.accident = 'accident'
                self.complete=True
                
        ## v_t =v_0 +a*t
        vx=self.velocity[0] + self.acceleration[0]*t
        vy=self.velocity[1] + self.acceleration[1]*t
        vz=self.velocity[2] + self.acceleration[2]*t
        
        return (px,py,pz),(vx,vy,vz)
        
        
    "Check if inital plane do not die"
    def initial(self):
        speed= (self.velocity[0]*self.velocity[0] + self.velocity[1]*self.velocity[1] + self.velocity[2]*self.velocity[2])
        
        if (is_greater(speed,self.max_speed)):
            self.finish = "accident"
            self.complete=True
            return
        
        # Crashes before taking off on ground
        # Why the fuck are you accelerating downward on ground and how is this happening
        if (is_equal(self.position[2],0)):
            if (is_less(self.velocity[2],0)):
                # How is this practically possible man
                self.finish='accident'
                self.complete=True
            
            ## Ok velocity is still considerable
            ## Like you are running and fell on ground
            ## So what is this case you fell standing what was pilot doing
            if (is_equal(self.velocity[2],0) and is_less(self.acceleration[2],0)):
                self.finish="accident"
                self.complete=True
    
    
    def set_acceleration(self, time, acceleration):
        """
        time : the instant from which the new acceleration applies
        acceleration : a tuple (ax, ay, az) of integers
        
        A flight that has already finished ignores this instruction.
        """
        if self.complete:   return
        
        self.position, self.velocity =self.current(time)
        self.time=time
        self.acceleration = acceleration
    

                
        
    def status(self, time):
        """
        Return this flight’s status at the given instant: "flying",
        "accident" or "landed safely".
        """
        ## Plane is already dead
        if self.finish is not None:
            return self.finish
        
        p,v=self.current(time)
        
        ## Plane crashed due to being so fast
        v1 = (v[0]*v[0] + v[1]*v[1] + v[2]*v[2])**0.5
        if (is_greater(v1,self.max_speed)):
            self.finish="accident"
            self.complete=True
            return "accident"
        
        if (is_less(p[2],0)):
            self.finish="accident"
            self.complete=True
            return "accident"
            
        if (is_equal(p[2],0)):
            if (is_less(v[2],0)):
                self.finish="accident"
                self.complete=True
                return "accident"
            
            elif (is_equal(v[2],0)) and is_less(self.acceleration[2],0):
                self.finish="accident"
                self.complete=True
                return "accident"
                
            elif (is_equal(v[2],0) and is_equal(self.acceleration[2],0)):
                self.finish="landed safely"
                self.complete=True
                return "landed safely"
            else:
                self.finish="flying"
                # self.complete=True
                return "flying"
        
        return "flying"
