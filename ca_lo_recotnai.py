import cv2
import numpy as np

def detect_square(mask, frame, label, rect_color, text_color):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            # Xấp xỉ đa giác
            epsilon = 0.04 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            if len(approx) == 4 and cv2.isContourConvex(approx):
                # Kiểm tra tỷ lệ vuông
                x, y, w, h = cv2.boundingRect(approx)
                ratio = float(w) / h
                if 0.9 <= ratio <= 1.1:  # Gần vuông
                    # Vẽ hình vuông
                    cv2.drawContours(frame, [approx], -1, rect_color, 2)

                    # Tính tọa độ tâm
                    M = cv2.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        side_length = (w + h) / 2  # Trung bình cạnh

                        # Vẽ tâm
                        cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)

                        # Hiển thị thông tin
                        cv2.putText(frame, f'{label} Square', (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)
                        cv2.putText(frame, f'Center: ({cx},{cy})', (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)
                        cv2.putText(frame, f'Side: {int(side_length)} px', (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1)

                        return True  # Đã phát hiện một hình vuông
    return False

# Thiết lập màu HSV
lower_red1, upper_red1 = np.array([0, 100, 100]), np.array([10, 255, 255])
lower_red2, upper_red2 = np.array([160, 100, 100]), np.array([179, 255, 255])
lower_blue, upper_blue = np.array([100, 50, 50]), np.array([130, 255, 255])

cap = cv2.VideoCapture(0)
debug = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask_red = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1),
                              cv2.inRange(hsv, lower_red2, upper_red2))
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    if debug:
        cv2.imshow('Mask Red', mask_red)
        cv2.imshow('Mask Blue', mask_blue)

    detected_red = detect_square(mask_red, frame, 'Red', (0, 255, 0), (0, 0, 255))
    detected_blue = detect_square(mask_blue, frame, 'Blue', (0, 0, 255), (0, 255, 0))

    if detected_red:
        cv2.putText(frame, 'Phat hien hinh vuong do', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if detected_blue:
        cv2.putText(frame, 'Phat hien hinh vuong xanh', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
