from HandDetector import HandDetector
import cv2
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def send_test_mail(body):
    sender_email = "signalforhelhack@email.com"
    receiver_email = "signalforhelhack@gmail.com"
    msg = MIMEMultipart()
    msg['Subject'] = 'DistressSignal_cam1'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msgText = MIMEText('<b>%s</b>' % body, 'html')
    msg.attach(msgText)
    img = open('screenshot.png', 'rb').read()
    msgImg = MIMEImage(img, 'png')
    msgImg.add_header('Content-ID', '<image1>')
    msgImg.add_header('Content-Disposition', 'inline', filename='screenshot.png')
    msg.attach(msgImg)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtpObj:
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("signalforhelhack@gmail.com", "Demo1234")
            smtpObj.sendmail(sender_email, receiver_email, msg.as_string())

    except Exception as e:
        print(e)


handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)
webcamFeed.set(cv2.CAP_PROP_FRAME_WIDTH, 1000)
track_list = []
timeLast = time.time()
previousCount = -1

while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count = 0

    if len(handLandmarks) != 0:
        # we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        # details: https://google.github.io/mediapipe/solutions/hands

        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:  # Right Thumb
            count = count + 1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:  # Left Thumb
            count = count + 1

        if handLandmarks[8][2] < handLandmarks[6][2]:  # Index finger
            count = count + 1
        if handLandmarks[12][2] < handLandmarks[10][2]:  # Middle finger
            count = count + 1
        if handLandmarks[16][2] < handLandmarks[14][2]:  # Ring finger
            count = count + 1
        if handLandmarks[20][2] < handLandmarks[18][2]:  # Little finger
            count = count + 1
    timeNow = time.time()

    if int(timeNow - timeLast) > 1 and count != previousCount:
        timeLast = timeNow
        previousCount = count
        if track_list == [5, 4]:
            if count == 0 or count == 4:
                if count == 0:
                    track_list.append(count)

            else:
                track_list = []
        if track_list == [5]:
            if count == 4 or count == 5:
                if count == 4:
                    track_list.append(count)
            else:
                track_list = []
        if count == 5 and track_list == []:
            track_list.append(count)

    if track_list == [5, 4, 0]:
        # cv2.putText(image, str("call the police"), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 25)
        # Window name in which image is displayed
        window_name = 'Image'

        # font
        font = cv2.FONT_HERSHEY_SIMPLEX

        # org
        org = (100, 200)

        # fontScale
        fontScale = 1

        # Blue color in BGR
        color = (0, 0, 255)

        # Line thickness of 2 px
        thickness = 2

        # Using cv2.putText() method
        image = cv2.putText(image, 'contacting authorities', org, font,
                            fontScale, color, thickness, cv2.LINE_AA)

    cv2.imshow("Volume", image)
    print(track_list)
    if track_list == [5, 4, 0]:
        cv2.waitKey(3000)
        return_value, image = webcamFeed.read()
        # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite('C:\\Users\\Hp\\PycharmProjects\\pythonProject\\screenshot.png', image)
        send_test_mail('Photo of person in distress located by camera number 1 (Beit Hadfus 7)')
        track_list = []
    cv2.waitKey(1)

