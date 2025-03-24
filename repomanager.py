import os
import json
import requests
import logging
from urllib.parse import urlparse
from telethon import events
from modules import owner_only
from help_registry import help_registry

logger = logging.getLogger(__name__)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "repositories.json")
MODULES_DIR = os.path.dirname(__file__)

class RepoManager:
    def __init__(self):
        self.repositories = self.load_config()

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return []
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.repositories, f, indent=2)

    def add_repo(self, url):
        if any(r['url'] == url for r in self.repositories):
            return False
        repo_name = urlparse(url).path.strip('/').split('/')[-1]
        self.repositories.append({"url": url, "name": repo_name})
        self.save_config()
        return True

repo_manager = RepoManager()

async def get_raw_url(github_url, module_name):
    parsed = urlparse(github_url)
    path_parts = parsed.path.split('/')
    user, repo = path_parts[1], path_parts[2]
    return f"https://raw.githubusercontent.com/{user}/{repo}/main/modules/{module_name}.py"

@owner_only
async def repo_handler(event):
    args = event.pattern_match.group(1)
    
    if args:
        if not args.startswith("https://github.com/"):
            await event.reply("❌ Поддерживаются только GitHub репозитории")
            return
        if repo_manager.add_repo(args):
            await event.reply(f"✅ Репозиторий добавлен: {args}")
        else:
            await event.reply("⚠️ Репозиторий уже существует в списке")
    else:
        if not repo_manager.repositories:
            await event.reply("📦 Список репозиториев пуст")
            return
        response = "📚 Список репозиториев:\n\n"
        for idx, repo in enumerate(repo_manager.repositories, 1):
            response += f"{idx}. {repo['name']} - {repo['url']}\n"
        await event.reply(response)

@owner_only
async def irepo_handler(event):
    try:
        args = event.pattern_match.group(1).split()
        if len(args) != 2:
            raise ValueError
            
        index = int(args[0]) - 1
        module_name = args[1]
        repo = repo_manager.repositories[index]
        raw_url = await get_raw_url(repo['url'], module_name)
        
        response = requests.get(raw_url)
        response.raise_for_status()
        
        module_path = os.path.join(MODULES_DIR, f"{module_name}.py")
        with open(module_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        await event.reply(f"✅ Модуль {module_name} установлен!\nПуть: {module_path}")

    except IndexError:
        await event.reply("❌ Неверный индекс репозитория")
    except requests.exceptions.RequestException:
        await event.reply("❌ Ошибка загрузки модуля с GitHub")
    except Exception as e:
        await event.reply(f"❌ Ошибка: {str(e)}")

async def register(client):
    client.add_event_handler(
        repo_handler,
        events.NewMessage(pattern=r"^\.repo(?:\s+(.+))?$")
    )
    client.add_event_handler(
        irepo_handler,
        events.NewMessage(pattern=r"^\.irepo\s+(\d+)\s+(\S+)$")
    )
    help_registry.register_command(
        ".repo [url]",
        "Добавить репозиторий или показать список"
    )
    help_registry.register_command(
        ".irepo <index> <module>",
        "Установить модуль из репозитория"
    )
