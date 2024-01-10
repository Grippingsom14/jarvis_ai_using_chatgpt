import os
import cv2
import sys
sys.path.append('jarvis-listening')
from listening import generate_random_string
import base64
from langchain_openai import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage


def encode_image(image_url):
    with open(image_url, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


cap = cv2.VideoCapture(0) # 0 stands for very first webcam attach

frame_iteration = 0
while True:
    isSuccess, frame = cap.read()
    frame_iteration += 1
    if frame_iteration > 5:
        if not isSuccess:
            print("Error reading frame")

        else:
            filename = f"misc/temp/image_{generate_random_string(6)}.png"
            cv2.imwrite(filename, frame)
            base64_image = encode_image(filename)

            chat = ChatOpenAI(model='gpt-4-vision-preview', max_tokens=256)

            output = chat.invoke([
                HumanMessage(
                    content=[
                        {"type": "text", "text": "Describe the person's clothing and wearing including colors of each. Focus on details and reply within 50 words"},
                        {"type": "image_url",
                         "image_url": {
                             "url": "data:image/png;base64," + base64_image,
                             "detail": "auto"
                         }}
                    ])
            ])

            print(output)
            print("DONE")
            os.remove(filename)
        break


cap.release()  # release webcam
cv2.destroyAllWindows()  # close all openCV windows