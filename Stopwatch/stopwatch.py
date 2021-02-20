# template for "Stopwatch: The Game"
#imports
import simplegui

# define global variables
t = 0
# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenth_sec = (t) % 10
    sec = int(t / 10) % 10
    minutes = int(t / 600) % 600
    ten_min = int(t / 100) % 6
    string = str(minutes) + ":" + str(ten_min) + str(sec) + "." + str(tenth_sec)
    return string
           
# define event handlers for buttons; "Start", "Stop", "Reset"
def Start():
    timer.start()

    
def Stop():
    timer.stop()

    
def Reset():
    global t 
    timer.stop()
    t = 0
    timer.start()
    
# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t
    t += 0.1

# define draw handler
def draw(canvas):
    canvas.draw_text(format(t),(150,100),24,'White' )
    
# create frame and timer
timer = simplegui.create_timer(100,timer_handler)
frame = simplegui.create_frame('Stopwatch Game',300,200)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start',Start,100)
frame.add_button('Stop',Stop,100)
frame.add_button('Reset',Reset,100)

# start frame and timer
frame.start()

