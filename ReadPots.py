from joy.plans import NBRPlan

class ReadPots():
    ##pass in shoulder, elbow, wrist position as get pos of those servos
    def __init__(self, shoulder_pos, elbow_pos, wrist_pos, *arg,**kw):        
        ##MOTOR INIT ANGLES
        self.SHOULDER_POS = shoulder_pos
        self.ELBOW_POS = elbow_pos
        self.WRIST_POS = wrist_pos

        self.max_pot = 1023

    def pot_to_degree(self, pot_val):
        # scale 0 - 255 to +-128
        dist = pot_val - self.max_pot/2

        #+-128 to +-135 degrees
        deg = (dist / (self.max_pot/2)) * 13500

        #saturation at 90 degrees
        if(deg < -9000):
            deg = -9000
        if(deg > 9000):
            deg = 9000
        return deg

if __name__=="__main__":
  app = ReadPots(0,0,0)
  app.run()
