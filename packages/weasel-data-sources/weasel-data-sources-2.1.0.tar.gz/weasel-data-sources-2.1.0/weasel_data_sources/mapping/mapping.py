""" Handles the parametrization of fetchers of known data sources """

import os
import re

from weasel_data_sources.releases import CDNJSFetcher, GitFetcher

from .sources import SOURCES


class TechnologyBuilder:
    """
    A builder to create TechnologyHandler instances
    """

    def __init__(self, git_repository_storage):
        self._git_storage = git_repository_storage

    def create_technology_handler(self, technology_name: str):
        """
        Creates a technology handler instance corresponding to the given technology name
        :param technology_name: The name of the technology
        """
        if technology_name in SOURCES:
            return TechnologyHandler(technology_name, self._git_storage)

        raise ValueError('Technology "{}" is not in known data sources')

    def get_all_technologies(self) -> dict:
        """
        Returns a dict of technology handler instances for all known data sources
        """
        return {name: self.create_technology_handler(name) for name in SOURCES}


class TechnologyHandler:
    """
    Handles the different data sources that are known for a technology
    and initializes corresponding fetchers.
    """

    def __init__(self, name: str, git_base_storage: str):
        self.name = name
        self.git_repo_url = SOURCES[self.name]["git"]
        self.git_tag_regex = (
            SOURCES[self.name]["git_tag_regex"]
            if "git_tag_regex" in SOURCES[self.name]
            else None
        )
        self.git_tag_substitute = (
            SOURCES[self.name]["git_tag_substitute"]
            if "git_tag_substitute" in SOURCES[self.name]
            else None
        )
        self.cdnjs_library_name = SOURCES[self.name]["cdnjs"]
        self.local_git_path = os.path.join(git_base_storage, self.safe_name)

    @property
    def safe_name(self):
        """
        The technology name in a form that is safe to use as a file name
        """
        tmp = self.name.strip().replace(" ", "_")
        return re.sub(r"(?u)[^-\w.]", "", tmp)

    @property
    def has_git(self):
        """
        True if a git repository for this technology is given in the known data sources
        """
        return self.git_repo_url is not None

    @property
    def has_cdnjs(self):
        """
        True if a cdnjs library name for this technology is given in the known data sources
        """
        return self.cdnjs_library_name is not None

    def create_git_fetcher(self):
        """
        Initializes and returns a `GitFetcher` instance for the technology
        :raise ValueError: If their is no known git repository for this technology
        """
        if not self.has_git:
            raise ValueError("There is no known git repo for {}".format(self.name))

        return GitFetcher(
            self.git_repo_url,
            self.local_git_path,
            self.git_tag_regex,
            self.git_tag_substitute,
        )

    def create_cdnjs_fetcher(self):
        """
        Initializes and returns a `CDNJSFetcher` instance for the technology
        :raise ValueError: If their is no known cdnjs library name for this technology
        """
        if not self.has_cdnjs:
            raise ValueError("There is no known cdnjs library for {}".format(self.name))

        return CDNJSFetcher(self.cdnjs_library_name)
