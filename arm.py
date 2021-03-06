from selectors import EpollSelector
from turtle import position
from joy.decl import *
from joy import JoyApp, progress
from joy.plans import Plan
import ckbot
from ReadPots import *
import sys, os
from CalibrationMatrices import *
import numpy as np


class WritingPlan(Plan):
  def __init__(self, app, *arg,**kwargs):
    Plan.__init__(self,app)
    self.max_pot = app.readPots.max_pot
  
  def behavior(self):
    while(True):
      while app.nbr.ln:
        ts = app.nbr.ts.pop()
        ln = app.nbr.ln.pop()
        #progress("len: "+ str(len(ln)))
        if(len(ln) == 7):
          BASE_read = int(ln[0]) | (int(ln[1]) & 0xF) << 8
          ELBOW_read = int(ln[2]) | (int(ln[3]) & 0xF) << 8
          WRIST_read = int(ln[4]) | (int(ln[5]) & 0xF) << 8
          ##flip base direction
          app.readPots.SHOULDER_POS = app.readPots.pot_to_degree(int(BASE_read))
          app.readPots.ELBOW_POS = app.readPots.pot_to_degree(int(self.max_pot - ELBOW_read - (self.max_pot/2 - 150)))
          app.readPots.WRIST_POS = app.readPots.pot_to_degree(int(WRIST_read + (self.max_pot/2 - 860)))
          yield 0.01
          #progress(str(BASE_read))
          #progress(str(ELBOW_read))
          #progress(str(WRIST_read))
          #progress(str(app.readPots.SHOULDER_POS))
          #progress(str(app.readPots.ELBOW_POS))
          #progress(str(app.readPots.WRIST_POS))
          #progress("")
          #yield 1
        app.wrist.set_pos(app.readPots.WRIST_POS)
        yield 0.1
        app.elbow.set_pos(app.readPots.ELBOW_POS)
        yield 0.01
        app.shoulder.set_pos(app.readPots.SHOULDER_POS)
        yield 0.01
        

class recordingPlan(Plan):
    def __init__(self, app, *arg,**kwargs):
        Plan.__init__(self,app)
        self.recorded = []
    
    def behavior(self):
        while(True):
            currPos = (self.app.wrist.get_pos(), self.app.elbow.get_pos(), self.app.shoulder.get_pos())
            self.recorded.append(currPos)
            yield 0.25 # Take 4 samples per second

class calibrationPlayback(Plan):
  def __init__(self, app, *arg, **kwargs):
    Plan.__init__(self,app)
    self.center_x = 0
    self.center_y = 0
    self.scale = 4

    self.curr_x = 0
    self.curr_y = 0

  def behavior(self):
    app.calibrationP.construct_interpolation()
    yield 1

    self.adjust_target()
    yield 1

    '''
    progress("go to 0,0")
    self.curr_x = 0
    self.curr_y = 0
    yield self.set_motors()
    yield 10

    progress("go to max,0")
    self.curr_x = app.calibrationP.interpolated.shape[1] - 1
    self.curr_y = 0
    yield self.set_motors()
    yield 10

    progress("go to max,max")
    self.curr_x = app.calibrationP.interpolated.shape[1] - 1
    self.curr_y = app.calibrationP.interpolated.shape[0] -1
    yield self.set_motors()
    yield 10

    progress("go to 0,max")
    self.curr_x = 0
    self.curr_y = app.calibrationP.interpolated.shape[0] - 1
    yield self.set_motors()
    yield 10
    '''

    
    progress("go to initial")
    app.calibrationP.construct_interpolation()
    yield 1
    self.curr_x = self.center_x -self.scale - 2
    self.curr_y = self.center_y - self.scale
    yield self.set_motors()
    yield 5

    progress("move right")
    #top horizontal
    for i in range(0, 2*self.scale + 4):
      self.curr_x += 1
      yield self.set_motors()

    # progress("overshoot")
    # #overshoot
    # self.curr_x -= 1
    # self.curr_y -= 1
    # yield self.set_motors()
    # self.curr_x -= 1
    # self.curr_y -= 1
    # yield self.set_motors()

    progress("move down")
    #right vertical
    for i in range(0, 2*self.scale + 4):
      self.curr_y += 1
      yield self.set_motors()

    # progress("overshoot")
    # #overshoot
    # self.curr_x += 1
    # self.curr_y -= 1
    # yield self.set_motors()
    # self.curr_x += 1
    # self.curr_y -= 1
    # yield self.set_motors()
    
    progress("move left")
    #bottom horizontal
    for i in range(0, 2*self.scale + 4):
      self.curr_x -= 1
      yield self.set_motors()

    # progress("overshoot")
    # #overshoot
    # self.curr_x += 1
    # self.curr_y += 1
    # yield self.set_motors()
    # self.curr_x += 1
    # self.curr_y += 1
    # yield self.set_motors()

    progress("move up")
    #left vertical
    for i in range(0, 2*self.scale + 4):
      self.curr_y -= 1
      yield self.set_motors()

    # progress("overshoot")
    # #overshoot
    # self.curr_x -= 1
    # self.curr_y += 1
    # yield self.set_motors()
    # self.curr_x -= 1
    # self.curr_y += 1
    # yield self.set_motors()

    yield
    ##LINE
    # progress(str(app.calibrationP.interpolated.shape[1]))
    # for i in range(0, app.calibrationP.interpolated.shape[1]):
    #       progress(str(i))
    #       values = app.calibrationP.interpolated[0,i]
    #       self.app.wrist.set_pos(values[0])
    #       self.app.elbow.set_pos(values[1])
    #       self.app.shoulder.set_pos(values[2])
    #       yield 1
  
  def set_motors(self):
    values = app.calibrationP.interpolated[self.curr_y,self.curr_x]
    self.app.wrist.set_pos(values[0])
    self.app.elbow.set_pos(values[1])
    self.app.shoulder.set_pos(values[2])
    yield 1

  def adjust_target(self):
    if self.center_x - self.scale - 2 < 0:
      self.center_x -= self.center_x - self.scale - 2
      progress("Adjusted x target to: " + str(self.center_x))
    if self.center_x + self.scale + 2 > 20:
      self.center_x -= (self.center_x + self.scale + 2)-20
      progress("Adjusted x target to: " + str(self.center_x))
    if self.center_y - self.scale - 2 < 0:
      self.center_y -= self.center_y - self.scale - 2
      progress("Adjusted y target to: " + str(self.center_y))
    if self.center_y + self.scale + 2 > 24:
      self.center_y -= (self.center_y + self.scale + 2) -24
      progress("Adjusted y target to: " + str(self.center_y))






