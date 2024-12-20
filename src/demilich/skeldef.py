from demilich.builder import SkeletonBuilder
from demilich.restrictions import to_races, to_power#, to_toughness

skeleton = (
    SkeletonBuilder()
    .create_keywords(
        flying="flying",
        vigilance="vigilance",
        lifelink="lifelink",
        first_strike="first strike",
        double_strike="double strike",
        ward="ward N",
        defender="defender",
        flash="flash",
        menace="menace",
        deathtouch="deathtouch",
        trample="trample",
        haste="haste",
        reach="reach",
    )
    .create_races(
        dinosaur="Dinosaur",
        dog="Dog",
        spirit="Spirit",
        human="Human",
        cat="Cat",
        bird="Bird",
    )
    .create_classes(
        cleric="Cleric",
        knight="Knight",
        monk="Monk",
        mystic="Mystic",
        soldier="Soldier",
        nomad="Nomad",
        samurai="Samurai",
        scout="Scout",
    )
    .common()
    .white(slots=15)
        .creatures()
        .restrict(flying=to_races(bird=True, spirit=True, dinosaur=False))
        .restrict(double_strike=to_power(under=3))
        # these are more examples, though they don't apply in white
        # .restrict(deathtouch=to_power(under=3))
        # .restrict(trample=to_power(over=3))
        # .restrict(defender=to_toughness(over=3))
        .mana_values(1, 2, 2, 2, 3, 3, 3, 4, 4, (5, 6), (6, 7))
        .sizes(
            (1, 1), (2, 2), (1, 2), (2, 2), (3, 3), (3, 3),
            (3, 3), (4, 4), (4, 4), (5, 6), (6, 6)
        )
        .with_keywords(
            flying=3, vigilance=2, lifelink=1,
            first_strike=0.25, double_strike=0.2
        )
        .from_races(
            human=20, bird=15, spirit=10, cat=5, dog=1, dinosaur=1,
        )
        .from_classes(
            none=20, scout=10, knight=10, soldier=10, monk=5, nomad=5,
            cleric=1, mystic=1, samurai=1,
        )

        .spells()
        .instruction("Combat-related removal")
        .card("Banishing Light", "Exile until this leaves", "{2}{W}")
        .instruction("Combat trick", "{W}")
        .card("Disenchant", "Removal for artifact and/or enchantment", "{1}{W}")

    .blue(slots=15)
        .creatures()
        .mana_values(2, 2, 3, 3, 3, 4, (5,6), (6,7))
    .black(slots=15)
        .creatures()
        .mana_values(1.5, 2, 2, 3, 3, 4, (4,5), (5,5), (6,7))
    .red(slots=15)
        .creatures()
        .mana_values(1.5, 2, 2, 3, 3, (3,4), (4,5), 5, 6)
    .green(slots=15)
        .creatures()
        .mana_values(1.5, 2, 2, 3, 3, (3,4), (4,5), 5, 6, (6,7))
    .artifact(slots=6)
        .creatures()
        .mana_values(2, 3, 4)
)
