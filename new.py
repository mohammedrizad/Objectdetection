import cv2
import numpy as np
import time
import pyttsx3
import speech_recognition as sr

class Detector:
    def init(self, configPath, modelPath, classesPath):
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)
        self.read_classes()

    def read_classes(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
        self.classesList.insert(0, 'Background')
        self.colorList = np.random.uniform(low=0, high=225, size=(len(self.classesList), 3))

    def on_cam(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error opening webcam...")
            return
        detected_objects = set()
        tts = pyttsx3.init()
        startTime = 0
        while True:
            currentTime = time.time()
            fps = 1 / (currentTime - startTime)
            startTime = currentTime
            success, image = cap.read()
            if not success:
                break
            classLabelIDs, confidences, bboxs = self.net.detect(image, confThreshold=0.4)
            bboxs = list(bboxs)
            confidences = list(np.array(confidences).reshape(1, -1)[0])
            confidences = list(map(float, confidences))
            bboxIdx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold=0.5, nms_threshold=0.2)
            if len(bboxIdx) != 0:
                for i in range(len(bboxIdx)):
                    bbox = bboxs[np.squeeze(bboxIdx[i])]
                    classConfidence = confidences[np.squeeze(bboxIdx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIdx[i])])
                    classLabel = self.classesList[classLabelID]
                    if classLabel not in detected_objects:
                        print(classLabel)
                        print(classConfidence)
                        detected_objects.add(classLabel)
                        tts_text = classLabel
                        tts.say(tts_text)
                        tts.runAndWait()
                    classColor = [int(c) for c in self.colorList[classLabelID]]
                    x, y, w, h = bbox
                    cv2.rectangle(image, (x, y), (x + w, y + h), color=classColor, thickness=1)
                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)
                    cv2.putText(image, displayText, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, classColor, 2)
            cv2.putText(image, "FPS: " + str(int(fps)), (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.imshow("Object Detection", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Please speak something...")
        audio = recognizer.listen(source)
    # Recognize the captured audio
    try:
        recognized_text = recognizer.recognize_google(audio)
        print(recognized_text)
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")

    configPath = "model_data/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    modelPath = "model_data/frozen_inference_graph.pb"
    classesPath = "model_data/coco.names"
    detector = Detector(configPath, modelPath, classesPath)
    detector.on_cam()