class Episode:
    def __init__(self, internal_episode):
        self.internal_episode = internal_episode

    def get_url(self):
        return self.__validate_episode() and self.__get_mp3_link()

    def get_title(self):
        return self.internal_episode.title

    def get_summary(self):
        return self.internal_episode.summary

    def get_published(self):
        return self.internal_episode.published

    def __validate_episode(self):
        return bool(self.internal_episode.enclosures)

    def __get_mp3_link(self):
        if self.__validate_episode():
            links = [enclosure.href for enclosure in self.internal_episode.enclosures if enclosure.type == u'audio/mpeg']
            if not links:
                return None
            else:
                return links[0]
        else:
            return None
