from database.db_connection import get_db, get_db
from datetime import datetime

SEED_SPECIES = [
    {
        "species_english": "Sumatran Tiger",
        "species_latin": "panthera tigris sumatrae",
        "body_text": (
            "The Sumatran Tiger is the smallest surviving tiger subspecies, found exclusively "
            "on the Indonesian island of Sumatra. Fewer than 400 individuals remain in the wild. "
            "Its dense forest habitat is rapidly disappearing due to agricultural expansion and "
            "illegal logging. Poaching for the illegal wildlife trade remains a severe threat. "
            "Conservation efforts include protected national parks, anti-poaching patrols, and "
            "community engagement programmes."
        ),
        "category": "Mammal",
        "extinction_risk": "Critically Endangered",
        "photoid": "sumatran tiger",
    },
    {
        "species_english": "Javan Rhinoceros",
        "species_latin": "rhinoceros sondaicus",
        "body_text": (
            "The Javan Rhinoceros is one of the rarest large mammals on Earth, with fewer than "
            "70 individuals confined entirely to Ujung Kulon National Park on the western tip of "
            "Java. It faces threats from its extremely small population size, habitat loss, and "
            "the risk of catastrophic events such as disease or volcanic activity. No captive "
            "individuals exist, making in-situ conservation absolutely critical."
        ),
        "category": "Mammal",
        "extinction_risk": "Critically Endangered",
        "photoid": "javan rhinoceros",
    },
    {
        "species_english": "Bali Myna",
        "species_latin": "leucopsar rothschildi",
        "body_text": (
            "The Bali Myna is a striking white bird endemic to the island of Bali. Fewer than "
            "100 individuals survive in the wild, making it one of the rarest birds in the world. "
            "The primary drivers of its decline are the illegal pet trade and loss of its lowland "
            "forest habitat. Captive breeding and reintroduction programmes have been key "
            "strategies in efforts to stabilise and grow its wild population."
        ),
        "category": "Bird",
        "extinction_risk": "Critically Endangered",
        "photoid": "bali myna"
    },
    {
        "species_english": "Javan Eagle",
        "species_latin": "nisaetus bartelsi",
        "body_text": (
            "The Javan Eagle is a medium-sized raptor endemic to the tropical forests of Java. "
            "Population estimates suggest fewer than 1,000 individuals remain. Severe "
            "deforestation and fragmentation of Java's forests, combined with illegal capture "
            "for the pet trade, have driven dramatic population declines. It is depicted on "
            "Indonesia's coat of arms as the Garuda, and its protection carries deep cultural "
            "significance."
        ),
        "category": "Bird",
        "extinction_risk": "Endangered",
        "photoid": "javan eagle"
    },
    {
        "species_english": "Tarsius",
        "species_latin": "tarsius sp.",
        "body_text": (
            "Tarsiers are among the world's smallest primates, found across Sulawesi and "
            "surrounding islands. They are unique among primates in being exclusively "
            "carnivorous, hunting insects and small vertebrates using enormous eyes adapted "
            "for night vision. Populations are estimated at under 5,000. Habitat destruction "
            "from agricultural conversion and logging, as well as the illegal pet trade, "
            "are the main threats."
        ),
        "category": "Mammal",
        "extinction_risk": "Endangered",
        "photoid": "tarsius"
    },
    {
        "species_english": "Celebes Crested Macaque",
        "species_latin": "macaca nigra",
        "body_text": (
            "The Celebes Crested Macaque is endemic to north-east Sulawesi, recognised by "
            "its jet-black coat and distinctive crest. Fewer than 5,500 individuals are thought "
            "to survive. The species is hunted for bushmeat and its forest habitat continues "
            "to shrink. Conservation programmes focus on community education, law enforcement, "
            "and ecotourism as a sustainable alternative income source for local communities."
        ),
        "category": "Mammal",
        "extinction_risk": "Critically Endangered",
        "photoid": "celebes crested macaque"
    },
]


def init_database():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS species (
            species_id INTEGER PRIMARY KEY AUTOINCREMENT,
            species_english TEXT UNIQUE,
            species_latin TEXT,
            body_text TEXT,
            category TEXT,
            extinction_risk TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            photoid TEXT
        )
        """)
    print("Database initialised.")
    seed_species()


def seed_species():
    with get_db() as conn:
        for sp in SEED_SPECIES:
            exists = conn.execute(
                "SELECT species_id FROM species WHERE species_english = ?",
                (sp["species_english"],)
            ).fetchone()
            if exists:
                print(f"  SKIP  {sp['species_english']} (already exists)")
                continue
            conn.execute("""
                INSERT INTO species
                    (species_english, species_latin, body_text, category, extinction_risk, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                sp["species_english"],
                sp["species_latin"],
                sp["body_text"],
                sp["category"],
                sp["extinction_risk"],
                datetime.now(),
            ))
            print(f"  ADD   {sp['species_english']}")
    print("Seeding complete.")


def init_accounts_database():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            account_type TEXT NOT NULL DEFAULT 'private_user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    print("Accounts database initialised.")


if __name__ == "__main__":
    init_database()
    init_accounts_database()