""" Test_socketcan

    Collection of tests for socketcan module to be run with pytest / tox / coverage
    @author: Patrick Menschel (menschel.p@posteo.de)
    @license: GPL v3 
"""

import pytest

from queue import Queue

from socketcan import CanFrame,CanFlags,BCMFlags,BcmMsg,BcmOpCodes,CanRawSocket,CanIsoTpSocket,CanBcmSocket

from subprocess import CalledProcessError,check_output

from threading import Thread

import time

import platform


# TODO: Add a pytest fixture that sets up vcan0 and tears it down afterwards, this requires superuser permissions though.


class TestObjectCreation():
    
    def test_unequal_frames(self):
        can_id1 = 0x123
        data1 = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id1,
                             data=data1)
        
        can_id2 = 0x12345678
        data2 = bytes(range(0,0x44,0x11))
        frame2 = CanFrame(can_id=can_id2,
                             data=data2)
     
        assert frame1 != frame2
        
    
    def test_can_frame_creation_with_short_id(self):
        can_id = 0x123
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        flags = frame1.flags
        assert not (flags & CanFlags.CAN_EFF_FLAG)
        assert not (flags & CanFlags.CAN_RTR_FLAG)
        assert not (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
        
        
    def test_can_frame_creation_with_short_id_and_short_data(self):
        can_id = 0x123
        data = bytes(range(0,0x44,0x11))
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        flags = frame1.flags
        assert not (flags & CanFlags.CAN_EFF_FLAG)
        assert not (flags & CanFlags.CAN_RTR_FLAG)
        assert not (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
        
    def test_can_frame_creation_with_short_id_and_rtr_flag(self):
        can_id = 0x123
        flags = CanFlags.CAN_RTR_FLAG
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                          flags=flags,
                             data=data)
        flags = frame1.flags
        assert not (flags & CanFlags.CAN_EFF_FLAG)
        assert (flags & CanFlags.CAN_RTR_FLAG)
        assert not (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
        
    def test_can_frame_creation_with_short_id_and_err_flag(self):
        can_id = 0x123
        flags = CanFlags.CAN_ERR_FLAG
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                          flags=flags,
                             data=data)
        flags = frame1.flags
        assert not (flags & CanFlags.CAN_EFF_FLAG)
        assert not (flags & CanFlags.CAN_RTR_FLAG)
        assert (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
    
    
    def test_can_frame_creation_with_long_id_and_no_eff_flag(self):
        can_id = 0x12345678
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        flags = frame1.flags
        assert  (flags & CanFlags.CAN_EFF_FLAG)
        assert not (flags & CanFlags.CAN_RTR_FLAG)
        assert not (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
    
    
    def test_can_frame_creation_with_long_id_and_eff_flag(self):
        can_id = 0x12345678
        flags = CanFlags.CAN_EFF_FLAG
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                         flags=flags,
                         data=data)
        flags = frame1.flags
        assert  (flags & CanFlags.CAN_EFF_FLAG)
        assert not (flags & CanFlags.CAN_RTR_FLAG)
        assert not (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
    
        
    def test_can_frame_creation_with_long_id_and_short_data(self):
        can_id = 0x12345678
        data = bytes(range(0,0x44,0x11))
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        flags = frame1.flags
        assert  (flags & CanFlags.CAN_EFF_FLAG)
        assert not (flags & CanFlags.CAN_RTR_FLAG)
        assert not (flags & CanFlags.CAN_ERR_FLAG)
        frame_as_bytes = frame1.to_bytes()
        
        assert len(frame_as_bytes) == CanFrame.get_size()
        
        frame2 = CanFrame.from_bytes(frame_as_bytes)
        assert frame1 == frame2
        
        
    def test_bcm_msg_creation(self):
        can_id = 0x123
        data = bytes(range(0,0x88,0x11))
         
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        opcode = BcmOpCodes.TX_SETUP
        flags = (BCMFlags.SETTIMER | BCMFlags.STARTTIMER)
        frames = [frame1,]
        interval=0.1
        bcm1 = BcmMsg(opcode=opcode,
                     flags=flags,
                     can_id=can_id,
                     frames = frames,
                     ival2=interval,
                     )
        bcm_as_bytes = bcm1.to_bytes()
        assert len(bcm_as_bytes) == BcmMsg.get_size()+(CanFrame.get_size()*len(frames))
        
        bcm2 = BcmMsg.from_bytes(bcm_as_bytes)
        assert bcm1 == bcm2
        
        
    def test_unequal_bcm_msgs(self):
        can_id = 0x123
        data = bytes(range(0,0x88,0x11))
         
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        opcode = BcmOpCodes.TX_SETUP
        flags = (BCMFlags.SETTIMER | BCMFlags.STARTTIMER)
        frames = [frame1,]
        interval=0.1
        bcm1 = BcmMsg(opcode=opcode,
                     flags=flags,
                     can_id=can_id,
                     frames = frames,
                     ival2=interval,
                     )
        bcm_as_bytes = bcm1.to_bytes()
        assert len(bcm_as_bytes) == BcmMsg.get_size()+(CanFrame.get_size()*len(frames))
        
        interval2 = 1
        bcm2 = BcmMsg(opcode=opcode,
                 flags=flags,
                 can_id=can_id,
                 frames = frames,
                 ival2=interval2,
                 )
        
        assert bcm1 != bcm2
    
    def test_bcm_msg_creation_with_2_frames(self):
        can_id = 0x123
        data = bytes(range(0,0x88,0x11))
         
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        can_id2 = 0x456
        data2 = bytes(range(0,0x88,0x11))
        frame2 = CanFrame(can_id=can_id2,
                             data=data2)
            
        opcode = BcmOpCodes.TX_SETUP
        flags = (BCMFlags.SETTIMER | BCMFlags.STARTTIMER)
        frames = [frame1,
                  frame2,
                  ]
        interval=0.1
        bcm1 = BcmMsg(opcode=opcode,
                     flags=flags,
                     can_id=can_id,
                     frames = frames,
                     ival2=interval,
                     )
        bcm_as_bytes = bcm1.to_bytes()
        assert len(bcm_as_bytes) == BcmMsg.get_size()+(CanFrame.get_size()*len(frames))
        
        bcm2 = BcmMsg.from_bytes(bcm_as_bytes)
        assert bcm1 == bcm2
    
    
    def test_bcm_msg_creation_with_2_extended_frames_and_different_sizes(self):
        can_id = 0x12345678
        data = bytes(range(0,0x88,0x11))
         
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        can_id2 = 0x1FFFF456
        data2 = bytes(range(0,0x44,0x11))
        frame2 = CanFrame(can_id=can_id2,
                             data=data2)
            
        opcode = BcmOpCodes.TX_SETUP
        flags = (BCMFlags.SETTIMER | BCMFlags.STARTTIMER)
        frames = [frame1,
                  frame2,
                  ]
        interval=0.1
        bcm1 = BcmMsg(opcode=opcode,
                     flags=flags,
                     can_id=can_id,
                     frames = frames,
                     ival2=interval,
                     )
        bcm_as_bytes = bcm1.to_bytes()
        assert len(bcm_as_bytes) == BcmMsg.get_size()+(CanFrame.get_size()*len(frames))
        
        bcm2 = BcmMsg.from_bytes(bcm_as_bytes)
        assert bcm1 == bcm2
    
    
    
    def test_bcm_msg_creation_with_2_extended_frames_and_ival1(self):
        can_id = 0x12345678
        data = bytes(range(0,0x88,0x11))
         
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        can_id2 = 0x1FFFF456
        data2 = bytes(range(0,0x44,0x11))
        frame2 = CanFrame(can_id=can_id2,
                             data=data2)
            
        opcode = BcmOpCodes.TX_SETUP
        flags = (BCMFlags.SETTIMER | BCMFlags.STARTTIMER)
        frames = [frame1,
                  frame2,
                  ]
        interval1 = 0.1
        interval2 = 5
        bcm1 = BcmMsg(opcode=opcode,
                     flags=flags,
                     can_id=can_id,
                     frames = frames,
                     ival1=interval1,
                     ival2=interval2,
                     )
        bcm_as_bytes = bcm1.to_bytes()
        assert len(bcm_as_bytes) == BcmMsg.get_size()+(CanFrame.get_size()*len(frames))
        
        bcm2 = BcmMsg.from_bytes(bcm_as_bytes)
        assert bcm1 == bcm2

def is_interface_present(interface):
    """ helper function """
    try:
        if check_output("ifconfig | grep {0}".format(interface), shell=True).strip():
            return True
    except CalledProcessError:
        pass    
    return False

def is_isotp_available():
    """ helper function """
    try:
        if check_output("ls /lib/modules/$(uname -r)/kernel/net/can/can-isotp.ko",shell=True).strip():
            return True
    except CalledProcessError:
        pass
    return False

@pytest.mark.skipif(not is_interface_present("vcan0"), reason="this test requires vcan0 to be set up")
class TestSocketOperations:

    def receive_from_can_raw_socket(self,interface,q):
        """ helper function """
        s = CanRawSocket(interface=interface)
        q.put(s.recv())

    def test_can_raw_socket(self):
        interface = "vcan0"
        s = CanRawSocket(interface=interface)
        can_id = 0x12345678
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                             data=data)
        
        q = Queue()
        p = Thread(target=self.receive_from_can_raw_socket, args=(interface,q,))
        p.setDaemon(True)
        p.start()
        time.sleep(1)
        s.send(frame1)
        frame2 = q.get()
        p.join()
         
        assert frame1 == frame2
    
    def receive_from_can_isotp_socket(self,interface,rx_addr,tx_addr,bufsize,q):
        """ helper function """
        s = CanIsoTpSocket(interface=interface, rx_addr=rx_addr, tx_addr=tx_addr)
        q.put(s.recv(bufsize=bufsize))
    
    @pytest.mark.skipif(not  is_isotp_available(), reason="this test requires isotp kernel module, mainline kernel >= 5.10")
    def test_can_isotp_socket(self):
        interface = "vcan0"
        rx_addr = 0x7e0
        tx_addr = 0x7e8
        s = CanIsoTpSocket(interface=interface, rx_addr=rx_addr, tx_addr=tx_addr)
        data = bytes(list(range(64)))
        bufsize = len(data)
        q = Queue()
        # Note: the receive thread logically has rx_addr, tx_addr inverted!
        p = Thread(target=self.receive_from_can_isotp_socket, args=(interface,tx_addr,rx_addr,bufsize,q,))
        p.setDaemon(True)
        p.start()
        time.sleep(1)        
        s.send(data)
        
        data2 = q.get()
        p.join()
        
        assert data == data2
        
    def test_bcm_msg_and_bcm_socket_send_operation(self):
        interface="vcan0"
        s = CanBcmSocket(interface=interface)
        
        can_id = 0x12345678
        data = bytes(range(0,0x88,0x11))
        frame1 = CanFrame(can_id=can_id,
                          data=data)
        
        bcm = BcmMsg(opcode=BcmOpCodes.TX_SETUP,
                     flags=(BCMFlags.SETTIMER | BCMFlags.STARTTIMER),
                     can_id=can_id,
                     frames = [frame1,],
                     ival1=0,
                     ival2=1,
        )
        q = Queue()
        p = Thread(target=self.receive_from_can_raw_socket, args=(interface,q,))
        p.setDaemon(True)
        p.start()
        try:
            s.send(bcm)
        except OSError:
            assert False, "The length of bcm_msg is false. Length {0} Platform {1}".format(len(bcm.to_bytes()),platform.machine())
        else:
            time.sleep(1)
            frame2 = q.get()
            p.join()
                        
            assert frame1 == frame2
