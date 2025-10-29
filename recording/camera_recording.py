import cv2

FOURCC = cv2.VideoWriter_fourcc(*'mp4v')


def record_video(filename: str, duration: int, fps: int) -> bool:

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False

    cap.set(cv2.CAP_PROP_FPS, fps)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(filename, FOURCC, fps, (frame_width, frame_height))

    total_frames = duration * fps
    frames_recorded = 0

    while frames_recorded < total_frames:
        ret, frame = cap.read()

        if ret:
            out.write(frame)
            frames_recorded += 1

        else:
            break

    cap.release()
    out.release()

    cv2.destroyAllWindows()

    if frames_recorded == total_frames:
        return True
    else:
        return False
