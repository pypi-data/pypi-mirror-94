

from libreflow.baseflow.runners import DefaultRunners, CHOICES, CHOICES_ICONS


CHOICES.append("wav")
CHOICES.append("ai")
CHOICES_ICONS["wav"] = ("icons.gui", "youtube-logo")
CHOICES_ICONS["ai"] = ("icons.gui", "picture")



class DefaultRunners(DefaultRunners):
    def mapped_names(self, page_num=0, page_size=None):
        return CHOICES
