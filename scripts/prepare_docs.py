"""根据上游目录生成导航；教程原文和图片保留在 _source。"""

from pathlib import Path
import re

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_source"


def entries(directory):
    result = []
    overview = directory / "README.md"
    if overview.is_file():
        result.append({"概览": overview.relative_to(SOURCE).as_posix()})
    for path in sorted(directory.iterdir(), key=lambda p: p.name):
        if path.name.startswith(".") or path == overview:
            continue
        if path.is_dir():
            children = entries(path)
            if children:
                result.append({path.name: children})
        elif path.suffix in {".md", ".ipynb"}:
            label = path.stem
            if path.suffix == ".ipynb" and path.with_suffix(".md").is_file():
                label += "（Notebook）"
            result.append({label: path.relative_to(SOURCE).as_posix()})
    return result


def main():
    nav = [{"首页": "README.md"}]
    if (SOURCE / "ROADMAP.md").is_file():
        nav.append({"学习路线": "ROADMAP.md"})
    modules = sorted(
        p for p in SOURCE.iterdir()
        if p.is_dir() and re.match(r"^\d{2}-", p.name)
    )
    for module in modules:
        nav.append({module.name: entries(module)})
    notes = [
        {p.stem: p.name} for p in sorted(SOURCE.glob("*.md"))
        if p.name not in {"README.md", "ROADMAP.md"}
    ]
    if notes:
        nav.append({"仓库说明": notes})
    config = {"INHERIT": "mkdocs.yml", "nav": nav}
    (ROOT / "mkdocs.generated.yml").write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    notebooks = len(list(SOURCE.rglob("*.ipynb")))
    print(f"已生成导航：{len(modules)} 个模块、{notebooks} 篇 Notebook。")


if __name__ == "__main__":
    main()
