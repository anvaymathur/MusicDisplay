import time
import microcontroller
import busio, displayio, digitalio, pwmio, rotaryio, keypad
import usb_cdc, usb_hid, vetorio, terminalio
from adafruit_display_text import label
from adafruit_ili9341 import ILI9341
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode as Key

try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire


p = microcontroller.pin

displayio.release_displays()
spi = busio.SPI(P.GPIO12, MOSI=P.GPIO1, MISO=P.GPIO13)
bus = FourWire(spi, command=P.GPIO8, chip_select=P.GPIO10, reset=P.GPIO9, baudrate=40_000_000)
display = ILI9341(bus, width=320, height=240, rotaton=0)
backlight = pwmio.PWMOut(P.GPIO5, frequency=5000, duty_cycle=0)

def set_brightness(pct):
    backlight.duty_cycle = pct * 65535 // 100

class State:
    volume = 40
    muted = False
    brightness = 80
    adjusting_brightness = 80
    playing = False
    title = "Playing Nothing"
    artist = ""
    hour, minute = 12, 0
    clock_t0 = time.monotonic()

st = State()


WHITE, BLACK, GREY, HDR = 0xFFFFFF, 0x000000, 0xBBBBBB, 0x202020
ACC, MUTE = 0x1DB954, 0x777777

ui = displayio.Group()
display.root_group = ui

def rect(x,y,w,h,color):
    pal = displayio.Palette(1)
    pal[0] = color
    r = vetorio.Rectangle(pixel_shader=pal, width=w, height=h, x=x, y=y)
    ui.append(r)
    return r

def text(s, x, y, color, scale=1, right=False):
    l = label.Label(terminalio.FONT, text=s, color=color, scale=scale)
    l.anchor_point = (1.0 if right else 0.0, 0.0)
    l.anchored_position = (x,y)
    ui.append(l)
    return l

def fit(s, n):
    return s if len(s) <= n else s[:n - 2] + "..."

rect(0, 0, 320, 28, HDR)
app_lbl = text("No Source", 8, 8, WHITE)
clock_lbl = text("12:00", 312, 8, WHITE, right=True)

title_lbl = text("", 120, 56, WHITE, scale=2)
artist_lbl = text("", 120, 92, GREY)
status_lbl = text("", 120, 120, ACC)

bar_lbl = text("Volume", 12, 204, WHITE)
rect(90, 202, 170, 12, WHITE) # Outline
rect(92, 204, 166, 8, BLACK) # inside
bar = rect(92, 204, 1, 8, ACC) # the filled part
pct_lbl = text("40%", 312,  204, WHITE, right=True)

art = None
def show_art(path="/art.bmp"):
    """Writing an image: load a BMP from the drive and put it at x=12, y=48."""
    global art
    bmp = displayio.OnDiskBitmap(path)
    tile = displayio.TileGrid(bmp, pixel_shader=bmp.pixel_shader, x=12, y=48)
    if art is not None:
        ui.remove(art)

    ui.append(tile)
    art = tile

def draw_bar():
    value = st.brightness if st.adjusting_brightness else st.volume
    muted = st.muted and not st.adjusting_brightness
    bar_lbl.text = "BRIGHT" if st.adjusting_brightness else ("MUTED" if muted else "VOLUME")
    bar.width = max(1, 166 * value // 100)
    bar.pixel_shader[0] = MUTE if muted else ACC
    pct_lbl.text = "%d%%" % value

def draw_track():
    title_lbl.text = fit(st.title, 15)
    artist_lbl.text = fit(st.artist, 30)
    status_lbl.text = "Playing" if st.playing else "Paused"

def draw_clock():
    clock_lbl.text = "%02d:%02d" % (st.hour, st.minute)

try:
    show_art()
except (OSError, ValueError):
    pass                       

draw_bar(); draw_track(); draw_clock()
set_brightness(st.brightness)  

enc = rotaryio.IncrementalEncoder(P.GPIO1, P.GPIO2)   
keys = keypad.Keys((P.GPIO4,), value_when_pressed=False, pull=True)
touch_irq = digitalio.DigitalInOut(P.GPIO6)           
touch_irq.pull = digitalio.Pull.UP
cc = ConsumerControl(usb_hid.devices)

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def on_turn(delta):
    if st.adjusting_brightness:
        st.brightness = clamp(st.brightness + 5 * delta, 10, 100)
        set_brightness(st.brightness)
    else:
        for _ in range(abs(delta)):
            cc.send(Key.VOLUME_INCREMENT if delta > 0 else Key.VOLUME_DECREMENT)
        st.volume = clamp(st.volume + 2 * delta, 0, 100)
        st.muted = False
    draw_bar()

press_t = 0
def on_key(ev):
    global press_t
    if ev.pressed:
        press_t = time.monotonic()
        return
    if time.monotonic() - press_t >= 0.6:            
        st.adjusting_brightness = not st.adjusting_brightness
    elif st.adjusting_brightness:                    
        st.adjusting_brightness = False
    else:                                            
        cc.send(Key.MUTE)
        st.muted = not st.muted
    draw_bar()

was_touched, last_tap = False, 0
def poll_touch():
    global was_touched, last_tap
    touched = not touch_irq.value
    if touched and not was_touched and time.monotonic() - last_tap > 0.4:
        last_tap = time.monotonic()
        cc.send(Key.PLAY_PAUSE)                     
        st.playing = not st.playing
        draw_track()
    was_touched = touched


ser = usb_cdc.data
rx = b""

def handle(line):
    p = line.split("|")
    if p[0] == "NOW" and len(p) >= 2:                
        st.title = p[1]
        st.artist = p[2] if len(p) > 2 else ""
        app_lbl.text = fit(p[3], 24) if len(p) > 3 else ""
        draw_track()
    elif p[0] == "PLAY" and len(p) >= 2:             
        st.playing = (p[1] == "1")
        draw_track()
    elif p[0] == "TIME" and len(p) >= 2:             
        h, m = p[1].split(":")
        st.hour, st.minute, st.clock_t0 = int(h), int(m), time.monotonic()
        draw_clock()
    elif p[0] == "ART" and len(p) >= 2:              
        show_art(p[1])

def poll_serial():
    global rx
    if ser is None:
        return
    if ser.in_waiting:
        rx += ser.read(ser.in_waiting)
    while b"\n" in rx:
        line, rx = rx.split(b"\n", 1)
        try:
            handle(line.decode().strip())
        except (ValueError, UnicodeError, OSError):
            pass

last_pos = enc.position
while True:
    pos = enc.position
    if pos != last_pos:
        on_turn(pos - last_pos)
        last_pos = pos
    ev = keys.events.get()
    if ev:
        on_key(ev)
    poll_touch()
    poll_serial()
    if time.monotonic() - st.clock_t0 >= 60:
        st.clock_t0 += 60
        st.minute += 1
        if st.minute >= 60:
            st.minute, st.hour = 0, (st.hour + 1) % 24
        draw_clock()
    time.sleep(0.005)