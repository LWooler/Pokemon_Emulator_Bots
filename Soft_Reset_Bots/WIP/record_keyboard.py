import time
import keyboard

start_time = time.time();
last_time = time.time();

keystroke = [];
timing = [];
pressed = [];

def hook_press(key):
    print(key.scan_code)

# Collect events until released
# with keyboard.Listener(
#         hook=hook) as listener:
#     listener.join()

# keyboard.hook(hook_press);
# while 1:
#     c = 1;

recorded = keyboard.record(until='esc')

end_time = time.time();
print(end_time-start_time);
print(recorded);

for i in recorded:
    if i.event_type == 'down':
        print(i.name, end = " ")
        print(i.time - start_time, end = " ")
        print(i.event_type)

# recorded = keyboard2.record(until='esc')
# keyboard2.play(recorded, speed_factor=1)
