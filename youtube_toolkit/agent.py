from autom import AgentWorker, Request, Response, AutomSchema, autom_registry

from .utils import download_youtube_video, download_youtube_subtitle
from .schema import YouTubeVideoDownloadParams, YouTubeVideoDownloadResult, YouTubeSubtitleDownloadParams, YouTubeSubtitleDownloadResult


@autom_registry(is_internal=False)
class YouTubeVideoDownloader(AgentWorker):
    """Download a YouTube video with one click!

    Subtitle can also be downloaded if needed.
    """
    @classmethod
    def define_name(cls) -> str:
        return "YouTube Video Downloader"

    @classmethod
    def define_input_schema(cls) -> AutomSchema | None:
        return YouTubeVideoDownloadParams

    @classmethod
    def define_output_schema(cls) -> AutomSchema | None:
        return YouTubeVideoDownloadResult

    def invoke(self, req: Request) -> Response:
        req_body: YouTubeVideoDownloadParams = req.body
  
        req_body.output_dir.mkdir(parents=True, exist_ok=True)      
        resp_body = download_youtube_video(
            url=req_body.url,
            output_dir=req_body.output_dir,
            keep_subtitle=req_body.keep_subtitle,
            subtitle_options=req_body.subtitle_options,
        )
        return Response[YouTubeVideoDownloadResult].from_worker(self).success(body=resp_body)


@autom_registry(is_internal=False)
class YouTubeSubtitleDownloader(AgentWorker):
    """Download the subtitle of a YouTube video."""
    @classmethod
    def define_name(cls) -> str:
        return "YouTube Subtitle Downloader"

    @classmethod
    def define_input_schema(cls) -> AutomSchema | None:
        return YouTubeSubtitleDownloadParams

    @classmethod
    def define_output_schema(cls) -> AutomSchema | None:
        return YouTubeSubtitleDownloadResult

    def invoke(self, req: Request) -> Response:
        req_body: YouTubeSubtitleDownloadParams = req.body

        req_body.output_dir.mkdir(parents=True, exist_ok=True)
        resp_body = download_youtube_subtitle(
            url=req_body.url,
            output_dir=req_body.output_dir,
            subtitle_options=req_body.subtitle_options,
        )
        return Response[YouTubeSubtitleDownloadResult].from_worker(self).success(
            body=resp_body,
        )


__all__ = [
    "YouTubeVideoDownloader",
]
