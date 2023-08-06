"""Module for declaring list of tracker proxies."""
import abc
import asyncio
import logging

import bs4

from mariner import exceptions, mixins

Url = str


class ProxyMeta(abc.ABCMeta, type):
    """Metaclass to check that ProxyList plugins override proxy_page_url."""

    def __new__(cls, name, bases, namespace, **kwargs):
        if abc.ABC not in bases:
            if not namespace.get("default_proxy"):
                raise exceptions.PluginError("You must define default_proxy")
            if not namespace.get("proxy_page_url"):
                raise exceptions.PluginError("You must define proxy_page_url")
        return type.__new__(cls, name, bases, namespace)


class ProxyPlugin(mixins.RequestMixin, abc.ABC, metaclass=ProxyMeta):
    """Get a list of proxies for given website."""

    log = logging.getLogger(__name__)
    default_proxy = ""  # To be overwritten by subclasses
    proxy_page_url = ""  # To be overwritten by subclasses

    async def get_proxy(self) -> Url:
        """Return the first working proxy.

        Returns:
            The first working proxy.
        """
        self.log.debug("Getting list of proxies.")
        try:
            proxy_page = await self.get(self.proxy_page_url)
            return self._parse(proxy_page)
        except (OSError, asyncio.TimeoutError, exceptions.NoProxyAvailable):
            return self.default_proxy

    @staticmethod
    @abc.abstractmethod
    def _parse(page: str) -> str:
        """Parse proxy page a yield a proxies.

        Args:
            page: Page with a list of proxies.

        Returns:
            A Proxy URL.
        """
        raise NotImplementedError

    @staticmethod
    @abc.abstractmethod
    def _is_online(soup: bs4.Tag) -> bool:
        """Check if listed proxy is online.

        Args:
            soup: BeautifulSoup for given proxy.

        Returns:
            True if site is listed online.
        """
        raise NotImplementedError
