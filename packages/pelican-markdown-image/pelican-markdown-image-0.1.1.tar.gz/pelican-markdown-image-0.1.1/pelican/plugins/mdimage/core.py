import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup
from pelican.contents import Article

from pelican import signals

logger = logging.getLogger(__name__)


def test2(article_generator):
    for article in article_generator.articles:
        content_path = Path(article_generator.path)
        source_path = Path(article.source_path)
        if content_path != source_path.parent:
            # if a article resides in /contents/some_sub_dir,
            # we need to update the relative path (add a prefix)
            prefix = source_path.parent.relative_to(content_path)
            logger.warning(f'adding prefix "{prefix}" to src of img of "{source_path}"')
            soup = BeautifulSoup(article.content, "html.parser")
            for img in soup.find_all('img'):
                img['src'] = str(prefix / img['src'])
            article._content = str(soup)

            # FIXME: this is dirty...
            class _Article(Article):
                @property
                def content(self):
                    content = self._content
                    return self._update_content(content, self.get_siteurl())

            article.__class__ = _Article

        static_links = set()
        img = re.compile(r'<img.*src="(.*)">')
        for res in img.finditer(article.content):
            img_relative_path = Path(res[1])
            path = source_path.parent / img_relative_path
            static_links.add(path)
        article_generator.context['static_links'] |= static_links


def register():
    signals.article_generator_pretaxonomy.connect(test2)