class playbackPlan(Plan):
  def __init__(self, app, *arg, **kwargs):
      Plan.__init__(self,app)
      self.finished = False
      self.wrist_offset = 0 # small offset for wrist to push the pen more into the paper
      pass

  def behavior(self):
    # If the length of "Hard" mode array is zero,
    # we have been recording in "Easy" mode
#    if(len(self.wrist_array) <= 0):
      
      # Do horizontal movement of arm first 
      for tuple in self.app.hline1:
          self.app.wrist.set_pos(tuple[0] + self.wrist_offset)
          self.app.elbow.set_pos(tuple[1])
          self.app.shoulder.set_pos(tuple[2])
          yield 1

      yield 1 # wait to reach first position

      for tuple in self.app.vline1:
          self.app.wrist.set_pos(tuple[0] + self.wrist_offset)
          self.app.elbow.set_pos(tuple[1])
          self.app.shoulder.set_pos(tuple[2])
          yield 1

      yield 1 # wait to reach second position

      for tuple in self.app.hline2:
          self.app.wrist.set_pos(tuple[0] + self.wrist_offset)
          self.app.elbow.set_pos(tuple[1])
          self.app.shoulder.set_pos(tuple[2])
          yield 1

      yield 1 # wait to reach third position

      for tuple in self.app.vline2:
          self.app.wrist.set_pos(tuple[0] + self.wrist_offset)
          self.app.elbow.set_pos(tuple[1])
          self.app.shoulder.set_pos(tuple[2])
          yield 1

      yield 1 # wait to reach fourth position

      for tuple in self.app.hline3:
          self.app.wrist.set_pos(tuple[0] + self.wrist_offset)
          self.app.elbow.set_pos(tuple[1])
          self.app.shoulder.set_pos(tuple[2])
          yield 1

      yield 1 # wait to reach fifth position

      for tuple in self.app.vline3:
          self.app.wrist.set_pos(tuple[0] + self.wrist_offset)
          self.app.elbow.set_pos(tuple[1])
          self.app.shoulder.set_pos(tuple[2])
          yield 1

      yield 1 # wait to reach final position
      self.finished = True

if 'pyckbot/hrb/' not in sys.path:
    sys.path.append(os.path.expanduser('~/pyckbot/hrb/'))

