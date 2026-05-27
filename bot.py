import asyncio
from mcrcon import MCRcon
import time
import sys
import os

# ===== НАСТРОЙКИ ПОДКЛЮЧЕНИЯ =====
RCON_HOST = "botcreatortest.aternos.me"
RCON_PORT = 25575
RCON_PASSWORD = os.environ.get("RCON_PASSWORD", "твой_пароль")
# =================================

# ===== ВСЕ РАНГИ HYPEMCPRO =====
RANKS = {
    "Премиум": {
        "prefix": "&e[Премиум] &6",
        "permissions": [
            "essentials.kit.premium", "essentials.fly", "essentials.god",
            "essentials.heal", "essentials.feed", "essentials.repair",
            "essentials.workbench", "essentials.enderchest", "essentials.hat",
            "essentials.back", "essentials.tptoggle"
        ],
        "homes": 3
    },
    "Креатив": {
        "prefix": "&b[Креатив] &3",
        "permissions": [
            "minecraft.command.gamemode", "essentials.ptime", "essentials.near",
            "essentials.hdb", "essentials.bn"
        ],
        "homes": 5
    },
    "Модер": {
        "prefix": "&a[Модер] &2",
        "permissions": [
            "essentials.vanish", "essentials.tp", "essentials.tphere",
            "essentials.time", "essentials.weather", "essentials.fireball",
            "essentials.more", "essentials.jump"
        ],
        "homes": 7
    },
    "Админ": {
        "prefix": "&4[Админ] &c",
        "permissions": [
            "essentials.give", "essentials.burn", "essentials.heal.other",
            "essentials.feed.other", "essentials.setwarp", "essentials.delwarp"
        ],
        "homes": 10
    },
    "Лорд": {
        "prefix": "&5[Лорд] &d",
        "permissions": [
            "essentials.book", "essentials.potion", "essentials.firework",
            "essentials.skull", "essentials.enchant", "essentials.thor"
        ],
        "homes": 15
    },
    "Гл.Админ": {
        "prefix": "&c[Гл.Админ] &4",
        "permissions": [
            "essentials.kick", "essentials.warn", "essentials.unwarn",
            "essentials.mute", "essentials.unmute", "essentials.seen",
            "essentials.flyspeed", "essentials.walkspeed"
        ],
        "homes": 20
    },
    "Создатель": {
        "prefix": "&6[Создатель] &e",
        "permissions": [
            "worldedit.*", "essentials.ban", "essentials.unban",
            "essentials.invsee", "essentials.endersee", "essentials.fly.other",
            "essentials.whois"
        ],
        "homes": 25
    },
    "Hype": {
        "prefix": "&d[Hype] &5",
        "permissions": [
            "essentials.nickname", "essentials.speed", "essentials.repair.all",
            "essentials.kit.hype"
        ],
        "homes": 5
    },
    "Staff": {
        "prefix": "&3[Staff] &b",
        "permissions": [
            "essentials.staffchat", "essentials.freeze", "essentials.vanish",
            "essentials.tp", "essentials.kick"
        ],
        "homes": 10
    },
    "Helper": {
        "prefix": "&9[Helper] &b",
        "permissions": [
            "essentials.helpop", "essentials.rules", "essentials.warn",
            "essentials.mute", "essentials.kick"
        ],
        "homes": 5
    },
    "Server": {
        "prefix": "&6[Server] &e",
        "permissions": [
            "essentials.clearchat", "essentials.ping", "essentials.tps",
            "essentials.gc", "essentials.restart"
        ],
        "homes": 10
    },
    "Sponsor": {
        "prefix": "&e[Sponsor] &6",
        "permissions": [
            "essentials.fly", "essentials.kit.sponsor", "essentials.nickname",
            "essentials.hat"
        ],
        "homes": 5
    },
    "Leader": {
        "prefix": "&4[Leader] &c",
        "permissions": ["*"],
        "homes": 50
    }
}
# =================================

def send_cmd(mcr, command, delay=0.5):
    print(f"[RCON] {command}")
    try:
        resp = mcr.command(command)
        if resp:
            print(f"Ответ: {resp[:200]}")
    except Exception as e:
        print(f"Ошибка: {e}")
    time.sleep(delay)

async def main():
    print("="*50)
    print("🚀 ЗАПУСК НАСТРОЙКИ СЕРВЕРА")
    print("="*50)
    print(f"🔌 Подключение к {RCON_HOST}:{RCON_PORT}...")
    
    try:
        with MCRcon(RCON_HOST, RCON_PASSWORD, port=RCON_PORT) as mcr:
            print("✅ ПОДКЛЮЧЕНО К RCON!")
            
            # 1. Проверка
            print("\n📦 ШАГ 1: Проверка сервера...")
            send_cmd(mcr, "version")
            
            # 2. Создание рангов
            print("\n👑 ШАГ 2: Создание рангов...")
            for rank, data in RANKS.items():
                send_cmd(mcr, f"lp creategroup {rank}")
                send_cmd(mcr, f"lp group {rank} meta set prefix {data['prefix']}")
                print(f"   ✅ Ранг '{rank}' создан")
            
            # 3. Выдача прав
            print("\n🔧 ШАГ 3: Настройка прав...")
            for rank, data in RANKS.items():
                for perm in data["permissions"]:
                    send_cmd(mcr, f"lp group {rank} permission set {perm} true")
                if "homes" in data:
                    send_cmd(mcr, f"lp group {rank} permission set essentials.sethome.multiple {data['homes']}")
                print(f"   ✅ Права для '{rank}' выданы")
            
            # 4. Сохранение
            print("\n💾 ШАГ 4: Сохранение и синхронизация...")
            send_cmd(mcr, "lp sync")
            send_cmd(mcr, "essentials reload")
            
            # 5. Итог
            print("\n" + "="*50)
            print("✅ НАСТРОЙКА ЗАВЕРШЕНА УСПЕШНО!")
            print("="*50)
            print("\n📋 СОЗДАННЫЕ РАНГИ:")
            for rank in RANKS.keys():
                print(f"   • {rank}")
            print("\n🎉 ТЕПЕРЬ ТВОЙ СЕРВЕР КАК HYPEMCPRO!")
            
    except ConnectionRefusedError:
        print(f"\n❌ НЕ УДАЛОСЬ ПОДКЛЮЧИТЬСЯ!")
        print("\n🔧 ПРОВЕРЬТЕ:")
        print("   1. Включён ли RCON в server.properties? (enable-rcon=true)")
        print("   2. Правильно ли указан порт? (обычно 25575)")
        print("   3. Запущен ли сервер Aternos?")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
