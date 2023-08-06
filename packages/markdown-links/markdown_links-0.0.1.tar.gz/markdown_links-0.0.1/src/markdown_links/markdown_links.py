import os
import re
from pathlib import Path
from re import Pattern
from typing import Optional, List
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from uuid import uuid4

from markdown import Markdown
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor, NOIMG
from markdown.treeprocessors import Treeprocessor


class MarkdownLinks(Extension):

    _link_pattern = NOIMG + r'\[(.*?)\](\+?)\((.+?)\)(\+?(?:(.+?)\+)?)(?:{(.+?)})?([<>](\d+)?)?'

    def extendMarkdown(self, md: Markdown):
        md.inlinePatterns.register(_InlineProcessor(self._link_pattern, md), 'markdown_links_inline_processor', 165)
        md.treeprocessors.register(_TreeProcessor(), 'markdown_links_tree_processor', 15)


class _InlineProcessor(InlineProcessor):

    _markdown_title_pattern: Pattern = re.compile(r'^(#+)\s*(\S.*)$')
    _markdown_primer_pattern: Pattern = re.compile(r'^(\w.*?(?:[.!?]|$))')
    _excerpt_depth_attribute = 'data-markdown-links-excerpt-depth'
    _excerpt_importance_attribute = 'data-markdown-links-excerpt-importance'

    def handleMatch(self, m, data):

        href: str = m.group(3)

        # filter out non-markdown-file hrefs
        if not href.endswith('.md') and not href.endswith('.mkd'):  # TODO add more common extensions
            return None, None, None

        # filter non-relative hrefs
        if not _is_relative_path(href):
            return None, None, None

        document_path: Path = Path() / href
        custom_title: Optional[str] = m.group(1)
        composite_title: str = m.group(2)
        custom_primer: Optional[str] = m.group(5)
        include_primer: bool = len(m.group(4)) > 0
        include_excerpt: Optional[str] = m.group(6)
        document_title: Optional[str] = None
        document_primer: Optional[str] = None
        document_excerpt_lines: List[str] = []
        document_excerpt_control: Optional[str] = m.group(7)
        document_excerpt_importance: int = m.group(8) if m.group(8) else '0'

        with document_path.open() as file:

            for line in file:
                title_match = self._markdown_title_pattern.match(line)
                if title_match:
                    title_level = len(title_match.group(1))
                    if title_level == 1:
                        document_title = title_match.group(2)
                        break

            if include_primer and not custom_primer:
                for line in file:
                    primer_match = self._markdown_primer_pattern.match(line)
                    if primer_match:
                        document_primer = primer_match.group(1)
                        break

        if include_excerpt:
            with document_path.open() as file:
                for line in file:
                    title_match = self._markdown_title_pattern.match(line)
                    if title_match and title_match.group(2) == include_excerpt:
                        for excerpt_line in file:
                            title_match = self._markdown_title_pattern.match(excerpt_line)
                            if title_match:
                                break
                            document_excerpt_lines.append(excerpt_line)

        result = Element('markdown_links_container')

        anchor = Element('a')
        anchor.set('href', href)
        result.append(anchor)
        if custom_title and document_title and composite_title:
            span = Element('span')
            span.text = custom_title
            span.tail = ' '
            anchor.append(span)
            span = Element('span')
            span.text = f'({document_title})'
            anchor.append(span)
        else:
            anchor.text = custom_title or document_title or document_path.name

        if include_primer:
            primer = custom_primer or document_primer
            if primer:
                span = Element('span')
                span.text = ': ' + primer
                result.append(span)

        if document_excerpt_lines:

            if document_excerpt_control:

                checkbox = Element('input')
                checkbox.attrib['class'] = 'markdown_links_excerpt_control'
                checkbox.attrib['type'] = 'checkbox'
                checkbox.attrib[self._excerpt_depth_attribute] = '0'
                checkbox.attrib[self._excerpt_importance_attribute] = document_excerpt_importance
                result.append(checkbox)

                if document_excerpt_importance != '0':
                    checkbox.attrib['checked'] = 'checked'

                if document_excerpt_control.startswith('<'):
                    uuid = str(uuid4())
                    checkbox.attrib['id'] = uuid
                    checkbox.attrib['class'] += ' hidden'
                    label = Element('label')
                    label.attrib['class'] = 'markdown_links_excerpt_control_label'
                    label.attrib['for'] = uuid
                    result.insert(0, label)

            return_dir = os.getcwd()
            os.chdir(document_path.parent)

            element_tree = ElementTree.fromstring(self.md.convert(''.join(document_excerpt_lines)))
            element_tree.attrib['class'] = 'markdown_links_excerpt'
            for element in _recurse(element_tree):
                _fix_attribute_relative_path(element, 'href', return_dir)
                _fix_attribute_relative_path(element, 'src', return_dir)
                excerpt_depth = int(element.attrib.get(self._excerpt_depth_attribute, -1))
                if excerpt_depth > -1:
                    excerpt_depth += 1
                    element.attrib[self._excerpt_depth_attribute] = str(excerpt_depth)
                    excerpt_importance = int(element.attrib[self._excerpt_importance_attribute])
                    if excerpt_importance > excerpt_depth:
                        element.attrib['checked'] = 'checked'
                    else:
                        element.attrib.pop('checked', None)
            result.append(element_tree)

            os.chdir(return_dir)

        return result, m.start(0), m.end(0)


class _TreeProcessor(Treeprocessor):
    def run(self, root: ElementTree):
        for element in _recurse(root):
            i = 0
            while i < len(element):
                child = element[i]
                if child.tag == 'markdown_links_container':
                    del element[i]
                    for transfer_child in child:
                        element.insert(i, transfer_child)
                        i += 1
                else:
                    i += 1


def _recurse(element_tree: ElementTree):
    yield element_tree
    for child in element_tree:
        yield from _recurse(child)


def _fix_attribute_relative_path(element: Element, attribute: str, anchor_path):
    value = element.attrib.get(attribute, None)
    if _is_relative_path(value):
        element.attrib[attribute] = os.path.relpath(value, anchor_path)


def _is_relative_path(path: Optional[str]) -> bool:
    # filter out urls and references to root
    if not path or '//' in path or os.path.isabs(path):
        return False
    return True


def makeExtension(**kwargs):
    return MarkdownLinks(**kwargs)
