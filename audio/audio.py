#!/usr/bin/env python
# encoding: utf-8

import gobject, pygst
pygst.require('0.10')
import gst

pipeline = gst.Pipeline("test voice")
bus = pipeline.get_bus()

# sender
alsasrc = gst.element_factory_make("pulsesrc")
# alsasrc.set_property('device', 'plughw:1,0')

q1 = gst.element_factory_make("queue", "q1")
q2 = gst.element_factory_make("queue", "q2")
audioconvert1 = gst.element_factory_make("audioconvert")
audioconvert2 = gst.element_factory_make("audioconvert")
vorbisenc = gst.element_factory_make("vorbisenc")
rtpvorbispay = gst.element_factory_make("rtpvorbispay")

# receiver
rtpvorbisdepay = gst.element_factory_make("rtpvorbisdepay")
r_q1 = gst.element_factory_make("queue", "r_q1")
r_q2 = gst.element_factory_make("queue", "r_q2")

r_audioconvert = gst.element_factory_make("audioconvert")
vorbisdec = gst.element_factory_make("vorbisdec")
autoaudiosink = gst.element_factory_make("pulsesink")

# add elements
pipeline.add(alsasrc, q1, audioconvert1, audioconvert2, vorbisenc, rtpvorbispay, rtpvorbisdepay, r_q1, vorbisdec, r_audioconvert, autoaudiosink)

# link elements
# alsasrc.link(audioconvert1)
# audioconvert1.link(vorbisenc)
# vorbisenc.link(rtpvorbispay)
gst.element_link_many(alsasrc, audioconvert1, vorbisenc, rtpvorbispay)

rtpvorbispay.link(rtpvorbisdepay)

gst.element_link_many(rtpvorbisdepay, r_q1, vorbisdec, r_audioconvert,autoaudiosink)

# gst.element_link_many(alsasrc, autoaudiosink)

def start():
    pipeline.set_state(gst.STATE_PLAYING)
    print 'Started...'
    
def loop():
    print "Running..."    
    gobject.MainLoop().run()


if __name__ == '__main__':
    start()
    loop()
