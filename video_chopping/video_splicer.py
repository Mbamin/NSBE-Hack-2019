import subprocess
import argparse
import io
import time

from google.cloud import videointelligence
from google.cloud.videointelligence import enums

def analyze_shots(path):
    # [START video_analyze_shots]
    """ Detects camera shot changes. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print('\nProcessing video for shot change annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    fout = open("cuts.txt","w+")

    # first result is retrieved because a single video was processed
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = (shot.start_time_offset.seconds +
                      shot.start_time_offset.nanos / 1e9)
        end_time = (shot.end_time_offset.seconds +
                    shot.end_time_offset.nanos / 1e9)

        print('\tShot {}: {} to {}'.format(i, start_time, end_time))
        fout.write("slide"+str(i+1)+".mp4 "+time.strftime("%H:%M:%S",time.gmtime(start_time))+" "+time.strftime("%H:%M:%S",time.gmtime(end_time))+"\n")
    fout.close()

    with open("cuts.txt") as f:
      for line in f.readlines():
        filename, start, end = line.strip().split(' ')
        cmd = ["ffmpeg", "-i", "coursera-example.mp4", "-ss", start, "-to", end, "-c", "copy", filename]
        subprocess.run(cmd, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest='command')
    analyze_labels_parser = subparsers.add_parser(
        'labels', help=analyze_labels.__doc__)
    analyze_labels_parser.add_argument('path')
    analyze_labels_file_parser = subparsers.add_parser(
        'labels_file', help=analyze_labels_file.__doc__)
    analyze_labels_file_parser.add_argument('path')
    analyze_explicit_content_parser = subparsers.add_parser(
        'explicit_content', help=analyze_explicit_content.__doc__)
    analyze_explicit_content_parser.add_argument('path')
    analyze_shots_parser = subparsers.add_parser(
        'shots', help=analyze_shots.__doc__)
    analyze_shots_parser.add_argument('path')
    transcribe_speech_parser = subparsers.add_parser(
        'transcribe', help=speech_transcription.__doc__)
    transcribe_speech_parser.add_argument('path')

    args = parser.parse_args()

    if args.command == 'labels':
        analyze_labels(args.path)
    if args.command == 'labels_file':
        analyze_labels_file(args.path)
    if args.command == 'shots':
        analyze_shots(args.path)
    if args.command == 'explicit_content':
        analyze_explicit_content(args.path)
    if args.command == 'transcribe':
        speech_transcription(args.path)
