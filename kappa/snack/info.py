import click
import ffmpeg
import os
import pprint
from .data import MediaFileData, MediaStreamData


def _print_stream(stream: MediaStreamData) -> None:
    exclude_fields = ["index",]
    click.echo(f"Stream #{stream.index}")
    for k, v in stream.__dict__.items():
        if k not in exclude_fields:
            click.echo(f" {k.title()}: {v}")


def _info_for_file(media_file: str) -> MediaFileData:
    props = ffmpeg.probe(media_file)
    mediafile_data = MediaFileData.from_dict(props)
    return mediafile_data


def _print_long_info_for_mediafile_data(mediafile_data: MediaFileData) -> None:
    click.echo("\n")
    click.echo(f"File: {mediafile_data.filename}")
    click.echo(f"Format: {mediafile_data.format_long_name}, {mediafile_data.format_name}")
    click.echo(f"Duration: {mediafile_data.duration}")
    click.echo(f"Size: {mediafile_data.size}")
    click.echo(f"Bitrate: {mediafile_data.bit_rate}")
    click.echo(f"Streams: {len(mediafile_data.streams)}")
    click.echo("")

    for stream in mediafile_data.streams:
        _print_stream(stream)
        click.echo("")


def _print_short_info_for_media_file_data(mediafile_data: MediaFileData) -> None:
    filename = os.path.basename(mediafile_data.filename)
    if not mediafile_data.is_video():
        click.echo(f"{filename} | {mediafile_data.format_long_name} | {mediafile_data.duration} | {mediafile_data.size} | {mediafile_data.bit_rate} | {len(mediafile_data.streams)}")
        return

    video_stream = mediafile_data.get_video_stream()
    click.echo(f"{filename}: {video_stream.codec_name} {video_stream.width}x{video_stream.height}")


def _print_mediadata_inside_dir(dir_path: str, recursive: bool = False) -> list[str]:
    skipped_files = []
    # get the list of files
    files = os.listdir(dir_path)
    for file in files:
        # non riesce a trovare il file
        file = os.path.abspath(os.path.join(dir_path, file))
        if os.path.isdir(file) and recursive:
            skipped_files += _print_mediadata_inside_dir(dir_path=file)
        else:
            try:
                mediafile_data = _info_for_file(file)
                _print_short_info_for_media_file_data(mediafile_data)
            except Exception as e:
                skipped_files.append(file)
    return skipped_files

@click.command()
# add option to get recursive
@click.option("--recursive", "-r", type=click.BOOL, is_flag=True, required=False, default=False)
@click.argument("media_path", type=click.Path(exists=True), required=True)
def info(media_path: str, recursive: bool) -> None:
    """Prints information about a media file or directory"""
    click.echo(f"Media path: {media_path}; Recursive: {recursive}")

    # if the path is just one file we can print the info
    if os.path.isfile(media_path):
        mediafile_data = _info_for_file(media_path)
        _print_long_info_for_mediafile_data(mediafile_data=mediafile_data)

    elif os.path.isdir(media_path):
        skipped_files = _print_mediadata_inside_dir(dir_path=media_path, recursive=recursive)
        click.echo(f"Skipped files: {len(skipped_files)}")
    else:
        return
