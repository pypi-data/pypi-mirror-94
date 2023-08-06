PyDream3
========

Python interface for talking to the Dream Cheeky 21x7 LED display (VendorId: 0x1d34 DeviceId: 0x0013)

Based on the original PyDream by Darren P. Meyer, which can be found [here](https://github.com/darrenpmeyer/pydream-led)

#

I'm fairly new to Python libraries; as a result, there may be some strange approaches here.
I'm open to accepting pull requests to improve the code, such as:

* better modularity
* support for other LED signs
* reducing reliance on "magic numbers"

Basic use
---------

First, install using `python setup.py install`

~~Or, if you prefer using PyPI: `pip install pydream-led-3`~~

The package should auto-install `pyusb`, but you will need to install libusb (upon which pyusb depends) for things to work. libusb is available for most Linux distros via their package managers, and via Homebrew on OS X. More information about installing libusb on Microsoft Windows is available [here](#installing-libusb-on-microsoft-windows).

We create an instance of the `display` object and connect:
```
import pydream3

sign = pydream3.display()
if not sign.connect():
    raise StandardError("Cannot connect to sign")
```
Then we set up a "frame" that we wish to display. We can do this using a combination of methods:
```
sign.light_on(0,0)  # turn light in upper-right corner on
sign.light_off(0,0) # the opposite

# clear_state below the "background"; 0=off, 1=on
sign.move_left(clear_state=0, count=1)   # move the frame left one
sign.move_right(clear_state=0, count=1)  # move the frame right one
sign.move_up(clear_state=0, count=1)     # up
sign.move_down(clear_state=0, count=1)   # down

sign.put_sprite(0,0,sprite)  # see Sprite section

# see Strings section
sign.put_char(0,0,'A')
sign.put_string(0,0,"Hi!")

sign.clear()  # make sign black
sign.clear(1) # make sign lit
```
We can also just specify the frame directly, like so:
```
sign.current_frame = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                      [1,0,0,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1]]
```
This approach isn't generally encouraged, which is why no method is provided
to support it. `current_frame` must be a list of 7 "rows" with 21 "columns"
each. A 1 represents a lit LED, a 0 is an unlit LED.

After setting up the frame, we can optionally set the brightness of the display:
```
sign.set_brightness(1)
```
The brightness can either be 0, 1, or 2, where 0 is darkest, 2 is brightest, and 1 is in-between

By combining these methods, we set up the frame we want to see, then tell the
display to refresh:
```
sign.refresh()
```
**NOTE:** this LED sign will only display for just under 0.4 seconds for each 
refresh. To maintain an image, `refresh()` must be called at least that 
frequently.

Sprites
-------

To draw a shape on the screen without turning each light on individually,
you can define a sprite. This is a list of lists that forms the rows and
columns of lit and unlit LEDs which define a shape. Like so:
```
eye = [[0,0,1,0,0],
       [0,1,0,1,0],
       [1,0,0,0,1],
       [0,1,0,1,0],
       [0,0,1,0,0]]
```
You can then put this sprite on the display using the `put_sprite()` method.
Putting a sprite changes the area of the frame you put the sprite to, but
otherwise leaves the frame alone.

This method supports several modes of drawing.
```
sign.put_sprite(0, 0, eye) # draw the eye at 0,0; replace what's there
sign.put_sprite(0, 0, eye, mode='and') # bitwise AND the sprite with the frame at this location
```
Possible modes to specify are:

- `replace`: the default. Replace the area of the frame with the sprite
- `and`: bit-wise AND the sprite with the frame area's content
- `or` : as `and`, but using bitwise OR
- `xor`: as `and`, but using bitwise XOR
- `invrep`: as `replace`, but inverts the sprite
- `inv`: inverts all LEDs in the sprite area
- `clear`: turn off all LEDs in the sprite area
- `fill` : turn on all LEDs in the sprite area

Strings
-------

PyDream3 is capable of displaying characters and strings using
the `put_char()` and `put_string()` methods.

These methods support the same draw modes as `put_sprite()`.
```
sign.put_char(0, 0, 'A') # draw the letter A at 0,0; replace what's there
sign.put_string(0, 0, "Hello", mode='and') # bitwise AND the string with the frame at this location
```
These commands use the PyDream3 font library. See more on fonts below

Scrolling Strings
-----------------

You may have noticed that most strings don't fit on the message board.
To solve this issue, PyDream3 has four methods: `scroll_string_right()`,
`scroll_string_left()`, `scroll_string_down()`, and `scroll_string_up()`.
These methods will automatically call `refresh` and do NOT support drawing modes.
```
sign.scroll_string_right(y, "Hello, World!", speed=1, inverse=0) # Scrolls the text left-to-right at a speed of 1
sign.scroll_string_left(y, "Hello, World!", speed=2, inverse=1) # Scrolls right-to-left, speed 2, inverted
sign.scroll_string_down(x, "Hello, World!", speed=0.5, inverse=1) # Scrolls top-to-bottom, speed 0.5, inverted
sign.scroll_string_up(x, "Hello, World!", speed=8, inverse=0) # Scrolls bottom-to-top, speed 8
```
Possible speeds are between 0 and 8, where 0 is fastest and 8 is slowest

Fonts
-----
Fonts in PyDream3 are stored as a collection of sprites, each one corresponding to
the appropriate glyph. These sprites can be replaced using the `set_glyph()` method.
```
smile = [[0,1,1,1,0],
         [1,0,0,0,1],
         [1,1,0,1,1],
         [1,0,0,0,1],
         [1,1,0,1,1],
         [1,0,1,0,1],
         [0,1,1,1,0]]

font = pydream3.font()
font.set_glyph('I', smile)
```
This code will replace the sprite for the capital letter I with a smile. Each sprite
assigned to the font must be 5x7 and follow the same rules as a regular sprite.

The font index is an index of all the sprites used to display text. This index can
be edited in bulk to completely change the font. However, this method is not
encouraged and there is no method supplied to do this. All normal list methods
(E.G. `push()`, `append()`, etc.) will still work on the font index.
```
new_font = [ASCII_char_0, ASCII_char_1, ..., ASCII_char_126, ASCII_char_127]
font.INDEX = new_font
```
Any character that is not assigned most be set to `None`.
The default font index can be found in [font.py](https://github.com/programmer2514/pydream-led-3/blob/master/pydream3/font.py#L667-L698).

Installing libusb on Microsoft Windows
--------------------------------------

1) Download the latest version of libusb from [here (7z)](https://github.com/libusb/libusb/releases/latest)
2) Extract the [7zip](https://www.7-zip.org/download.html) file and navigate to `\VS2019\MS64\dll\`
3) Copy all of the contained files to the folder of your choice (E.G. `C:\LibUSB\bin\`)
4) Press the windows key and search for `Edit the system environment variables`
5) Open it and click `Environment Variables...`
6) Under 'System Variables', find `Path` and double-click it
7) Click new and type the path that you placed the dll in (E.G. `C:\LibUSB\bin\`)
8) Click <kbd>OK</kbd>, click <kbd>OK</kbd>, and then click <kbd>OK</kbd> again
9) Restart Python
10) PyUSB syould work now
