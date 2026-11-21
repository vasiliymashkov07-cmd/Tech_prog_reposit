from __future__ import annotations

from typing import Sequence
from pathlib import Path
from .game.game_facade import GameFacade

from .combat.outcome import Outcome
from .console_view import ConsoleView
from .hero.hero import Hero
from .hero.hero_class import HeroClass
from .item.item import Item

VIEW = ConsoleView()


def main() -> None:
    save_file = Path("saves") / "heroes.json"
    print("Файл сохранения: " + str(save_file.resolve()))
    game = GameFacade(save_file)
    hero = choose_hero(game)
    print(f"{hero.name} разбивает лагерь на опушке мистического леса.")

    while True:
        print()
        VIEW.print_hero(hero)
        print("1 - отправиться в экспедицию, 2 - снаряжение, 3 - торговец, 4 - журнал, 0 - выйти из игры")
        choice = input().strip()
        if choice == "1":
            go_on_expedition(hero, game)
        elif choice == "2":
            manage_equipment(hero, game)
        elif choice == "3":
            visit_merchant(hero, game)
        elif choice == "4":
            for report in game.get_journal(hero.name):
                print(
                    VIEW.summarize(
                        report,
                        game.get_location(report.location_code).display_name,
                        game.get_tactic(report.tactic_code).display_name,
                    )
                )
        elif choice == "0":
            return
        else:
            print("Такого варианта нет")


def choose_hero(game: GameFacade) -> Hero:
    heroes = game.heroes
    if not heroes:
        return create_hero(game)
    print("Выберите сохраненного героя (0 - создать нового):")
    for i, hero in enumerate(heroes):
        print(f"{i + 1} - {hero.name}, {hero.hero_class.display_name} {hero.level} ур.")
    index = read_choice(len(heroes))
    return heroes[index] if index >= 0 else create_hero(game)


def create_hero(game: GameFacade) -> Hero:
    print("Создайте своего героя!")
    while True:
        print("Выберите класс:")
        hero_classes = list(HeroClass)
        for i, hero_class in enumerate(hero_classes):
            weapon, armor = game.get_starter_kit(hero_class.code)
            print(
                f"{i + 1} - {hero_class.display_name} (здоровье {hero_class.base_health}): "
                f"{VIEW.describe(weapon)}, {VIEW.describe(armor)}"
            )
        class_index = read_choice(len(hero_classes))
        if class_index < 0:
            continue
        hero_class = hero_classes[class_index]

        print("Введите имя:")
        name = input().strip()

        try:
            return game.create_hero(name, hero_class.code)
        except ValueError as error:
            print(f"Не получилось создать героя: {error}")


def go_on_expedition(hero: Hero, game: GameFacade) -> None:
    all_locations = game.locations
    print("Куда отправимся?")
    for i, location in enumerate(all_locations):
        print(f"{i + 1} - {location.display_name} (рекомендуемый уровень {location.recommended_level})")
    index = read_choice(len(all_locations))
    if index < 0:
        return

    location = all_locations[index]
    print("Выберите тактику:")
    for i, tactic in enumerate(game.tactics):
        print(f"{i + 1} - {tactic.display_name}: {tactic.description}")
    tactic_index = read_choice(len(game.tactics))
    if tactic_index < 0:
        return
    report = game.explore(hero.name, location.code, game.tactics[tactic_index].code)
    print()
    VIEW.print_report(report, location.display_name)

    if report.battle.outcome == Outcome.VICTORY and report.battle.enemy.code == "dragon":
        print(f"\nДракон повержен! Барды еще долго будут петь о подвиге героя по имени {hero.name}.")


def manage_equipment(hero: Hero, game: GameFacade) -> None:
    inventory = hero.inventory
    if not inventory:
        print("Инвентарь пуст")
        return

    print("Что экипировать? (0 - назад)")
    print_items(inventory)
    index = read_choice(len(inventory))
    if index < 0:
        return

    item = inventory[index]
    game.equip(hero.name, index)
    print("Экипировано: " + VIEW.describe(item))


def visit_merchant(hero: Hero, game: GameFacade) -> None:
    print(f'Торговец: "Чего желаешь?" (золото: {hero.gold})')
    print("1 - купить, 2 - продать, 0 - назад")
    choice = input().strip()
    if choice == "1":
        buy(hero, game)
    elif choice == "2":
        sell(hero, game)


def buy(hero: Hero, game: GameFacade) -> None:
    showcase = game.showcase
    for i, item in enumerate(showcase):
        print(f"{i + 1} - {VIEW.describe(item)}: {item.price} золота")
    index = read_choice(len(showcase))
    if index < 0:
        return

    try:
        item = game.buy(hero.name, showcase[index].code)
        print("Куплено: " + VIEW.describe(item))
    except ValueError as error:
        print(error)


def sell(hero: Hero, game: GameFacade) -> None:
    inventory = hero.inventory
    if not inventory:
        print("Продавать нечего (экипированные предметы продать нельзя)")
        return

    for i, item in enumerate(inventory):
        print(f"{i + 1} - {VIEW.describe(item)}: {game.sell_price(item)} золота")
    index = read_choice(len(inventory))
    if index < 0:
        return

    item = inventory[index]
    price = game.sell(hero.name, index)
    print(f"Продано: {item.name} за {price} золота")


def print_items(items: Sequence[Item]) -> None:
    for i, item in enumerate(items):
        print(f"{i + 1} - {VIEW.describe(item)}")


# читает номер варианта от 1 до count, возвращает индекс или -1, если ввели что-то другое
def read_choice(count: int) -> int:
    try:
        choice = int(input().strip())
        if 1 <= choice <= count:
            return choice - 1
    except ValueError:
        # некорректный ввод обрабатываем так же, как отказ от выбора
        pass

    return -1


if __name__ == "__main__":
    main()
