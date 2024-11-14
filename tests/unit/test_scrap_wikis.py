import pytest

from mush_wikis_scraper.adapters.file_system_page_reader import FileSystemPageReader
from mush_wikis_scraper.usecases.scrap_wikis import ScrapWikis


@pytest.mark.parametrize(
    "page_data",
    [
        {
            "title": "Game Basics",
            "link": "tests/data/mushpedia.com/Game Basics",
            "source": "Mushpedia",
            "content": "There are two teams of players on the ship. Humans who are trying to save Humanity",
        },
        {
            "title": "Human Play",
            "link": "tests/data/mushpedia.com/Human Play",
            "source": "Mushpedia",
            "content": "Figure out what your character's role is and do it.",
        },
        {
            "title": "Personnages - Pnj",
            "link": "tests/data/twin.tithom.fr/mush/personnages/pnj",
            "source": "Twinpedia",
            "content": "NERON est l'intelligence artifcielle de bord, sa puissance de calcul est indispensable à l'opération du PILGRED.",
        },
        {
            "title": "Pilgred",
            "link": "tests/data/twin.tithom.fr/mush/pilgred",
            "source": "Twinpedia",
            "content": "Si la réparation du PILGRED est complétée avant la décryogénisation de tous, il est possible de rentrer sur Sol. Aucun point de triomphe n'est perdu pour le retour sur Sol avant la désignation des Mush, puisqu'il n'y a techniquement aucun membre Mush à bord du Daedalus, à ce moment.",
        },
    ],
)
def test_execute(page_data) -> None:
    # given I have page links
    page_links = [page_data["link"]]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = scraper.execute(page_links)

    # then I should get the pages content
    page = pages[0]
    assert list(page.keys()) == ["title", "link", "source", "content"]
    assert page["title"] == page_data["title"]
    assert page["link"] == page_data["link"]
    assert page["source"] == page_data["source"]
    assert page_data["content"] in page["content"]


@pytest.mark.parametrize(
    "format",
    ["html"],
)
def test_remove_line_breaks(format: str) -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = scraper.execute(page_links, format=format)

    # then I should get the pages content without line breaks
    assert pages[0]["content"].count("\n") == 0


def test_execute_with_html_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = scraper.execute(page_links, format="html")

    # then I should get the pages content in HTML format
    assert pages[0]["content"].startswith("<!DOCTYPE html>")


def test_execute_with_text_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = scraper.execute(page_links, format="text")

    # then I should get the pages content without HTML tags
    assert "<!DOCTYPE html>" not in pages[0]["content"]


def test_execute_with_markdown_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    pages = scraper.execute(page_links, format="markdown")

    # then I should get the pages content in Markdown format
    assert "Game Basics\n===========" in pages[0]["content"]


def test_execute_with_unknown_format() -> None:
    # given I have page links
    page_links = ["tests/data/mushpedia.com/Game Basics"]

    # when I run the scraper
    scraper = ScrapWikis(FileSystemPageReader())
    with pytest.raises(ValueError):
        scraper.execute(page_links, format="unknown")
