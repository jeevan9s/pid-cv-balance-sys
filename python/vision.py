# vision module 
import cv2
import numpy as np 
import time 
from typing import Callable, Optional
import config as cfg


class Vision:
    
    """
    class for vision module 
    
    - live webcam stream video capture 
    - ROI selection
    - detect ball position relative to ROI
    - filtering 
    
    """
    def __init__(self, callback: Optional[Callable[[int, int, float, float,float], None]] = None):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("failed to read webcam")
        
        self.frame_h, self.frame_w = frame.shape[:2] # get h w (indicies 0 n 1)
        
        # params 
        self.blur_ksize = 7
        self.moprh_ksize = 5
        self.min_blob_area = 60
        self.show_windows = True
        self.callback = callback
        
        self._select_roi(frame)
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.moprh_ksize, self.moprh_ksize)) 
        
    # ----- ROI -----
    def _select_roi(self, frame):
        r = cv2.selectROI("select platform ROI & press ENTER", frame, True, False)
        
        cv2.destroyWindow("select platform ROI & press ENTER")
        x,y,w,h = r
        if w == 0 or h == 0:
            self.roi = (0,0, self.frame_w, self.frame_h)
        else:
            self.roi = (int(x), int(y), int(w), int(h))
            
    def _crop_to_roi(self, frame):
        x,y,w,h = self.roi
        return frame[y:y+h, x:x+w], (x,y,w,h) # slice from y/x ref to ROI dimensions
    
    # ----- BALL -----
    def _find_ball(self, binary):
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        
        centroid = max(contours, key=cv2.contourArea)
        if cv2.contourArea(centroid) < self.min_blob_area:
            return None
        
        M = cv2.moments(centroid)
        if M["m00"] == 0:
            return None
        
        # centroid coordinate calculation
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        return (cx, cy), centroid
        
    
    def _binarize_ball(self, roi_bgr):
        # colour masking
        
        blurred = cv2.GaussianBlur(roi_bgr, (5,5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
        lower = np.array([50, 50, 50])
        upper = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower, upper)
        
        # cleaning 
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel)
        
        return mask
    
    # ----- GUI -----
    def _draw_dash(self, img, gx, gy, x_norm, y_norm, fps, found, pid_x=cfg.PID_X, pid_y=cfg.PID_Y):
        # top left
        cv2.putText(img, f"norm: ({x_norm:.3f}, {y_norm:.3f})" if found else "norm: (-, -)", 
                    (10, 24), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 225, 0), 1, cv2.LINE_AA)
        cv2.putText(img, f"fps: {fps:.1f}", (10, 46), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,0), 1, cv2.LINE_AA)

        # top right
        esc_text = "press ESC to quit"
        text_size = cv2.getTextSize(esc_text, cv2.FONT_HERSHEY_PLAIN, 0.8, 1)[0]
        cv2.putText(img, esc_text, (img.shape[1]-text_size[0]-10, 24), cv2.FONT_HERSHEY_PLAIN, 0.8, (0,0,0), 2, cv2.LINE_AA)

        # bottom left
        cv2.putText(img, f"pid_x: {pid_x['kp'], pid_x['ki'], pid_x['kd']}", (10, img.shape[0]-38),
                    cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,0), 1, cv2.LINE_AA)
        cv2.putText(img, f"pid_y: {pid_y['kp'], pid_y['ki'], pid_y['kd']}", (10, img.shape[0]-16),
                    cv2.FONT_HERSHEY_PLAIN, 0.8, (255,255,0), 1, cv2.LINE_AA)
    
    def _create_panel(self, left_bgr, right_gray):
        h,w = left_bgr.shape[:2]
        right_bgr = right_gray if right_gray.ndim == 3 else cv2.cvtColor(right_gray, cv2.COLOR_GRAY2BGR)
        
        # constrain same height 
        rh, rw = right_bgr.shape[:2]
        if rh != h:
            new_w = int(rw * (h/rh))
            right_bgr = cv2.resize(right_bgr, (new_w, h), interpolation=cv2.INTER_NEAREST)
        
        divider = np.full((h,2,3), (40,40,40), dtype=np.uint8)
        panel = np.hstack([left_bgr, divider, right_bgr])
        return panel
    
    
    # ----- MAIN -----
    def run(self):
        # main loop for live tracking
        
        showing=self.show_windows
        
        prev_t = time.perf_counter()
        fps = 0.0
        
        while True:
            ok, frame = self.cap.read()
            if not ok:
                break
            
            # roi position
            roi_frame, (rx, ry, rw, rh) = self._crop_to_roi(frame)
            binary = self._binarize_ball(roi_frame)
            res = self._find_ball(binary)
            now = time.perf_counter()
            dt = max(1e-6, now-prev_t)
            fps = 0.9*fps + 0.1*(1.0/dt)
            prev_t = now
            
            t = time.perf_counter()
            
            # dash defaults
            gx = gy = None
            x_norm = y_norm = 0.0
            found = False
            
            if res is not None:
                
                # position computation
                (cx, cy), cnt = res
                gx = rx+cx
                gy = ry+cy
                x_norm = cx / float(rw) if rw > 0 else 0.0
                y_norm = cy / float(rh) if rh > 0 else 0.0
                found = True
                
                if self.callback is not None:
                    self.callback(gx, gy, x_norm, y_norm, t)
                
                if showing:
                    cv2.circle(frame, (gx, gy), 6, (0,255,0), 2)
                    cv2.putText(
                    frame,
                    f"({gx},{gy})",
                    (gx + 10, gy - 10),              
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (0, 255, 0),
                    1,
                    cv2.LINE_AA
                )
                    
            if showing:
                cv2.rectangle(frame, (rx, ry), (rx+rw, ry+rh), (255, 0, 0), 2)
            
            if showing:
                h_roi, w_roi = roi_frame.shape[:2]
                binary_resized = cv2.resize(binary, (w_roi, h_roi), interpolation=cv2.INTER_NEAREST)
                
                vis_bin = np.zeros_like(frame[:, :, 0])
                vis_bin[ry:ry+h_roi, rx:rx+w_roi] = binary_resized
                
                self._draw_dash(frame,gx,gy,x_norm,y_norm,fps,found)
                panel = self._create_panel(frame,vis_bin)
                
                cv2.namedWindow("vision (camera | mask)", cv2.WINDOW_NORMAL)    
                cv2.imshow("vision (camera | mask)", panel)
            else:
                pass
                
            # hotkeys
            key = cv2.waitKey(1) & 0xFF
            if key == ord('\x1b'):
                break
                
        self.cap.release()
        cv2.destroyAllWindows()
           
# testing
if __name__ == "__main__":
    def test_callback(gx, gy, x_norm, y_norm, t):
        print(f"[{t:.2f}] global: ({gx},{gy}) | normalized: ({x_norm:.2f}, {y_norm:.2f})")
    
    vision = Vision(callback=test_callback)
    vision.run()
            
        
            
    
               
        
