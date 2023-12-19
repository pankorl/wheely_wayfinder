import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

# Initialize GStreamer
Gst.init(None)

# This function will be called when the pipeline is ready to start playing
def on_pipeline_ready(bus, message, pipeline):
    if message.type == Gst.MessageType.EOS:
        pipeline.set_state(Gst.State.NULL)
    elif message.type == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        pipeline.set_state(Gst.State.NULL)

# Create the pipeline
pipeline = Gst.parse_launch(
    "udpsrc port=5201 ! application/x-rtp, encoding-name=VP8 ! rtpvp8depay ! "
    "vp8dec ! videoconvert ! appsink name=sink emit-signals=True"
)

# Get the sink element from the pipeline
appsink = pipeline.get_by_name("sink")

# This function will be called when new buffers are available at the sink
def new_sample(appsink):
    sample = appsink.emit("pull-sample")
    # Here you can access the video frame and do processing
    # buffer = sample.get_buffer()
    # ... do something with the buffer ...
    return Gst.FlowReturn.OK

appsink.connect("new-sample", new_sample)

# Set up a bus to listen to messages on the pipeline
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", on_pipeline_ready, pipeline)

# Start playing the pipeline
pipeline.set_state(Gst.State.PLAYING)

# Create a GLib MainLoop and set it to run
mainloop = GObject.MainLoop()
try:
    mainloop.run()
except KeyboardInterrupt:
    mainloop.quit()
    pipeline.set_state(Gst.State.NULL)
    print("Stopped pipeline")
