import os
import json
import requests
import logging
from urllib.parse import urlparse
from telethon import events
from help_registry import help_registry
from modules import owner_only

logger = logging.getLogger(__name__)
CONFIG_FILE = "repositories.json"
MODULES_DIR = "modules"

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
        self.repositories.append({
            "url": url,
            "name": repo_name
        })
        self.save_config()
        return True

repo_manager = RepoManager()

async def get_raw_url(github_url, module_name):
    parsed = urlparse(github_url)
    path_parts = parsed.path.split('/')
    user, repo = path_parts[1], path_parts[2]
    return f"https://raw.githubusercontent.com/{user}/{repo}/main/{module_name}.py"

@owner_only
async def repo_handler(event):
    args = event.pattern_match.group(1)
    if args:
        if not args.startswith("https://github.com/"):
            await event.edit("❌ Только GitHub репозитории поддерживаются")
            return
            
        if repo_manager.add_repo(args):
            await event.edit(f"✅ Репозиторий добавлен: {args}")
        else:
            await event.edit("⚠️ Репозиторий уже существует в списке")
    else:
        if not repo_manager.repositories:
            await event.edit("📦 Список репозиториев пуст")
            return
            
        response = "📚 Список репозиториев:\n\n"
        for idx, repo in enumerate(repo_manager.repositories, 1):
            response += f"{idx}. {repo['name']} - {repo['url']}\n"
        
        await event.edit(response)

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
        
        os.makedirs(MODULES_DIR, exist_ok=True)
        with open(os.path.join(MODULES_DIR, f"{module_name}.py"), "w") as f:
            f.write(response.text)
            
        await event.edit(f"✅ Модуль {module_name} установлен из {repo['name']}")

    except IndexError:
        await event.edit("❌ Неверный индекс репозитория")
    except Exception as e:
        await event.edit(f"❌ Ошибка: {str(e)}")

async def register(client):
    client.add_event_handler(
        repo_handler,
        events.NewMessage(pattern=r"^\.repo(?:\s+(.+)|$")
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
