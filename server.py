import time
import zmq

class Connection:
    string_message = ""
    shape_feedback = ""
    color_feedback = ""

    @staticmethod
    def server():
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:5555")

        messages = []
    
        while True:
            #  Wait for next request from client
            message = socket.recv()
            #print("Received request: %s" % message)

            Connection.string_message = message.decode("utf-8")
            
            errorDetection = Connection.color_feedback + " " + Connection.shape_feedback
            feedbackToUnity = errorDetection.encode()

            #print(errorDetection)

            #  In the real world usage, you just need to replace time.sleep() with
            #  whatever work you want python to do.-
            #time.sleep(1)
            messages.append(message)

            #  Send reply back to client
            #  In the real world usage, after you finish your work, send your output here
            socket.send(feedbackToUnity)