class ControllerApp( JoyApp ):
  """Concrete class RobotSimulatorApp <<singleton>>
     A JoyApp which runs the DummyRobotSim robot model in simulation, and
     emits regular simulated tagStreamer message to the desired waypoint host.

  """
  def __init__(self, *arg,**kw):
      """
      Initialize the simulator
      """
      JoyApp.__init__( self,
        confPath="$/cfg/JoyApp.yml", *arg, **kw)
      # ADD pre-startup initialization here, if you need it
      self.readPots = None
      c = ckbot.logical.Cluster(count=3, names={
        0x97:"WRIST",
        0x10:"ELBOW",
        0x0A:"SHOULDER"
      })

      self.wrist = c.at.WRIST
      self.elbow = c.at.ELBOW
      self.shoulder = c.at.SHOULDER

      # Arrays to store miscellanous movement of robot arm
      self.wrist_array = []
      self.elbow_array = []
      self.shoulder_array = []
      
      # Lists to store movement tuples
      self.hline1 = []
      self.hline2 = []
      self.hline3 = []
      self.vline1 = []
      self.vline2 = []
      self.vline3 = []

      # Flags for recording each hor./ver. line
      self.record = False
      self.recordhline1 = False
      self.recordhline2 = False
      self.recordhline3 = False
      self.recordvline1 = False
      self.recordvline2 = False
      self.recordvline3 = False

      self.setup_time_completed = False
      self.manual_mode = False
      self.measure_index = 0

  def onStart( self ):
    """
    Sets up the JoyApp
    """

    # Set mode to 0 to use set_pos function
    self.wrist.set_mode(0)
    self.elbow.set_mode(0)
    self.shoulder.set_mode(2)
    
    # Set speeds of all motors
    self.wrist.set_speed(0.5)
    self.elbow.set_speed(0.5)
    self.shoulder.set_speed(0.5)
    
    # Set-up recording & playback plans
    # Need to pass in vector to recording plan to retrieve position data
    self.recordP = recordingPlan(self)
    self.playP = playbackPlan(self)
    self.readPots = ReadPots(shoulder_pos = self.shoulder.get_pos(), elbow_pos = self.elbow.get_pos(), wrist_pos = self.wrist.get_pos())

    self.writingP = WritingPlan(self)
    self.calibrationP = CalibrationMatrices(self)
    self.calPlaybackP = calibrationPlayback(self)

    self.nbr = NBRPlan(self,fn="/dev/ttyACM0")
    self.nbr.start()

  def stop_all_plans(self):
    yield

  def onEvent( self, evt ):
    
    w = self.wrist.set_pos
    e = self.elbow.set_pos
    s = self.shoulder.set_pos
    lw = self.wrist.get_pos
    le = self.elbow.get_pos
    ls = self.shoulder.get_pos
    
    #progress(str(self.manual_mode))
    
    if evt.type == KEYDOWN:
      if evt.key == K_a:
        w(lw() + 200) # 1000 = 10 degree increment
        progress("Wrist Up, increment w")
      elif evt.key == K_z:
        w(lw() - 200) # -1000 = 10 degree decrement
        progress("Wrist Down, decrement w")
      elif evt.key == K_s:
        e(le() + 300)
        progress("Shoulder Up, increment e")
      elif evt.key == K_x:
        e(le() - 300)
        progress("Shoulder Down, decrement e")
      elif evt.key == K_d:
        s(ls() + 200)
        progress("Turn Right, increment s")
      elif evt.key == K_c:
        s(ls() - 200)
        progress("Turn Left, decrement s")
        
      # "Easy" Mode Recordings
      # "Easy" Mode Recordings
      elif evt.key == K_w:
          self.recordhline1 = not self.recordhline1
          if(self.recordhline1):
              progress("Recording Horizontal line 1!")
              self.recordP.start()
          else:
              self.hline1 = self.recordP.recorded
              progress("Horizontal line 1 has finished recording!")
              self.recordP.stop()
              
      elif evt.key == K_e:
          self.recordvline1 = not self.recordvline1
          if(self.recordvline1):
              progress("Recording Vertical line 1!")
              self.recordP.start()
          else:
              self.vline1 = self.recordP.recorded
              progress("Vertical line 1 has finished recording!")
              self.recordP.stop()
              
      elif evt.key == K_r:
          self.recordhline2 = not self.recordhline2
          if(self.recordhline2):
              progress("Recording Horizontal line 2!")
              self.recordP.start()
          else:
              self.hline2 = self.recordP.recorded
              progress("Horizontal line 2 has finished recording!")
              self.recordP.stop()
              
      elif evt.key == K_t:
          self.recordvline2 = not self.recordvline2
          if(self.recordvline2):
              progress("Recording Vertical line 2!")
              self.recordP.start()
          else:
              self.vline2 = self.recordP.recorded
              progress("Vertical line 2 has finished recording!")
              self.recordP.stop()

      elif evt.key == K_y:
          self.recordhline3 = not self.recordhline3
          if(self.recordhline3):
              progress("Recording Horizontal line 3!")
              self.recordP.start()
          else:
              self.hline3 = self.recordP.recorded
              progress("Horizontal line 3 has finished recording!")
              self.recordP.stop()

      elif evt.key == K_u:
          self.recordvline3 = not self.recordvline3
          if(self.recordvline3):
              progress("Recording Vertical line 3!")
              self.recordP.start()
          else:
              self.vline3 = self.recordP.recorded
              progress("Vertical line 3 has finished recording!")
              self.recordP.stop()
              
      # Stop all recordings
      elif evt.key == K_q:
          self.hline1.clear()
          self.hline2.clear()
          self.hline3.clear()
          self.vline1.clear()
          self.vline2.clear()
          self.vline3.clear()
          progress("Cleared all recorded vectors")
          progress("Proof: " + "HLine1 = " + str(self.hline1) + ", VLine3 = " + str(self.vline3))
          
      elif evt.key == K_i and not self.playP.isRunning():
        self.playP.start()
        if(self.playP.finished):
            progress("Killing the Playback!")
            self.playP.stop()
            self.playP.finish = False
            
      elif evt.key == K_p:
        currPos = (self.wrist.get_pos(), self.elbow.get_pos(), self.shoulder.get_pos())
        progress("(Wrist_pos, Elbow_pos, Shoulder_pos) = " +  str(currPos))
      
      elif evt.key == K_o:
          progress("Printing out recorded vectors")
          progress("Horizontal Line 1: " + str(self.hline1))
          progress("Vertical Line 1: " + str(self.vline1))
          progress("Horizontal Line 2: " + str(self.hline2))
          progress("Vertical Line 2: " + str(self.vline2))
          progress("Horizontal Line 3: " + str(self.hline3))
          progress("Vertical Line 3: " + str(self.vline3))
        
      elif evt.key == K_m:
        #progress("MMMMMMMMMMMMMMMMMMMMMMMMMMMMMM")
        self.manual_mode = not self.manual_mode
        if self.manual_mode:
          self.wrist.set_speed(4)
          self.elbow.set_speed(2)
          self.shoulder.set_speed(2)
          self.writingP.start()
        else:
          self.wrist.set_speed(0.5)
          self.elbow.set_speed(0.5)
          self.shoulder.set_speed(0.5)
          self.writingP.stop()

      elif evt.key == K_n:
        r = None
        c = None
        if self.measure_index == self.calibrationP.NUM_X * self.calibrationP.NUM_Y:
          progress("DONE MEASURING")
        else:
          if self.calibrationP.is_hamburger_style:
            r = self.measure_index // self.calibrationP.NUM_X
            c = self.measure_index % self.calibrationP.NUM_X
          else:
            r = self.measure_index // self.calibrationP.NUM_Y
            c = self.measure_index % self.calibrationP.NUM_Y
          progress("Measured at [" + str(r) + "," 
            + str(c) +"]")
          currPos = (self.wrist.get_pos(), self.elbow.get_pos(), self.shoulder.get_pos())
          self.calibrationP.measured[r,c] = currPos
          self.measure_index += 1
          progress(self.calibrationP.measured)
      
      elif evt.key == K_b:
        self.calPlaybackP.start()
      
      elif evt.key == K_g:
        np.save("calibration", self.calibrationP.measured)

      elif evt.key == K_h:
        self.calibrationP.measured = np.load("calibration.npy")

      elif evt.key == K_v:
        self.wrist.set_mode(1)
        self.wrist.go_slack()
        self.elbow.set_mode(1)
        self.elbow.go_slack()
        self.shoulder.set_mode(1)
        self.shoulder.go_slack()
      
      elif evt.key == K_f:
        self.wrist.set_mode(0)
        self.elbow.set_mode(0)
        self.shoulder.set_mode(2)

      
    ### DO NOT MODIFY -----------------------------------------------
    else:# Use superclass to show any other events
        return JoyApp.onEvent(self,evt)
    return # ignoring non-KEYDOWN events


if __name__=="__main__":
    motorNames = {0x97:"WRIST",
                0x10:"ELBOW",
                0x0A:"SHOULDER"}
    robot = {'count':3, 'names': motorNames}
    app = ControllerApp()
    app.run()