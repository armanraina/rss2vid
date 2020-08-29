class Response:
    def __init__(self, total_episodes: int, episodes_skipped: int, messages: []):
        self.total_episodes = total_episodes
        self.episodes_skipped = episodes_skipped
        self.messages = messages

    def skip_episode(self, message: str):
        self.episodes_skipped += 1
        self.messages.append(message)

    def fail(self, message: str):
        self.episodes_skipped = self.total_episodes
        self.messages.append(message)

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.total_episodes!r}, '
                f'{self.episodes_skipped!r}, '
                f'{self.messages!r})')
