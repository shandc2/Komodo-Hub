from database.db_connection import get_db
from database.db_commands import register_user
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
            "community engagement programs."
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
            "forest habitat. Captive breeding and reintroduction programs have been key "
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
            "to shrink. Conservation programs focus on community education, law enforcement, "
            "and ecotourism as a sustainable alternative income source for local communities."
        ),
        "category": "Mammal",
        "extinction_risk": "Critically Endangered",
        "photoid": "celebes crested macaque"
    },
]
test_article = [
    {
        "article_id":"a-starrier-night",
        "title"     :"A Starrier Night",
        "subtitle"  :("In the past decade, our planet has rapidly lost its night sky. In response,"
                      "West Texas created the largest international dark-sky reserve on Earth."),
        "main_text" :("Light pollution has been growing rapidly, with the sky brightening nearly 10% each year "
                      "since 2011. In West Texas, the McDonald Observatory—the darkest observatory in the "
                      "continental US—faced an operational threat as development crept into the region. "
                      "Superintendent Teznie Pugh and colleagues partnered with local landowners, parks, and "
                      "The Nature Conservancy to protect the night sky. In 2022, DarkSky International certified "
                      "the Greater Big Bend International Dark Sky Reserve, covering 9.6 million acres and "
                      "spanning the US-Mexico border—the largest International Dark Sky Reserve in the world. "
                      "The Davis Mountains Preserve (33,000 acres) forms the core of the reserve. The greatest "
                      "ongoing threat comes from oil and gas development in the Permian Basin. The reserve also "
                      "supports ecological research into the effects of light pollution on nocturnal wildlife, "
                      "plants, and ecosystems."),
        "author"    :"Jenny Rogers",
        "publish_date":"2026-02-13"
    }
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
    init_accounts_database()
    print("Database initialised.")
    seed_species()

def init_articles():
    with get_db() as conn:
        # table for articles in library
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS articles (
                         article_id TEXT PRIMARY KEY UNIQUE,
                         title TEXT,
                         subtitle TEXT,
                         main_text TEXT,
                         author TEXT,
                         publish_date);""")
        print("Successfully created/found articles table.")
        # table to store links relevant to articles (e.g. sources or original article)
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS article_links (
                         link_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                         article_id TEXT NOT NULL,
                         url        TEXT NOT NULL,
                         link_text  TEXT,
                         FOREIGN KEY (article_id) REFERENCES articles(article_id)
                         ON DELETE CASCADE);""")
        print("Succesfully found/created article_links table.")
        for article in test_article:
            table_exists = conn.execute(
                "SELECT article_id FROM articles WHERE article_id = ?",
                (article["article_id"],)).fetchone()
            if table_exists:
                print(f"  SKIP  {article['article_id']} (already exists)")
                continue
            conn.execute("""
                         INSERT INTO articles
                         (article_id, title, subtitle, main_text, author, publish_date)
                         VALUES (?, ?, ?, ?, ?, ?)""",
                         (article["article_id"],
                          article["title"],
                          article["subtitle"],
                          article["main_text"],
                          article["author"],
                          article["publish_date"],))
            print(f"  ADD   {article['article_id']}")

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
                    (species_english, species_latin, body_text, category, extinction_risk, photoid, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                sp["species_english"],
                sp["species_latin"],
                sp["body_text"],
                sp["category"],
                sp["extinction_risk"],
                sp["photoid"],
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
        conn.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            user_id INTEGER
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS password_resets (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
    print("Accounts database initialised.")


def init_classes_database():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS classes (
            class_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            name       TEXT    NOT NULL,
            description TEXT   DEFAULT '',
            join_code  TEXT    UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS class_enrolments (
            class_id   INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (class_id, student_id)
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id      INTEGER NOT NULL,
            title         TEXT    NOT NULL,
            description   TEXT    DEFAULT '',
            max_marks     INTEGER DEFAULT 10,
            created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            student_id    INTEGER NOT NULL,
            answer_text   TEXT    NOT NULL,
            submitted_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            marks         INTEGER DEFAULT NULL,
            feedback      TEXT    DEFAULT NULL,
            marked_at     TIMESTAMP DEFAULT NULL,
            UNIQUE (assignment_id, student_id)
        )
        """)
    print("Classes database tables initialised.")


def init_programs_database():
    with get_db() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS programs (
            program_id INTEGER PRIMARY KEY AUTOINCREMENT,
            leader_id    INTEGER NOT NULL,
            title        TEXT    NOT NULL,
            description  TEXT    DEFAULT '',
            created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS program_enrolments (
            program_id INTEGER NOT NULL,
            user_id      INTEGER NOT NULL,
            enrolled_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (program_id, user_id)
        )
        """)
    print("Programs database tables initialised.")

def init_activities_database():
    activities_list = [
        {
            "title": "Build a Bird Feeder",
            "description": "Create a bird feeder using recycled materials.",
            "species": "Bird Conservation",
            "due_date": "3 days",
            "difficulty": "Easy"
        },
        {
            "title": "Plant a Tree",
            "description": "Plant a tree in your garden or local area to help restore natural habitats and support wildlife.",
            "species": "Habitat Restoration",
            "due_date": "5 days",
            "difficulty": "Medium"
        },
        {
            "title": "Organise a Conservation Awareness Campaign",
            "description": "Plan and deliver a campaign to raise awareness about endangered species.",
            "species": "Education & Conservation",
            "due_date": "2 weeks",
            "difficulty": "Hard"
        }
    ]

    with get_db() as conn:
        # Create activities table if it doesn't exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activities (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                species TEXT,
                due_date TEXT,
                difficulty TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Activities table created/found.")

        # Insert activities if not already in table
        for activity in activities_list:
            exists = conn.execute(
                "SELECT activity_id FROM activities WHERE title = ?",
                (activity["title"],)
            ).fetchone()
            if exists:
                print(f"  SKIP  {activity['title']} (already exists)")
                continue

            conn.execute("""
                INSERT INTO activities
                    (title, description, species, due_date, difficulty, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                activity["title"],
                activity["description"],
                activity["species"],
                activity["due_date"],
                activity["difficulty"],
                datetime.now(),
            ))
            print(f"  ADD   {activity['title']}")
    print("Activities seeding complete.")



init_database()
init_accounts_database()
init_classes_database()
init_programs_database()
init_articles()
init_activities_database()
register_user("admin", "admin@komodohub.org", "admin", "admin")