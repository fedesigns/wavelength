"""
Recording data from an existing Muse LSL stream
"""

from muselsl import record

if __name__ == "__main__":

    # Note: an existing Muse LSL stream is required
    record(300)

    # Note: Recording is synchronous, so code here will not execute until the stream has been closed
    print('Recording has ended')