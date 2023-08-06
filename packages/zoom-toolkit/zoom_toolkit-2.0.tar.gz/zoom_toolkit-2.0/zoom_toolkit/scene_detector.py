from __future__ import print_function
import os

# Standard PySceneDetect imports:
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
# For caching detection metrics and saving/loading to a stats file
from scenedetect.stats_manager import StatsManager
from scenedetect.video_splitter import split_video_ffmpeg, split_video_mkvmerge

# For content-aware scene detection:
from scenedetect.detectors.content_detector import ContentDetector
import cv2

class SceneDetect():
    def find_scenes(video_path):
        # type: (str) -> List[Tuple[FrameTimecode, FrameTimecode]]
        video_manager = VideoManager([video_path])

        cap = cv2.VideoCapture(video_path) #to read images

        stats_manager = StatsManager()
        # Construct our SceneManager and pass it our StatsManager.
        scene_manager = SceneManager(stats_manager)

        # Add ContentDetector algorithm (each detector's constructor
        # takes detector options, e.g. threshold).
        cont_detector = ContentDetector()
        scene_manager.add_detector(cont_detector)
        #frame_list = ContentDetector.process_frame(5, [5])
        #print("frame_list", frame_list)

        base_timecode = video_manager.get_base_timecode()

        # We save our stats file to {VIDEO_PATH}.stats.csv.
        stats_file_path = '%s.stats.csv' % video_path

        scene_list = []

        try:
            # If stats file exists, load it.
            if os.path.exists(stats_file_path):
                # Read stats from CSV file opened in read mode:
                with open(stats_file_path, 'r') as stats_file:
                    stats_manager.load_from_csv(stats_file, base_timecode)

            # Set downscale factor to improve processing speed.
            video_manager.set_downscale_factor()

            # Start video_manager.
            video_manager.start()

            # Perform scene detection on video_manager.
            scene_manager.detect_scenes(frame_source=video_manager)

            # Obtain list of detected scenes.
            scene_list = scene_manager.get_scene_list(base_timecode)
            
            # Each scene is a tuple of (start, end) FrameTimecodes.

            print('List of scenes obtained:')
            for i, scene in enumerate(scene_list):
                print(
                    'Scene %2d: Start %s / Frame %d, End %s / Frame %d' % (
                    i+1,
                    scene[0].get_timecode(), scene[0].get_frames(),
                    scene[1].get_timecode(), scene[1].get_frames(),))
                
                cap.set(cv2.CAP_PROP_POS_FRAMES, scene[1].get_frames()) #ending frame
                ret, frame = cap.read() # Read the frame

                #resizing the image
                scale_percent = 50
                width = int(frame.shape[1] * scale_percent / 100)
                height = int(frame.shape[0] * scale_percent / 100)
                dsize = (width, height)
                output_frame = cv2.resize(frame, dsize)

                cv2.imshow('End frame image of one scene', output_frame) # show frame on window
                cv2.imwrite("frame%d.jpg" % scene[1].get_frames(), output_frame) 
                cv2.waitKey(0)
                cv2.destroyAllWindows()


            # We only write to the stats file if a save is required:
            if stats_manager.is_save_required():
                with open(stats_file_path, 'w') as stats_file:
                    stats_manager.save_to_csv(stats_file, base_timecode)


        finally:
            video_manager.release()

        return scene_list


    def detect(input_vid_name = "video.mp4"):
        vid_scene_list = find_scenes(input_vid_name)
        video_name = input_vid_name.split('.')[0]
        split_video_mkvmerge([input_vid_name], vid_scene_list, video_name + "scene.mp4", "video.mp4")   

        #split_video_ffmpeg(input_vid_name, vid_scene_list, "ffmpeg.mp4", "video_out.mp4")