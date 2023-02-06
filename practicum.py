import usb

RQ_GET_GYRO    = 0
RQ_SET_LED     = 1

####################################
def find_mcu_boards():
    boards = [dev for bus in usb.busses()
                  for dev in bus.devices
                  if (dev.idVendor,dev.idProduct) == (0x16c0,0x05dc)]
    return boards

####################################
class McuBoard:

    ################################
    def __init__(self, dev):
        self.device = dev
        self.handle = dev.open()

    ################################
    def usb_write(self, request, data=[], index=0, value=0):
        reqType = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_OUT
        self.handle.controlMsg(
                reqType, request, data, value=value, index=index)

    ################################
    def usb_read(self, request, length=1, index=0, value=0):
        reqType = usb.TYPE_VENDOR | usb.RECIP_DEVICE | usb.ENDPOINT_IN
        buf = self.handle.controlMsg(
                reqType, request, length, value=value, index=index)
        return buf


####################################
class PeriBoard:

    ################################
    def __init__(self, mcu):
        self.mcu = mcu

    ################################
    def get_gyro(self):
        state = self.mcu.usb_read(RQ_GET_GYRO, length=1)[0]
        return (state != 0)

    ################################
    def set_led_value(self,led_state):
        self.mcu.usb_write(RQ_SET_LED,value=led_state)

