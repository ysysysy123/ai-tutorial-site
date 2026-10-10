"""适配 nbconvert 的站内链接，以及本站统一加载的公式和 Mermaid。"""

import posixpath
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from mkdocs.plugins import event_priority
from mkdocs.utils import get_relative_url


@event_priority(-50)
def on_files(files, config):
    for file in files:
        if file.src_uri.endswith(".ipynb") and file.is_documentation_page():
            destination = PurePosixPath(file.src_uri).with_suffix(".notebook.html").as_posix()
            file.dest_path = destination
            file.dest_uri = destination
            file.abs_dest_path = str(Path(config["site_dir"]) / destination)
            file.url = quote(destination)
    return files


def on_page_content(html, page, config, files):
    if not page.file.src_uri.endswith(".ipynb"):
        return html
    soup = BeautifulSoup(html, "html.parser")
    for script in soup.find_all("script"):
        if (
            script.get("type") == "text/x-mathjax-config"
            or script.get("src") == ""
            or (
                script.get("type") == "module"
                and '.jp-Mermaid > pre.mermaid' in script.get_text()
            )
        ):
            script.decompose()
    for diagram in soup.select(".jp-Mermaid > pre.mermaid"):
        source = diagram.decode_contents(formatter=None)
        pre = soup.new_tag("pre", attrs={"class": "mermaid-source"})
        code = soup.new_tag("code")
        code.string = source
        pre.append(code)
        diagram.parent.replace_with(pre)
    for anchor in soup.find_all("a", href=True):
        link = urlsplit(anchor["href"])
        if link.scheme or link.netloc or not link.path:
            continue
        source_path = posixpath.normpath(posixpath.join(
            posixpath.dirname(page.file.src_uri), unquote(link.path)
        ))
        target = files.get_file_from_path(source_path)
        if target and target.is_documentation_page():
            path = get_relative_url(target.url, page.file.url)
            anchor["href"] = urlunsplit(("", "", path, link.query, link.fragment))
    return str(soup)
