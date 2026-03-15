"""
Generates and seeds the sample SQLite database with car data.
Run this once to create cars.db before starting the MCP server.
"""

import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "cars.db")


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS manufacturers (
            id      INTEGER PRIMARY KEY,
            name    TEXT NOT NULL UNIQUE,
            country TEXT NOT NULL,
            founded INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS models (
            id              INTEGER PRIMARY KEY,
            manufacturer_id INTEGER NOT NULL REFERENCES manufacturers(id),
            name            TEXT NOT NULL,
            year_start      INTEGER NOT NULL,
            year_end        INTEGER,           -- NULL means still in production
            category        TEXT NOT NULL      -- sedan, suv, truck, sports, van
        );

        CREATE TABLE IF NOT EXISTS parts (
            id          INTEGER PRIMARY KEY,
            model_id    INTEGER NOT NULL REFERENCES models(id),
            part_number TEXT NOT NULL UNIQUE,
            name        TEXT NOT NULL,
            category    TEXT NOT NULL,         -- engine, suspension, brakes, electrical, body, interior
            description TEXT NOT NULL
        );
    """)


def seed(conn: sqlite3.Connection) -> None:
    manufacturers = [
        (1, "Toyota",     "Japan",   1937),
        (2, "Ford",       "USA",     1903),
        (3, "BMW",        "Germany", 1916),
        (4, "Honda",      "Japan",   1948),
        (5, "Chevrolet",  "USA",     1911),
        (6, "Volkswagen", "Germany", 1937),
        (7, "Subaru",     "Japan",   1953),
        (8, "Tesla",      "USA",     2003),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO manufacturers (id, name, country, founded) VALUES (?, ?, ?, ?)",
        manufacturers,
    )

    models = [
        # Toyota
        (1,  1, "Camry",      1982, None, "sedan"),
        (2,  1, "Corolla",    1966, None, "sedan"),
        (3,  1, "RAV4",       1994, None, "suv"),
        (4,  1, "Tacoma",     1995, None, "truck"),
        (5,  1, "Supra",      1978, 2002, "sports"),
        # Ford
        (6,  2, "F-150",      1948, None, "truck"),
        (7,  2, "Mustang",    1964, None, "sports"),
        (8,  2, "Explorer",   1990, None, "suv"),
        (9,  2, "Bronco",     2021, None, "suv"),
        # BMW
        (10, 3, "3 Series",   1975, None, "sedan"),
        (11, 3, "5 Series",   1972, None, "sedan"),
        (12, 3, "X5",         1999, None, "suv"),
        (13, 3, "M3",         1986, None, "sports"),
        # Honda
        (14, 4, "Civic",      1972, None, "sedan"),
        (15, 4, "Accord",     1976, None, "sedan"),
        (16, 4, "CR-V",       1995, None, "suv"),
        (17, 4, "Ridgeline",  2005, None, "truck"),
        # Chevrolet
        (18, 5, "Silverado",  1998, None, "truck"),
        (19, 5, "Corvette",   1953, None, "sports"),
        (20, 5, "Equinox",    2004, None, "suv"),
        (21, 5, "Camaro",     1966, None, "sports"),
        # Volkswagen
        (22, 6, "Golf",       1974, None, "sedan"),
        (23, 6, "Passat",     1973, None, "sedan"),
        (24, 6, "Tiguan",     2007, None, "suv"),
        # Subaru
        (25, 7, "Outback",    1994, None, "suv"),
        (26, 7, "Impreza",    1992, None, "sedan"),
        (27, 7, "WRX",        1992, None, "sports"),
        (28, 7, "Forester",   1997, None, "suv"),
        # Tesla
        (29, 8, "Model S",    2012, None, "sedan"),
        (30, 8, "Model 3",    2017, None, "sedan"),
        (31, 8, "Model X",    2015, None, "suv"),
        (32, 8, "Model Y",    2020, None, "suv"),
        (33, 8, "Cybertruck", 2023, None, "truck"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO models (id, manufacturer_id, name, year_start, year_end, category) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        models,
    )

    parts = [
        # --- Camry (1) ---
        (1,  1, "CAM-ENG-001", "2.5L 4-Cylinder Engine",         "engine",     "DOHC 16-valve naturally aspirated engine producing 203 hp"),
        (2,  1, "CAM-BRK-001", "Front Brake Caliper",            "brakes",     "Single-piston sliding caliper for front disc brakes"),
        (3,  1, "CAM-SUS-001", "Front Strut Assembly",           "suspension", "MacPherson strut with coil spring for front suspension"),
        (4,  1, "CAM-ELE-001", "Alternator 130A",                "electrical", "130-amp alternator to charge the 12V battery"),
        (5,  1, "CAM-BOD-001", "Front Bumper Cover",             "body",       "Painted thermoplastic front bumper cover"),
        # --- Corolla (2) ---
        (6,  2, "COR-ENG-001", "2.0L Dynamic Force Engine",      "engine",     "DOHC 16-valve engine producing 169 hp with VVT-i"),
        (7,  2, "COR-BRK-001", "Rear Drum Brake Kit",            "brakes",     "Complete rear drum brake kit including shoes and hardware"),
        (8,  2, "COR-INT-001", "Instrument Cluster Display",     "interior",   "7-inch multi-information display cluster"),
        # --- RAV4 (3) ---
        (9,  3, "RAV-ENG-001", "2.5L Hybrid Powertrain",         "engine",     "Combined system output of 219 hp with electric motor assist"),
        (10, 3, "RAV-SUS-001", "Rear Trailing Arm",              "suspension", "Rear trailing arm for double-wishbone suspension"),
        (11, 3, "RAV-BOD-001", "Roof Rail Set",                  "body",       "Aluminum cross-bar roof rack rails"),
        # --- Tacoma (4) ---
        (12, 4, "TAC-ENG-001", "3.5L V6 Engine",                 "engine",     "DOHC 24-valve V6 producing 278 hp"),
        (13, 4, "TAC-SUS-001", "Front Skid Plate",               "suspension", "Steel front skid plate for off-road protection"),
        (14, 4, "TAC-BOD-001", "Bed Liner",                      "body",       "Spray-in bed liner for the truck cargo bed"),
        # --- Supra (5) ---
        (15, 5, "SUP-ENG-001", "2JZ-GTE Turbo Engine",           "engine",     "Twin-turbocharged inline-6 producing 320 hp"),
        (16, 5, "SUP-SUS-001", "Adjustable Coilover Kit",        "suspension", "Full adjustable coilover suspension kit"),
        # --- F-150 (6) ---
        (17, 6, "F15-ENG-001", "3.5L EcoBoost V6",               "engine",     "Twin-turbocharged V6 producing 400 hp and 500 lb-ft torque"),
        (18, 6, "F15-ENG-002", "5.0L Coyote V8",                 "engine",     "Naturally aspirated V8 producing 400 hp"),
        (19, 6, "F15-BRK-001", "4-Wheel Disc Brake Kit",         "brakes",     "Heavy-duty 4-wheel disc brake upgrade kit"),
        (20, 6, "F15-BOD-001", "Running Board Set",              "body",       "Aluminum side step running boards"),
        # --- Mustang (7) ---
        (21, 7, "MUS-ENG-001", "5.0L Coyote V8",                 "engine",     "High-output V8 producing 450 hp in GT trim"),
        (22, 7, "MUS-ENG-002", "2.3L EcoBoost 4-Cylinder",       "engine",     "Turbocharged 4-cylinder producing 310 hp"),
        (23, 7, "MUS-SUS-001", "Performance Suspension Package",  "suspension", "Stiffer springs, larger sway bars, and strut tower brace"),
        (24, 7, "MUS-ELE-001", "Brembo Brake Upgrade",           "brakes",     "6-piston Brembo front calipers with slotted rotors"),
        # --- Explorer (8) ---
        (25, 8, "EXP-ENG-001", "3.0L EcoBoost V6",               "engine",     "Twin-turbocharged V6 producing 400 hp in ST trim"),
        (26, 8, "EXP-INT-001", "Third-Row Seat Assembly",        "interior",   "Fold-flat third-row bench seat"),
        # --- Bronco (9) ---
        (27, 9, "BRO-SUS-001", "Sasquatch Lift Kit",             "suspension", "2-inch suspension lift with Bilstein shocks"),
        (28, 9, "BRO-BOD-001", "Hardtop Roof Panel Set",         "body",       "Modular hardtop panels with removable sections"),
        # --- BMW 3 Series (10) ---
        (29, 10, "BMW3-ENG-001", "2.0L TwinPower Turbo",         "engine",     "Inline-4 turbocharged engine producing 255 hp in 330i"),
        (30, 10, "BMW3-SUS-001", "M Sport Suspension",           "suspension", "Lowered sport-tuned suspension with adaptive dampers"),
        (31, 10, "BMW3-ELE-001", "iDrive 8 Infotainment Unit",   "electrical", "14.9-inch curved iDrive 8 display and controller"),
        # --- BMW 5 Series (11) ---
        (32, 11, "BMW5-ENG-001", "3.0L Inline-6 Turbo",          "engine",     "Turbocharged inline-6 producing 375 hp in 540i xDrive"),
        (33, 11, "BMW5-INT-001", "Executive Lounge Rear Seat",   "interior",   "Rear seat with massage function and extended recline"),
        # --- BMW X5 (12) ---
        (34, 12, "BMWX-ENG-001", "3.0L xDrive45e Hybrid",       "engine",     "Plug-in hybrid inline-6 with combined output of 389 hp"),
        (35, 12, "BMWX-BOD-001", "Panoramic Sunroof",            "body",       "Two-section power panoramic glass sunroof"),
        # --- BMW M3 (13) ---
        (36, 13, "M3-ENG-001",  "3.0L S58 Twin-Turbo",          "engine",     "Hand-built twin-turbocharged inline-6 producing 503 hp in Competition"),
        (37, 13, "M3-BRK-001",  "Carbon Ceramic Brake Kit",     "brakes",     "Carbon-ceramic M compound brake kit with gold calipers"),
        # --- Honda Civic (14) ---
        (38, 14, "CIV-ENG-001", "1.5L VTEC Turbo",              "engine",     "Turbocharged 4-cylinder producing 192 hp"),
        (39, 14, "CIV-SUS-001", "Sport Shock Absorber Set",     "suspension", "Sport-tuned shock absorbers for improved handling"),
        (40, 14, "CIV-ELE-001", "Honda Sensing Suite",          "electrical", "Camera and radar unit for Honda Sensing safety systems"),
        # --- Honda Accord (15) ---
        (41, 15, "ACC-ENG-001", "2.0L VTEC Turbo",              "engine",     "Turbocharged inline-4 producing 252 hp in Sport Touring"),
        (42, 15, "ACC-INT-001", "10-Speed Automatic Transmission", "interior", "10-speed dual-clutch automatic transmission"),
        # --- Honda CR-V (16) ---
        (43, 16, "CRV-ENG-001", "2.0L Hybrid Powertrain",       "engine",     "Two-motor hybrid system with combined 204 hp output"),
        (44, 16, "CRV-BOD-001", "Hands-Free Power Tailgate",    "body",       "Power-actuated tailgate with hands-free foot sensor"),
        # --- Chevrolet Silverado (18) ---
        (45, 18, "SIL-ENG-001", "6.2L EcoTec3 V8",              "engine",     "Naturally aspirated V8 producing 420 hp and 460 lb-ft torque"),
        (46, 18, "SIL-BOD-001", "Multi-Flex Tailgate",          "body",       "6-function MultiPro tailgate system"),
        (47, 18, "SIL-SUS-001", "Z71 Off-Road Package",         "suspension", "Rancho monotube shocks and skid plates for off-road use"),
        # --- Corvette (19) ---
        (48, 19, "VET-ENG-001", "6.2L LT2 V8",                  "engine",     "Mid-mounted naturally aspirated V8 producing 495 hp"),
        (49, 19, "VET-SUS-001", "Magnetic Ride Control",        "suspension", "Continuous real-time damping adjustment suspension"),
        (50, 19, "VET-BRK-001", "Brembo Carbon Ceramic Brakes", "brakes",     "Standard carbon ceramic brake package on Z51"),
        # --- Camaro (21) ---
        (51, 21, "CAM2-ENG-001","6.2L LT1 V8",                  "engine",     "V8 producing 455 hp in SS trim"),
        (52, 21, "CAM2-ELE-001","Bose Audio System",            "electrical", "9-speaker 300W Bose premium audio system"),
        # --- VW Golf (22) ---
        (53, 22, "GOL-ENG-001", "2.0L TSI Turbo",               "engine",     "Turbocharged 4-cylinder producing 241 hp in GTI"),
        (54, 22, "GOL-SUS-001", "DCC Adaptive Chassis",         "suspension", "Dynamic Chassis Control with adjustable damping"),
        (55, 22, "GOL-INT-001", "Digital Cockpit Pro",          "interior",   "10-inch digital instrument cluster with navigation"),
        # --- VW Tiguan (24) ---
        (56, 24, "TIG-ENG-001", "2.0L TSI AWD",                 "engine",     "Turbocharged 4-cylinder with 4MOTION all-wheel drive, 184 hp"),
        (57, 24, "TIG-BOD-001", "Panoramic Tilting Sunroof",    "body",       "Large panoramic tilt/slide sunroof with UV protection"),
        # --- Subaru Outback (25) ---
        (58, 25, "OUT-ENG-001", "2.5L Boxer 4-Cylinder",        "engine",     "Naturally aspirated horizontally-opposed 4-cylinder, 182 hp"),
        (59, 25, "OUT-SUS-001", "X-Mode AWD System",            "suspension", "X-Mode controller and symmetrical AWD hardware"),
        (60, 25, "OUT-ELE-001", "EyeSight Driver Assist",       "electrical", "Stereo camera system for EyeSight safety features"),
        # --- Subaru WRX (27) ---
        (61, 27, "WRX-ENG-001", "2.4L Turbocharged Boxer",      "engine",     "Direct-injected turbocharged boxer-4 producing 271 hp"),
        (62, 27, "WRX-SUS-001", "STI Sport Suspension",         "suspension", "Bilstein struts and springs with front/rear sway bars"),
        # --- Tesla Model S (29) ---
        (63, 29, "MDS-ENG-001", "Dual Motor All-Wheel Drive",   "engine",     "Front and rear electric motors with combined 670 hp in Plaid"),
        (64, 29, "MDS-ELE-001", "17-Inch Cinematic Display",    "electrical", "17-inch horizontal touchscreen with 2200x1300 resolution"),
        (65, 29, "MDS-INT-001", "Yoke Steering Wheel",          "interior",   "Aircraft-style yoke steering wheel"),
        # --- Tesla Model 3 (30) ---
        (66, 30, "MD3-ENG-001", "Long Range Dual Motor",        "engine",     "Dual motor AWD with 358 hp and 358-mile EPA range"),
        (67, 30, "MD3-ELE-001", "15.4-Inch Touchscreen",        "electrical", "15.4-inch center touchscreen with vehicle controls"),
        (68, 30, "MD3-BRK-001", "Regenerative Braking System",  "brakes",     "Standard and strong regenerative braking with one-pedal drive"),
        # --- Tesla Model Y (32) ---
        (69, 32, "MDY-ENG-001", "Performance Dual Motor",       "engine",     "Dual motor AWD producing 456 hp with 0-60 in 3.5s"),
        (70, 32, "MDY-BOD-001", "Glass Roof Panel",             "body",       "Full-length panoramic UV-filtering glass roof"),
        # --- Tesla Cybertruck (33) ---
        (71, 33, "CYB-BOD-001", "Exoskeleton Body Panel",       "body",       "Ultra-hard 30X cold-rolled stainless steel body panel"),
        (72, 33, "CYB-SUS-001", "Adaptive Air Suspension",      "suspension", "Air suspension with 6-inch ride height adjustment"),
        (73, 33, "CYB-ENG-001", "Tri Motor AWD System",         "engine",     "Three-motor system producing 845 hp with 0-60 in 2.6s"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO parts "
        "(id, model_id, part_number, name, category, description) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        parts,
    )

    conn.commit()


if __name__ == "__main__":
    with sqlite3.connect(DB_PATH) as conn:
        create_schema(conn)
        seed(conn)
    print(f"Database seeded at {DB_PATH}")
