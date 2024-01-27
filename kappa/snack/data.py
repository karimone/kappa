import dataclasses
from decimal import Decimal as D

VIDEO = "video"
AUDIO = "audio"
DATA = "data"


@dataclasses.dataclass
class MediaStreamData:
    index: int
    codec_type: str
    codec_tag_string: str
    duration_ts: int
    duration: D
    codec_long_name: str | None = None
    codec_name: str | None = None
    profile: str | None = None
    bit_rate: int | None = None
    width: int| None = None
    height: int | None = None
    coded_width: int | None = None
    coded_height: int | None = None
    closed_captions: int | None = None
    sample_aspect_ratio: str | None = None
    display_aspect_ratio: str | None = None
    pix_fmt: str | None = None
    level: int | None = None
    color_range: str | None = None
    color_primaries: str | None = None
    field_order: str | None = None
    refs: int | None = None

    def is_video(self):
        return self.codec_type == VIDEO

    def is_audio(self):
        return self.codec_type == AUDIO

    def is_data(self):
        return self.codec_type == DATA


    @classmethod
    def from_dict(cls, stream: dict) -> "MediaStreamData":
        stream_fields = [field for field in cls.__dataclass_fields__.keys()]
        stream_data = dict()
        for k, v in stream.items():
            if k in stream_fields:
                stream_data[k] = v
        return cls(**stream_data)


@dataclasses.dataclass
class MediaFileData:
    filename: str
    format_name: str
    format_long_name: str
    start_time: D
    duration: D
    size: int
    bit_rate: int
    streams: list[MediaStreamData]

    @classmethod
    def from_dict(cls, media_data: dict) -> "MediaFileData":
        format: dict = media_data["format"]
        streams: list[dict] = media_data["streams"]

        MediaFileData_fields = [field for field in MediaFileData.__dataclass_fields__.keys() if field != "streams"]
        media_file = dict()
        for k, v in format.items():
            if k in MediaFileData_fields:
                media_file[k] = v

        media_streams: list[MediaStreamData] = list()
        for stream in streams:
            media_streams.append(MediaStreamData.from_dict(stream))

        media_file["streams"] = media_streams
        return cls(**media_file)

    def is_video(self):
        """Returns True if the file has video streams"""
        return any([stream.is_video() for stream in self.streams])

    def get_video_stream(self) -> MediaStreamData:
        """Returns the first video stream"""
        return next(stream for stream in self.streams if stream.is_video())
