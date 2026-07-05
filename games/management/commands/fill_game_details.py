import re
import time
import requests
from django.core.management.base import BaseCommand
from games.models import Game


class Command(BaseCommand):
    help = "Fill missing description, genre and year using Steam appdetails"

    def handle(self, *args, **options):
        games = Game.objects.filter(genre="Unknown")
        total = games.count()
        updated = 0
        failed = 0

        for game in games:
            if not game.poster_url:
                failed += 1
                continue

            # вытаскиваем App ID из URL постера
            match = re.search(r"/apps/(\d+)/", game.poster_url)
            if not match:
                failed += 1
                continue

            app_id = match.group(1)

            url = "https://store.steampowered.com/api/appdetails"
            params = {"appids": app_id}
            response = requests.get(url, params=params)
            data = response.json()

            app_data = data.get(str(app_id), {})

            if not app_data.get("success"):
                self.stdout.write(f"❌ No data: {game.title}")
                failed += 1
                time.sleep(1)
                continue

            details = app_data["data"]

            game.description = details.get("short_description", "")

            genres = details.get("genres", [])
            if genres:
                game.genre = genres[0]["description"]

            release_date = details.get("release_date", {}).get("date", "")
            year_match = re.search(r"\d{4}", release_date)
            if year_match:
                game.year_of_release = int(year_match.group())

            # если постера не было — заполним и его
            if not game.poster_url or "header.jpg" not in game.poster_url:
                game.poster_url = details.get("header_image", game.poster_url)

            game.save()
            self.stdout.write(f"✅ {game.title}")
            updated += 1

            time.sleep(1)  # ограничение скорости запросов к Steam

        self.stdout.write(f"\nГотово: обновлено {updated}, не удалось {failed} из {total}")