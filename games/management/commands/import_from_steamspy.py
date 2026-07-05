import time
import requests
from django.core.management.base import BaseCommand
from games.models import Game


class Command(BaseCommand):
    help = "Import top games from SteamSpy, sorted by popularity (owners)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--pages',
            type=int,
            default=10,
            help='Number of pages to fetch (1000 games per page)'
        )

    def handle(self, *args, **options):
        pages = options['pages']
        created = 0
        skipped = 0

        for page in range(pages):
            self.stdout.write(f"\n📥 Fetching page {page}...")

            url = "https://steamspy.com/api.php"
            params = {"request": "all", "page": page}
            response = requests.get(url, params=params)
            data = response.json()

            for app_id, info in data.items():
                title = info.get("name", "").strip()

                if not title:
                    continue

                if Game.objects.filter(title=title).exists():
                    skipped += 1
                    continue

                Game.objects.create(
                    title=title,
                    description="",  # SteamSpy не даёт описание, заполним позже
                    year_of_release=2000,  # тоже заполним позже через appdetails
                    genre=info.get("genre", "Unknown") or "Unknown",
                    poster_url=f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
                )
                created += 1
                self.stdout.write(f"✅ {title}")

            # обязательная задержка 60 секунд между страницами запроса "all"
            if page < pages - 1:
                self.stdout.write("⏳ Waiting 60 seconds (SteamSpy rate limit)...")
                time.sleep(60)

        self.stdout.write(f"\nГотово: создано {created}, пропущено {skipped}")