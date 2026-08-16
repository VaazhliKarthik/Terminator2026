# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       rahul                                                        #
# 	Created:      8/16/2026, 4:47:38 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #




#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
Front_Right = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
controller_1 = Controller(PRIMARY)
Front_Left = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
center = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)
Back_Left = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
Back_Right = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
intake_top2 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
intake_mid3 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
intake_low4 = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
gate5 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
sweeper_arm6 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
gate_sensor8 = Rotation(Ports.PORT8, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

screen_precision = 0
console_precision = 0
controller_1_precision = 0
gate_state_list = [0 for x in range(4)]
is_intake_spinning = False
is_gate_open = False
is_scooper_down = False
is_dir_backward = False
my_event = Event()
gate_position = 0
move_cntr = 0
cur_speed = 0

def vector_drive_ip_fwd_ip_turn(vector_drive_ip_fwd_ip_turn__ip_fwd, vector_drive_ip_fwd_ip_turn__ip_turn):
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    global is_dir_backward
    global cur_speed

    MAX_STEP = 5

    TURN_SCALE = 0.7
    turn_ = vector_drive_ip_fwd_ip_turn__ip_turn #controller_1.axis4.position()
    turn1 = int(turn_ * TURN_SCALE)

    fwd_ = vector_drive_ip_fwd_ip_turn__ip_fwd #controller_1.axis2.position()

    #for deadband - if deadband is enabled. will not be able to stop
    #fwd_ = 0 if abs(fwd_) < 5 else fwd_

    #more sentivity
    fwd_final = (fwd_ ** 2 / 100 ) * (-1 if fwd_ > 0 else 1)
    #preserving turn direction
    turn_final = (turn1 **2 / 100 ) * (-1 if turn1 > 0 else 1)


    if fwd_final > cur_speed:
        cur_speed += min(MAX_STEP, fwd_final - cur_speed)
    elif fwd_final < cur_speed:
        cur_speed -= min(MAX_STEP, cur_speed - fwd_final)
    fwd_final = cur_speed


    # Differential drive mixing
    left_speed = fwd_final + turn_final
    right_speed = fwd_final - turn_final

    # Normalize (preserve vector direction)
    max_mag = max(abs(left_speed), abs(right_speed))
    if max_mag > 100:
        left_speed  = left_speed  * 100 / max_mag
        right_speed = right_speed * 100 / max_mag

    if fwd_final > 0:
        is_dir_backward = True
        #controller_1.screen.next_row()
        #controller_1.screen.print(fwd_final,",",turn_final,", b: ","True")
    else: #current direction is forward
        if is_dir_backward: #Earlier it was moving backward
            wait(800,MSEC)  #to prevent topple
            controller_1.screen.next_row()
            controller_1.screen.print(fwd_final,",",turn_final,", b: ","False")
        is_dir_backward = False

    #controller_1.screen.next_row()
    #controller_1.screen.print(fwd_final,",",turn_final,", b: ",is_dir_backward)

    #filename = "/usd/robot_log.csv"
    #brain.sdcard.appendfile(filename, right_speed+"\n")

    if turn_ == 0 and fwd_ == 0 :
        Front_Right.stop()
        Front_Left.stop()
        Back_Left.stop()
        Back_Right.stop()
        return

    #controller_1.screen.next_row()
    #controller_1.screen.print(left_speed,",",right_speed)

    Front_Left.set_velocity(left_speed, PERCENT)
    Front_Right.set_velocity(right_speed, PERCENT)
    Back_Left.set_velocity(left_speed, PERCENT)
    Back_Right.set_velocity(right_speed, PERCENT)
    Back_Left.spin(FORWARD)
    Back_Right.spin(FORWARD)
    Front_Right.spin(FORWARD)
    Front_Left.spin(FORWARD)

def reverse_intake_start():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    is_intake_spinning = True
    intake_top2.set_velocity(100,PERCENT)
    intake_mid3.set_velocity(100,PERCENT)
    intake_low4.set_velocity(100,PERCENT)
    intake_top2.spin(FORWARD)
    intake_mid3.spin(FORWARD)
    intake_low4.spin(FORWARD)

def forward_Intake_start():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    is_intake_spinning = True
    intake_top2.set_velocity(100,PERCENT)
    intake_mid3.set_velocity(100,PERCENT)
    intake_low4.set_velocity(100,PERCENT)
    intake_top2.spin(REVERSE)
    intake_mid3.spin(REVERSE)
    intake_low4.spin(REVERSE)

def stop_intake():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    intake_top2.stop()
    intake_mid3.stop()
    intake_low4.stop()
    is_intake_spinning = False

def onauton_autonomous_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    gate_position = 0
    is_intake_spinning = False
    is_gate_open = True
    is_scooper_down = False
    is_dir_backwards = False
    Front_Left.set_velocity(30,PERCENT)
    Front_Right.set_velocity(30,PERCENT)
    Back_Left.set_velocity(30,PERCENT)
    Back_Right.set_velocity(30,PERCENT)
    gate5.set_stopping(HOLD)
    side = "LEFT"

    if side == "LEFT":
        first_move_dir = REVERSE
        second_move_angle = "CLOCKWISE"
        third_move_dir = REVERSE
        fourth_move_dir = FORWARD
        fifth_move_dir = REVERSE
        sixth_move_angle = "COUNTER_CLOCKWISE"
        seventh_move_dir = REVERSE
    if side == "RIGHT":
        first_move_dir = REVERSE
        second_move_angle = "COUNTER_CLOCKWISE"
        third_move_dir = REVERSE
        fourth_move_dir = FORWARD
        fifth_move_dir = REVERSE
        sixth_move_angle = "CLOCKWISE"
        seventh_move_dir = REVERSE


    def drive_straight(direction=FORWARD, dist=5, units=TURNS  ):
        Front_Right.spin_for(direction,dist,TURNS,wait=False)
        Front_Left.spin_for(direction,dist,TURNS,wait=False)
        Back_Left.spin_for(direction,dist,TURNS,wait=False)
        Back_Right.spin_for(direction,dist,TURNS,wait=True)
        wait(20,MSEC)
        return

    def turn_angle(direction="CLOCKWISE", ang=240, units=DEGREES ):
        if direction == "CLOCKWISE":
            Front_Right.spin_for(REVERSE,ang,units,wait=False)
            Front_Left.spin_for(FORWARD,ang,units,wait=False)
            Back_Left.spin_for(FORWARD,ang,units,wait=False)
            Back_Right.spin_for(REVERSE,ang,units,wait=True)
            wait(20,MSEC)

        if direction == "COUNTER_CLOCKWISE":
            Front_Right.spin_for(FORWARD,ang,units,wait=False)
            Front_Left.spin_for(REVERSE,ang,units,wait=False)
            Back_Left.spin_for(REVERSE,ang,units,wait=False)
            Back_Right.spin_for(FORWARD,ang,units,wait=True)
            wait(20,MSEC)
            return

    def control_gate5(state="OPEN"):
        if state == "OPEN":
            gate5.set_velocity(40,PERCENT)
            gate5.spin_for(FORWARD,255,DEGREES,wait=True)
        if state == "CLOSE":
            gate5.set_velocity(40,PERCENT)
            gate5.spin_for(REVERSE,255,DEGREES,wait=True)

    def set_sweeper(state="OPEN"):
        sweeper_arm6.set_max_torque(100,PERCENT)
        sweeper_arm6.set_velocity(30,PERCENT)
        if state == "OPEN":
            sweeper_arm6.spin_for(REVERSE,200,DEGREES,wait=True)
        if state == "CLOSE":
            sweeper_arm6.spin_for(FORWARD,195,DEGREES,wait=True)

    set_sweeper("OPEN")
    forward_Intake_start()
    ###############################################
    #move one tile forward
    drive_straight(first_move_dir, 2.7, TURNS)

    ###############################################
    #Turn around 90 degrees
    turn_angle(second_move_angle, 250, DEGREES)


    ###############################################
    #start pulling the balls
    #forward_Intake_start()

    ###############################################
    #move one tile forward at 30%
    drive_straight(third_move_dir, .9, TURNS)
    for i in range(4):
        drive_straight(FORWARD, .15, TURNS)
        drive_straight(REVERSE, .15, TURNS)


    wait(2,SECONDS)

    stop_intake()
    control_gate5("OPEN")

    drive_straight(fourth_move_dir, 2, TURNS)
    forward_Intake_start()
    wait(2,SECONDS)

    ###############################################
    drive_straight(fifth_move_dir, 1, TURNS)
    set_sweeper("CLOSE")


    ###############################################
    #move one tile backward at 30%
    turn_angle(sixth_move_angle, 250, DEGREES)

    drive_straight(seventh_move_dir, 3, TURNS)




    ###############################################
    #move one tile backward at 30%
    # back to parking lot
    #drive_straight( fifth_move_dir, 5, TURNS)


    ###############################################
    #move one tile forward at 30%
    #drive_straight(FORWARD, 5, TURNS)


def ondriver_drivercontrol_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    cur_speed = 0
    gate_position = 0
    is_intake_spinning = False
    is_gate_open = True
    is_scooper_down = False
    is_dir_backward = False
    Front_Left.set_velocity(100,PERCENT)
    Front_Right.set_velocity(100,PERCENT)
    Back_Left.set_velocity(100,PERCENT)
    Back_Right.set_velocity(100,PERCENT)

    gate5.set_stopping(HOLD)
    sweeper_arm6.set_stopping(HOLD)

    controller_1.screen.clear_screen()
    controller_1.screen.set_cursor(1,1)

def controller_1buttonX_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    brain.program_stop()

def ondriver_drivercontrol_1():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    move_cntr = 0
    while True:
        vector_drive_ip_fwd_ip_turn(controller_1.axis2.position(), controller_1.axis4.position())
        #controller_1.screen.next_row()
        #controller_1.screen.print(move_cntr , "joy: ",\
        # controller_1.axis2.position(),",",controller_1.axis4.position())
        move_cntr = (move_cntr + 1) % 1000
        wait(5, MSEC)

def when_started1():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    pass

def controller_1buttonA_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    if is_intake_spinning:
        stop_intake()
    else:
        forward_Intake_start()

def controller_1buttonB_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    if is_intake_spinning:
        stop_intake
    else:
        reverse_intake_start

def controller_1buttonLeft_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    gate5.set_velocity(50,PERCENT)
    gate5.set_max_torque(100,PERCENT)
    gate5.spin_for(FORWARD, 20,DEGREES,wait=False)
    gate5.set_stopping(HOLD)
    brain.screen.set_pen_color(Color.BLACK)
    print("gate angle :")
    print(gate_sensor8.angle())

def controller_1buttonRight_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    gate5.set_velocity(50,PERCENT)
    gate5.set_max_torque(100,PERCENT)
    gate5.spin_for(REVERSE,20,DEGREES,wait=False)
    gate5.set_stopping(HOLD)
    brain.screen.set_pen_color(Color.GREEN)
    print("gate angle :")
    print(gate_sensor8.angle())

# Used to find the format string for printing numbers with the
# desired number of decimal places
def console_format(variable):
    # If the input is a string, return it as is
    if isinstance(variable, str):
        return variable
    # Otherwise, apply precision logic for numbers
    precision = 0
    # Equivalent to setting precision to 'All Digits'
    if console_precision is None:
        precision = 6
    else:
        precision = console_precision
    return "{0:.{1}f}".format(variable, precision)

def controller_1buttonL1_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    gate_at = gate_sensor8.angle()
    print("\033[30m")
    print(console_format("L1 gate angle:"), end="")
    print(console_format(gate_sensor8.angle()), end="")
    if (gate_at > 80) and (gate_at < 120):
        gate5.set_velocity(40,PERCENT)
        gate5.spin_for(FORWARD,255,DEGREES,wait=True)
        #gate5.set_stopping(HOLD)
        print("L1 Final pos: ",gate_sensor8.angle())
    elif (gate_at > 320) and (gate_at < 365):
        gate5.set_velocity(40,PERCENT)
        gate5.spin_for(REVERSE,255,DEGREES,wait=True)
        #gate5.set_stopping(HOLD)
        print("L1 Final pos: ",gate_sensor8.angle())
    else:
        print(console_format("L1 gate angle No Action:"), end="")
        print(console_format(gate_sensor8.angle()), end="")

def controller_1buttonL2_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    gate5.set_velocity(100,PERCENT)
    gate5.spin_for(REVERSE, 40,DEGREES,wait=False)
    gate5.set_stopping(HOLD)
    brain.screen.set_pen_color(Color.GREEN)
    print("L2 gate angle :")
    print(gate_sensor8.angle())

def controller_1buttonUp_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    if is_scooper_down:
        print("\033[35m")
        console_precision = 1
        print("motor current",sweeper_arm6.current(CurrentUnits.AMP))
        sweeper_arm6.set_velocity(30, PERCENT)
        sweeper_arm6.set_max_torque(100, PERCENT)
        sweeper_arm6.spin_for(FORWARD, 195, DEGREES)
        is_scooper_down = False
        sweeper_arm6.set_stopping(HOLD)
        print("motor current",sweeper_arm6.current(CurrentUnits.AMP))
    if sweeper_arm6.is_spinning():
        print("\033[34m")
        print(console_format("sweeper arm6 is_spinning "), end="")
    if sweeper_arm6.is_done():
        print("\033[34m")
        print(console_format("sweeper arm6 is_done closing up"), end="")
    if not (sweeper_arm6.is_spinning()):
        print("\033[31m")
        print(console_format("sweeper arm6 NOT is_spinning "), end="")
        print("motor current",sweeper_arm6.current(CurrentUnits.AMP))
        sweeper_arm6.stop()
    if not sweeper_arm6.is_spinning():
        print("sweep arm6 NOT is_spinning ")
        pass
    if not sweeper_arm6.is_done():
        brain.screen.set_pen_color(Color.RED)
        print("sweeper arm6 is_done closint")
    if sweeper_arm6.is_done():
        brain.screen.set_pen_color(Color.BLUE)
        print("sweeper arm6 is_done closing")


def controller_1buttonDown_pressed_callback_0():
    global gate_state_list, is_intake_spinning, is_gate_open, is_scooper_down, is_dir_backward, my_event, gate_position, move_cntr, cur_speed, screen_precision, console_precision, controller_1_precision
    if not is_scooper_down:
        sweeper_arm6.set_max_torque(100, PERCENT)
        sweeper_arm6.set_velocity(30, PERCENT)
        sweeper_arm6.spin_for(REVERSE,195,DEGREES,wait=True)
        print("\033[32m")
        console_precision = 1
        print("motor current",sweeper_arm6.current(CurrentUnits.AMP))
        is_scooper_down = True
    if sweeper_arm6.is_spinning():
        print("\033[91m")
        print(console_format("sweeper arm6 is_spinning "), end="")
    if sweeper_arm6.is_done():
        print("\033[91m")
        print(console_format("sweeper arm6 is_done opening out"), end="")
    if not (sweeper_arm6.is_spinning()):
        print("\033[91m")
        print(console_format("sweeper arm6 NOT is_spinning stuck"), end="")
    if not (sweeper_arm6.is_done()):
        print("\033[91m")
        print(console_format("sweeper arm6 NOT is_done stuck"), end="")

# create a function for handling the starting and stopping of all autonomous tasks
def vexcode_auton_function():
    # Start the autonomous control tasks
    auton_task_0 = Thread( onauton_autonomous_0 )
    # wait for the driver control period to end
    while( competition.is_autonomous() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the autonomous control tasks
    auton_task_0.stop()

def vexcode_driver_function():
    # Start the driver control tasks
    driver_control_task_0 = Thread( ondriver_drivercontrol_0 )
    driver_control_task_1 = Thread( ondriver_drivercontrol_1 )

    # wait for the driver control period to end
    while( competition.is_driver_control() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the driver control tasks
    driver_control_task_0.stop()
    driver_control_task_1.stop()


# register the competition functions
competition = Competition( vexcode_driver_function, vexcode_auton_function )

# system event handlers
controller_1.buttonX.pressed(controller_1buttonX_pressed_callback_0)
controller_1.buttonA.pressed(controller_1buttonA_pressed_callback_0)
controller_1.buttonB.pressed(controller_1buttonB_pressed_callback_0)
controller_1.buttonLeft.pressed(controller_1buttonLeft_pressed_callback_0)
controller_1.buttonRight.pressed(controller_1buttonRight_pressed_callback_0)
controller_1.buttonL1.pressed(controller_1buttonL1_pressed_callback_0)
controller_1.buttonL2.pressed(controller_1buttonL2_pressed_callback_0)
controller_1.buttonUp.pressed(controller_1buttonUp_pressed_callback_0)
controller_1.buttonDown.pressed(controller_1buttonDown_pressed_callback_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

when_started1()

        
