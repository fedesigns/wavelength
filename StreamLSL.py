"""
Search for available Muses and creating a new stream using the muselsl library
"""

from muselsl import stream, list_muses

if __name__ == "__main__":

    muses = list_muses()

    if not muses:
        print('No Muses found')
    else:
        stream(muses[0]['address'])

        # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
        print('Stream has ended')