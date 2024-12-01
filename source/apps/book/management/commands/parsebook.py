import asyncio
import random
import sys

import aiohttp
from alive_progress import alive_bar
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from book.models import Author, Book


def get_key_press():
    if sys.platform.startswith("win"):
        import msvcrt

        return msvcrt.getch().decode("utf-8").lower()
    else:
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.lower()


def get_yes_no_choice(prompt):
    print(prompt + " (д/н): ", end="", flush=True)
    while True:
        key = get_key_press()
        if key in ["д", "y", "н", "n"]:
            print(key)
            return key in ["д", "y"]


class Command(BaseCommand):
    help = "Парсит книги и заполняет базу данных"

    async def fetch(self, session, url, max_retries=3, timeout=5):
        for attempt in range(max_retries):
            try:
                # proxy = 'http://217.196.97.212:1111'
                proxy = None
                async with session.get(
                    url, timeout=aiohttp.ClientTimeout(total=timeout), proxy=proxy
                ) as response:
                    return await response.text()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if attempt == max_retries - 1:
                    self.stdout.write(
                        self.style.ERROR(f"Ошибка при запросе {url}: {str(e)}")
                    )
                    return None
                await asyncio.sleep(2**attempt)

    @sync_to_async
    def create_author_entry(self, author_name):
        author, _ = Author.objects.get_or_create(name=author_name)
        return author

    @sync_to_async
    def create_book_entry(self, book_info):
        book = Book(
            title=book_info["title"],
            author=book_info["author"],
            genre=book_info.get("genre", []),
            tags=book_info.get("tags", []),
            publisher=book_info.get("publisher"),
            image=book_info.get("image"),
            annotation=book_info.get("annotation"),
            price=book_info.get("price", 0.00),
        )
        book.save()

    async def parse_book_page(self, session, url):
        response_text = await self.fetch(session, url)
        soup = BeautifulSoup(response_text, "html.parser")

        book_info = {}

        item_info = soup.find("div", class_="item_info item_title")

        if item_info:
            title_elem = item_info.find("h1")
            book_info["title"] = (
                title_elem.text.strip() if title_elem else "Название не найдено"
            )

            author_elem = item_info.find("a")
            author_name = author_elem.text.strip() if author_elem else "Автор не указан"

            book_info["author"] = await self.create_author_entry(author_name)

        else:
            book_info["title"] = "Название не найдено"
            book_info["author"] = None

        info_blocks = soup.find_all("div", class_="item_info border_bottom mob")

        for block in info_blocks:
            header = block.find(class_="h2")
            if header:
                header_text = header.text

                if "Жанр" in header_text:
                    elements = [
                        ell.get_text() for ell in block.children if ell.name == "a"
                    ]
                    book_info["genre"] = elements if elements else "Жанр не указан"
                elif "Метк" in header_text:
                    tags = [ell.get_text() for ell in block.children if ell.name == "a"]
                    book_info["tags"] = tags
                elif "Издательств" in header_text:
                    elements = [ell.get_text() for ell in block.children][1]
                    book_info["publisher"] = (
                        elements if elements else "Издательство не указано"
                    )

        cwr_images = soup.find_all("img", class_="cwr")
        if len(cwr_images) >= 2:
            book_info["image"] = cwr_images[1]["src"]
        else:
            book_info["image"] = "Второе изображение с классом cwr не найдено"

        annotation_elem = soup.find("div", class_="annotation")
        if annotation_elem:
            annotation = annotation_elem.text.strip().replace("\t", " ")

            annotation = " ".join(annotation.split())
            split_annotation = annotation.split("В нашей электронной библиотеке")

            book_info["annotation"] = split_annotation[0].strip()
            if not split_annotation[0].strip():
                book_info["annotation"] = "Аннотация отсутствует"

        book_info["price"] = self.generate_random_price()

        return book_info

    def generate_random_price(self):
        return random.randint(50, 249) * 10 + 9

    async def parse_page(self, session, url):
        response_text = await self.fetch(session, url)
        property(response_text)
        soup = BeautifulSoup(response_text, "html.parser")

        book_links = []

        for li in soup.find_all("li"):
            wrap = li.find("div", class_="wrap")
            if wrap:
                img = wrap.find("div", class_="img")
                if img:
                    link = img.find("a")
                    if link and "href" in link.attrs:
                        book_links.append(f"https://aldebaran.ru{link['href']}")

        return book_links

    async def parse_and_save_multiple_pages(self, base_url, num_pages):
        async with aiohttp.ClientSession() as session:
            try:
                pages = list(range(1, num_pages + 1))

                # Перемешиваем список
                # random.shuffle(pages)
                for page in pages:
                    if page == 1:
                        url = base_url
                    else:
                        url = f"{base_url}pagenum-{page}/"

                    self.stdout.write(f"Парсинг страницы {page}/{num_pages}: {url}")

                    book_links = await self.parse_page(session, url)

                    if book_links:
                        with alive_bar(
                            len(book_links), title="Парсинг книг", bar="blocks"
                        ) as bar_books:
                            tasks = [
                                self.parse_book_page(session, book_link)
                                for book_link in book_links
                            ]
                            for book_info in await asyncio.gather(*tasks):
                                if book_info:
                                    await self.create_book_entry(book_info)
                                bar_books()
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Не удалось получить ссылки на книги со страницы {url}"
                            )
                        )

            except KeyboardInterrupt:
                print("\nПарсинг прерван пользователем.")

    def add_arguments(self, parser):
        parser.add_argument("-n", "--num", type=int, help="Кол-во страниц для парсинга")

    def handle(self, *args, **options):
        base_url = "https://aldebaran.ru/knigi/"
        num_pages = options["num"]
        if num_pages is None:
            num_pages = 20
        print(f"Кол-во страниц : {num_pages}")
        if get_yes_no_choice("Продолжить?"):
            asyncio.run(self.parse_and_save_multiple_pages(base_url, num_pages))
        else:
            exit()
