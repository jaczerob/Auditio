from concurrent.futures import ThreadPoolExecutor

from track import Track


class Player:
    def __init__(self, executor: ThreadPoolExecutor) -> None:
        self.current_track: Track = None
        self.__previous_track: Track = None

        self.executor = executor

    async def update(self) -> None:
        current_track = self.current_track
        self.__previous_track = current_track

        self.current_track = Track(self.executor)
        await self.current_track.parse()

        if self.__previous_track is None:
            return

        if self.current_track != self.__previous_track:
            await self.__previous_track.delete()