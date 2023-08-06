import usb.core
# import usb.util
import time
import struct
from .font import font

def util_byteify(row):
    byte = [0,0,0]
    mrow = [0,0,0]
    mrow.extend( reversed( list(row) ) )

    for i in range(0,len(mrow)):
        if mrow[i]:
            mrow[i] = '0' # device spec: 0 is "on". Weird.
        else:
            mrow[i] = '1'

    byte[0] = ''.join(mrow[:8])
    byte[1] = ''.join(mrow[8:16])
    byte[2] = ''.join(mrow[16:])

    for i in range(0,3):
        byte[i] = int( byte[i], 2 )

    return byte

class display():

    # vendorID = 0x1d34
    # deviceID = 0x0013

    def clear(self, state=0):
        self.current_frame = []
        for row in range(0,7):
            a_row = []
            for col in range(0,21):
                a_row.append(state)
            self.current_frame.append(a_row)

    def __init__(self):
        self.brightness = 2
        self.clear()

    def connect(self):
        self.device = usb.core.find(idVendor=0x1d34, idProduct=0x0013)
        if self.device == None:
            return 0
        
        self.device.set_configuration()
        return 1

    def is_connected(self):
        if self.device == None:
            return 0
        return 1

    def _pack_current_frame(self):
        cframe = self.current_frame
        packed_frame = []
        
        for start in [0,2,4,6]:
            byterow = [0, start]
            byterow.extend( util_byteify(cframe[start]) )

            if start < 6:
                byterow.extend( util_byteify(cframe[start+1]) )
            else:
                byterow.extend([0,0,0])
                
            byterow[0] = self.brightness

            for i in range(0,len(byterow)):
                byterow[i] = bytes([byterow[i]])

            packed_frame.append(
                struct.pack(
                    'cccccccc',
                    byterow[0],
                    byterow[1],
                    byterow[2],
                    byterow[3],
                    byterow[4],
                    byterow[5],
                    byterow[6],
                    byterow[7],
                    )
                )

        self.packed_frame = packed_frame

    def _send_packed_frame(self):
        count = 0
        while True:
            try:
                for i in range(0,4):
                    assert self.device.ctrl_transfer(0x21, 0x09, 0, 0, self.packed_frame[i]) == 8
            except Exception as e:
                count += 1
                if count >= 100:
                    raise Exception("Request timed out with the following error:\n" + str(e))
                    break
                self.connect()
                continue
            else:
                count = 0
                break

    def refresh(self):
        self._pack_current_frame()
        self._send_packed_frame()
        
    def set_brightness(self, value="2"):
        self.brightness = value

    def change_light(self, col, row, state):
        self.current_frame[row][col] = state

    def light_on(self, x, y):
        self.change_light(x, y, 1)

    def light_off(self, x, y):
        self.change_light(x, y, 0)

    def put_sprite(self, x, y, sprite, mode='replace'):
        row = y
        for gridrow in sprite:
            col = x
            for state in gridrow:
                if (row >= 0) and (col >= 0) and (row < 7) and (col < 21):
                    if mode == 'replace':
                        self.current_frame[row][col] = state
                    elif mode == 'and':
                        self.current_frame[row][col] = self.current_frame[row][col] & state
                    elif mode == 'or':
                        self.current_frame[row][col] = self.current_frame[row][col] | state
                    elif mode == 'xor':
                        self.current_frame[row][col] = self.current_frame[row][col] ^ state
                    elif mode == 'invrep':
                        if state == 1:
                            self.current_frame[row][col] = 0
                        else:
                            self.current_frame[row][col] = 1
                    elif mode == 'inv':
                        if self.current_frame[row][col] == 1:
                            self.current_frame[row][col] = 0
                        else:
                            self.current_frame[row][col] = 1
                    elif mode == 'clear':
                        self.current_frame[row][col] = 0
                    elif mode == 'fill':
                        self.current_frame[row][col] = 1
                    else:
                        raise ValueError("Mode must be one of: replace, and, or, xor, invrep, inv, clear, fill")
                col += 1
            row += 1

        self.current_frame = self.current_frame[:7]
        for r in range(0, len(self.current_frame)):
            self.current_frame[r] = self.current_frame[r][:21]
        
    def put_char(self, x, y, char, mode='replace'):
        if font.INDEX[ord(char)] != None:
            self.put_sprite(x, y, font.INDEX[ord(char)], mode)
        
    def put_string(self, x, y, string, mode='replace'):
        offset = 0
        for i in string:
            self.put_char(x + offset, y, i, mode)
            offset += 6
            
    def scroll_string_right(self, y, string, speed=1, inverse=0):
        index = -(len(string) * 6) + 1
        scroll_len = (len(string) * 6) + 21
        for x in range(scroll_len):
            self.clear(inverse)
            if inverse == 0:
                self.put_string(index, y, string)
            else:
                self.put_string(index, y, string, mode='invrep')
            self.refresh()
            if speed <= 4:
                time.sleep(speed / 10)
            elif speed <= 8:
                time.sleep(0.2)
                self.refresh()
                time.sleep(0.2)
                self.refresh()
                time.sleep(speed / 20)
            else:
                raise ValueError("Speed must be between 0 and 8")
            index += 1
            
    def scroll_string_left(self, y, string, speed=1, inverse=0):
        index = 21
        scroll_len = (len(string) * 6) + 21
        for x in range(scroll_len):
            self.clear(inverse)
            if inverse == 0:
                self.put_string(index, y, string)
            else:
                self.put_string(index, y, string, mode='invrep')
            self.refresh()
            if speed <= 4:
                time.sleep(speed / 10)
            elif speed <= 8:
                time.sleep(0.2)
                self.refresh()
                time.sleep(0.2)
                self.refresh()
                time.sleep(speed / 20)
            else:
                raise ValueError("Speed must be between 0 and 8")
            index -= 1
            
    def scroll_string_down(self, x, string, speed=1, inverse=0):
        index = -7
        for y in range(15):
            self.clear(inverse)
            if inverse == 0:
                self.put_string(x, index, string)
            else:
                self.put_string(x, index, string, mode='invrep')
            self.refresh()
            if speed <= 4:
                time.sleep(speed / 10)
            elif speed <= 8:
                time.sleep(0.2)
                self.refresh()
                time.sleep(0.2)
                self.refresh()
                time.sleep(speed / 20)
            else:
                raise ValueError("Speed must be between 0 and 8")
            index += 1
            
    def scroll_string_up(self, x, string, speed=1, inverse=0):
        index = 7
        for y in range(15):
            self.clear(inverse)
            if inverse == 0:
                self.put_string(x, index, string)
            else:
                self.put_string(x, index, string, mode='invrep')
            self.refresh()
            if speed <= 4:
                time.sleep(speed / 10)
            elif speed <= 8:
                time.sleep(0.2)
                self.refresh()
                time.sleep(0.2)
                self.refresh()
                time.sleep(speed / 20)
            else:
                raise ValueError("Speed must be between 0 and 8")
            index -= 1

    def move_right(self, clear_state=0, count=1):
        for row in self.current_frame:
            for c in range(0,count):
                row.insert(0, clear_state)
                row.pop()

    def move_left(self, clear_state=0, count=1):
        for row in self.current_frame:
            for c in range(0,count):
                row.append(clear_state)
                row.pop(0)

    def move_down(self, clear_state=0, count=1):
        new_row = []
        for i in range(0,21):
            new_row.append(clear_state)

        for i in range(0,count):
            self.current_frame.insert(0,new_row)
            self.current_frame.pop()

    def move_up(self, clear_state=0, count=1):
        new_row = []
        for i in range(0,21):
            new_row.append(clear_state)

        for i in range(0,count):
            self.current_frame.append(new_row)
            self.current_frame.pop(0)