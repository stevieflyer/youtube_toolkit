from pathlib import Path
from typing import Literal, Optional

from autom import AutomSchema, AutomField

SubtitleFormat = Literal[
    "json3",
    "srv1",
    "srv2",
    "srv3",
    "ttml",
    "vtt",
]


SubtitleLanguage = Literal[
    "fr-FR",  # 法语 (French)
    "ko",     # 韩语 (Korean)
    "en",     # 英语 (English)
    "es",     # 西班牙语 (Spanish)
    "de",     # 德语 (German)
    "ja",     # 日语 (Japanese)
    "zh-CN",  # 简体中文 (Simplified Chinese)
    "zh-TW",  # 繁体中文 (Traditional Chinese)
    "ru",     # 俄语 (Russian)
    "pt",     # 葡萄牙语 (Portuguese)
    "it",     # 意大利语 (Italian)
    "hi"      # 印地语 (Hindi)
]


class SubtitleOptions(AutomSchema):
    subtitle_format: SubtitleFormat = AutomField(
        "vtt",
        description="The format of the subtitle file."
    )
    language: SubtitleLanguage = AutomField(
        "best",
        description="The language of the subtitle file."   
    )


class YouTubeSubtitleDownloadParams(AutomSchema):
    url: str = AutomField(
        ...,
        description="The URL of the YouTube video to download."
    )
    output_dir: Path = AutomField(
        ...,
        description="The directory to save the downloaded subtitle file."
    )
    subtitle_options: Optional[SubtitleOptions] = AutomField(
        None,
        description="The options for the subtitle file."
    )


class YouTubeVideoDownloadParams(AutomSchema):
    url: str = AutomField(
        ...,
        description="The URL of the YouTube video to download.",
    )
    output_dir: Path = AutomField(
        ...,
        description="The directory to save the downloaded files."
    )
    keep_subtitle: bool = AutomField(
        False,
        description="Whether to keep the subtitle file(The format can be specified in `subtitle_options`)"
    )
    subtitle_options: Optional[SubtitleOptions] = AutomField(
        None,
        description="The options for the subtitle file. Keep it `None` if `keep_subtitle` is `False`."
    )


class YouTubeSubtitleDownloadResult(AutomSchema):
    subtitle_available: bool = AutomField(
        ...,
        description="Whether the subtitle is available."
    )
    subtitle_file: Optional[Path] = AutomField(
        None,
        description="The path of the downloaded subtitle file. It is `None` if `subtitle_available` is `False`."
    )


class YouTubeVideoDownloadResult(AutomSchema):
    video_file: Path = AutomField(
        ...,
        description="The path of the downloaded video file."
    )
    subtitle_file: Optional[Path] = AutomField(
        None,
        description="The path of the downloaded subtitle file. It is `None` if `keep_subtitle` is `False`."
    )
