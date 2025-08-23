from server.core.audio_processor.event_generation import EventGenerator
from server.core.lyrics_handler import LyricsHandler
from server.core.album_processor import AlbumProcessor
from server.core.image_generator import ImageGenerator
from server.core.video_composer.text_renderer import ArtisticTextRenderer
from server.core.video_composer.video_export import VideoExporter
import os

def process_song(file_path: str, output_dir: str, style_preset="minimal_geometric"):
    audio_analysis = EventGenerator().generate_events(file_path)

    events_with_lyrics = LyricsHandler().process(file_path, audio_analysis["events"])

    album_processor = AlbumProcessor(n_colors=5)
    color_palette = album_processor.process_album(file_path)
    
    image_dir = os.path.join(output_dir, "images")
    os.makedirs(image_dir, exist_ok=True)
    
    image_generator = ImageGenerator()
    image_generator.generate_images(
        events_with_lyrics,
        output_dir=image_dir,
        style_preset=style_preset,
        color_palette=color_palette
    )

    if events_with_lyrics:
        text_renderer = ArtisticTextRenderer()
        text_renderer.process_image_directory(image_dir, events_with_lyrics,color_palette)

    video_exporter = VideoExporter()
    
    song_name = os.path.splitext(os.path.basename(file_path))[0]
    output_video = os.path.join(output_dir, f"{song_name}_video.mp4")
    
    video_exporter.create_video(image_dir, file_path, events_with_lyrics, output_video)
    
    return output_video