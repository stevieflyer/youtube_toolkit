from pathlib import Path
from typing import Optional

import yt_dlp

from .schema import SubtitleOptions, YouTubeVideoDownloadResult, YouTubeSubtitleDownloadResult

def download_youtube_video(
    url: str,
    keep_subtitle: bool = False,
    subtitle_options: Optional[SubtitleOptions] = None,
    output_dir: Path = Path('.')
) -> YouTubeVideoDownloadResult:
    """Download a YouTube video. If `keep_subtitle` is `True`, the subtitle file will also be downloaded.

    Args:
        url (str): The URL of the YouTube video to download.
        keep_subtitle (bool, optional): Whether to keep the subtitle file (the format can be specified in `subtitle_options`). Defaults to False.
        subtitle_options (Optional[SubtitleOptions], optional): The options for the subtitle file. Keep it `None` if `keep_subtitle` is `False`. Defaults to None.
        output_dir (Path, optional): The directory to save the downloaded files. Defaults to the current directory.
    """
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
        'writesubtitles': keep_subtitle,
        'subtitlesformat': subtitle_options.subtitle_format if keep_subtitle and subtitle_options else 'best',
        'merge_output_format': 'mp4',
        'keepvideo': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as video:
        info_dict = video.extract_info(url, download=True)
        video_title: str = info_dict['title']
        print(f"Successfully Downloaded: {video_title}")

        # 生成文件路径
        video_file = output_dir / f"{video_title}.mp4"
        subtitle_file = output_dir / f"{video_title}.{subtitle_options.subtitle_format}" if keep_subtitle and subtitle_options else None

        # 删除 .webm 文件
        webm_file = output_dir / f"{video_title}.webm"
        if webm_file.exists():
            webm_file.unlink()  # 删除 .webm 文件

    return YouTubeVideoDownloadResult(
        video_file=video_file,
        subtitle_file=subtitle_file,
    )


def download_youtube_subtitle(
    url: str,
    output_dir: Path = Path('.'),
    subtitle_options: Optional[SubtitleOptions] = None,
) -> YouTubeSubtitleDownloadResult:
    """Download the subtitle of a YouTube video.

    Args:
        url (str): The URL of the YouTube video to download.
        output_dir (Path, optional): The directory to save the downloaded subtitle file. Defaults to the current directory.
        subtitle_options (Optional[SubtitleOptions], optional): The options for the subtitle file. Defaults to None.
    """
    if subtitle_options is None:
        subtitle_options = SubtitleOptions()
    ydl_opts = {
        'writesubtitles': True,
        'subtitlesformat': subtitle_options.subtitle_format if subtitle_options else 'best',
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as video:
        info_dict = video.extract_info(url, download=False)
        video_title: str = info_dict['title']
        print(f"Successfully Downloaded: {video_title}")

        subtitle_file = output_dir / f"{video_title}.{subtitle_options.subtitle_format}" if subtitle_options else None

    return YouTubeSubtitleDownloadResult(
        subtitle_available=subtitle_file is not None,
        subtitle_file=subtitle_file,
    )
