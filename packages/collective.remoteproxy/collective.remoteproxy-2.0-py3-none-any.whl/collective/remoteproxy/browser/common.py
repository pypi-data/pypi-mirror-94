from ..remoteproxy import get_content
from plone.tiles.tile import Tile
from plone.uuid.interfaces import IUUID
from Products.Five.browser import BrowserView
from urllib import parse
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class RemoteProxyBaseView:

    templatename = None
    content = None

    def __call__(self, *args, **kwargs):

        url = self.context.remote_url

        # url_parts[2] .. path
        # url_parts[4] .. query string
        url_parts = list(parse.urlparse(url))

        # Update path
        subpath = self.request.get(
            "collective.remoteproxy__subpath", getattr(self, "subpath", [])
        )
        if subpath:
            url_parts[2] = "/".join([url_parts[2].rstrip("/")] + subpath)

        # Update query string
        query = dict(parse.parse_qsl(url_parts[4]))
        query.update(self.request.form)
        url_parts[4] = parse.urlencode(query)

        url = parse.urlunparse(url_parts)

        cookies = self.request.cookies if self.context.send_cookies else None

        self.content, content_type = get_content(
            remote_url=url,
            content_selector=getattr(self.context, "content_selector", None),
            keep_scripts=getattr(self.context, "keep_scripts", False),
            keep_styles=getattr(self.context, "keep_styles", False),
            extra_replacements=getattr(
                self.context, "extra_replacements", None
            ),  # noqa
            auth_user=getattr(self.context, "auth_user", None),
            auth_pass=getattr(self.context, "auth_pass", None),
            cookies=cookies,
            cache_time=getattr(self.context, "cache_time", 3600),
            standalone=IUUID(self.context)
            if getattr(self.context, "standalone", False)
            else None,  # noqa
        )

        if "text/html" not in content_type:
            self.request.response.setHeader("Content-type", content_type)
            return self.content

        return self.index(*args, **kwargs)


@implementer(IPublishTraverse)
class RemoteProxyView(RemoteProxyBaseView, BrowserView):
    def publishTraverse(self, request, name):
        """Subpath traverser"""
        if getattr(self, "subpath", None) is None:
            self.subpath = []
        self.subpath.append(name)
        return self


class RemoteProxyTile(RemoteProxyBaseView, Tile):
    pass
