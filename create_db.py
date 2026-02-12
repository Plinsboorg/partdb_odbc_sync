"""Create a sample Part-DB SQLite database for KiCad database library testing."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "partdb.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS Resistors (
    id          TEXT PRIMARY KEY,
    IPN         TEXT,
    Value       TEXT,
    Description TEXT,
    Keywords    TEXT,
    Symbols     TEXT,
    Footprints  TEXT,
    Manufacturer TEXT,
    MPN         TEXT,
    Package     TEXT,
    Tolerance   TEXT,
    Power       TEXT,
    Datasheet   TEXT,
    PartDbUrl   TEXT
);

CREATE TABLE IF NOT EXISTS Capacitors (
    id          TEXT PRIMARY KEY,
    IPN         TEXT,
    Value       TEXT,
    Description TEXT,
    Keywords    TEXT,
    Symbols     TEXT,
    Footprints  TEXT,
    Manufacturer TEXT,
    MPN         TEXT,
    Package     TEXT,
    Voltage     TEXT,
    Dielectric  TEXT,
    Datasheet   TEXT,
    PartDbUrl   TEXT
);

CREATE TABLE IF NOT EXISTS Inductors (
    id          TEXT PRIMARY KEY,
    IPN         TEXT,
    Value       TEXT,
    Description TEXT,
    Keywords    TEXT,
    Symbols     TEXT,
    Footprints  TEXT,
    Manufacturer TEXT,
    MPN         TEXT,
    Package     TEXT,
    Current     TEXT,
    Datasheet   TEXT,
    PartDbUrl   TEXT
);

CREATE TABLE IF NOT EXISTS Diodes (
    id          TEXT PRIMARY KEY,
    IPN         TEXT,
    Value       TEXT,
    Description TEXT,
    Keywords    TEXT,
    Symbols     TEXT,
    Footprints  TEXT,
    Manufacturer TEXT,
    MPN         TEXT,
    Package     TEXT,
    Datasheet   TEXT,
    PartDbUrl   TEXT
);

CREATE TABLE IF NOT EXISTS ICs (
    id          TEXT PRIMARY KEY,
    IPN         TEXT,
    Value       TEXT,
    Description TEXT,
    Keywords    TEXT,
    Symbols     TEXT,
    Footprints  TEXT,
    Manufacturer TEXT,
    MPN         TEXT,
    Package     TEXT,
    Datasheet   TEXT,
    PartDbUrl   TEXT
);

CREATE TABLE IF NOT EXISTS Connectors (
    id          TEXT PRIMARY KEY,
    IPN         TEXT,
    Value       TEXT,
    Description TEXT,
    Keywords    TEXT,
    Symbols     TEXT,
    Footprints  TEXT,
    Manufacturer TEXT,
    MPN         TEXT,
    Package     TEXT,
    Datasheet   TEXT,
    PartDbUrl   TEXT
);
"""

# Sample data using KiCad's built-in library symbols/footprints
SAMPLE_DATA = {
    "Resistors": [
        ("R001", "R-0402-10K", "10k", "Resistor 10k 0402 1%", "resistor smd",
         "Device:R", "Resistor_SMD:R_0402_1005Metric",
         "Yageo", "RC0402FR-0710KL", "0402", "1%", "0.0625W", "", ""),
        ("R002", "R-0402-4K7", "4.7k", "Resistor 4.7k 0402 1%", "resistor smd",
         "Device:R", "Resistor_SMD:R_0402_1005Metric",
         "Yageo", "RC0402FR-074K7L", "0402", "1%", "0.0625W", "", ""),
        ("R003", "R-0603-100R", "100R", "Resistor 100R 0603 1%", "resistor smd",
         "Device:R", "Resistor_SMD:R_0603_1608Metric",
         "Yageo", "RC0603FR-07100RL", "0603", "1%", "0.1W", "", ""),
        ("R004", "R-0805-1K", "1k", "Resistor 1k 0805 5%", "resistor smd",
         "Device:R", "Resistor_SMD:R_0805_2012Metric",
         "Yageo", "RC0805JR-071KL", "0805", "5%", "0.125W", "", ""),
        ("R005", "R-0402-0R", "0R", "Resistor 0R 0402 jumper", "resistor smd jumper",
         "Device:R", "Resistor_SMD:R_0402_1005Metric",
         "Yageo", "RC0402JR-070RL", "0402", "", "0.0625W", "", ""),
    ],
    "Capacitors": [
        ("C001", "C-0402-100N", "100nF", "Capacitor 100nF 0402 16V X5R", "capacitor smd mlcc",
         "Device:C", "Capacitor_SMD:C_0402_1005Metric",
         "Murata", "GRM155R61C104KA88D", "0402", "16V", "X5R", "", ""),
        ("C002", "C-0402-1U", "1uF", "Capacitor 1uF 0402 6.3V X5R", "capacitor smd mlcc",
         "Device:C", "Capacitor_SMD:C_0402_1005Metric",
         "Murata", "GRM155R60J105ME15D", "0402", "6.3V", "X5R", "", ""),
        ("C003", "C-0805-10U", "10uF", "Capacitor 10uF 0805 16V X5R", "capacitor smd mlcc",
         "Device:C", "Capacitor_SMD:C_0805_2012Metric",
         "Samsung", "CL21A106KAYNNNE", "0805", "16V", "X5R", "", ""),
        ("C004", "C-0603-10N", "10nF", "Capacitor 10nF 0603 50V C0G", "capacitor smd mlcc",
         "Device:C", "Capacitor_SMD:C_0603_1608Metric",
         "Murata", "GRM1885C1H103JA01D", "0603", "50V", "C0G", "", ""),
        ("C005", "C-1206-100U", "100uF", "Capacitor 100uF 1206 6.3V X5R", "capacitor smd mlcc",
         "Device:C_Polarized", "Capacitor_SMD:C_1206_3216Metric",
         "Samsung", "CL31A107MQHNNNE", "1206", "6.3V", "X5R", "", ""),
    ],
    "Inductors": [
        ("L001", "L-0402-1U", "1uH", "Inductor 1uH 0402 1.2A", "inductor smd",
         "Device:L", "Inductor_SMD:L_0402_1005Metric",
         "Murata", "LQM15FN1R0N00D", "0402", "1.2A", "", ""),
        ("L002", "L-0603-10U", "10uH", "Inductor 10uH 0603 0.8A", "inductor smd",
         "Device:L", "Inductor_SMD:L_0603_1608Metric",
         "Murata", "LQM18FN100M00D", "0603", "0.8A", "", ""),
    ],
    "Diodes": [
        ("D001", "D-SOD323-1N4148", "1N4148W", "Diode switching 100V 0.15A SOD-323", "diode switching",
         "Device:D", "Diode_SMD:D_SOD-323",
         "Nexperia", "1N4148WS,115", "SOD-323", "", ""),
        ("D002", "D-SMA-SS14", "SS14", "Schottky diode 40V 1A SMA", "diode schottky",
         "Device:D_Schottky", "Diode_SMD:D_SMA",
         "MDD", "SS14", "SMA", "", ""),
        ("D003", "LED-0603-RED", "Red", "LED Red 0603 2V 20mA", "led smd red",
         "Device:LED", "LED_SMD:LED_0603_1608Metric",
         "Everlight", "19-217/R6C-AL1M2VY/3T", "0603", "", ""),
    ],
    "ICs": [
        ("IC001", "IC-STM32F070F6", "STM32F070F6P6", "MCU ARM Cortex-M0 48MHz 32KB Flash TSSOP-20", "mcu arm stm32 cortex",
         "MCU_ST_STM32F0:STM32F070F6Px", "Package_SO:TSSOP-20_4.4x6.5mm_P0.65mm",
         "STMicroelectronics", "STM32F070F6P6", "TSSOP-20", "", ""),
        ("IC002", "IC-STM32F446RC", "STM32F446RCT6", "MCU ARM Cortex-M4 180MHz 256KB Flash LQFP-64", "mcu arm stm32 cortex",
         "MCU_ST_STM32F4:STM32F446RCTx", "Package_QFP:LQFP-64_10x10mm_P0.5mm",
         "STMicroelectronics", "STM32F446RCT6", "LQFP-64", "", ""),
        ("IC003", "IC-LM1117-3V3", "LM1117-3.3", "LDO 3.3V 800mA SOT-223", "regulator ldo linear voltage",
         "Regulator_Linear:AMS1117-3.3", "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
         "Texas Instruments", "LM1117MP-3.3/NOPB", "SOT-223", "", ""),
    ],
    "Connectors": [
        ("J001", "J-USB-C-16P", "USB-C", "USB Type-C Receptacle 16-pin", "usb type-c connector",
         "Connector:USB_C_Receptacle_USB2.0", "Connector_USB:USB_C_Receptacle_GCT_USB4105",
         "GCT", "USB4105-GF-A", "SMD", "", ""),
        ("J002", "J-HDR-2x5-1.27", "2x5 1.27mm", "Pin Header 2x5 1.27mm SWD", "header pin swd debug",
         "Connector_Generic:Conn_02x05_Odd_Even", "Connector_PinHeader_1.27mm:PinHeader_2x05_P1.27mm_Vertical_SMD",
         "Samtec", "FTSH-105-01-L-DV-K", "SMD", "", ""),
    ],
}


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Create tables
    cur.executescript(SCHEMA)

    # Insert sample data
    for row in SAMPLE_DATA["Resistors"]:
        cur.execute(
            "INSERT INTO Resistors VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row
        )

    for row in SAMPLE_DATA["Capacitors"]:
        cur.execute(
            "INSERT INTO Capacitors VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row
        )

    for row in SAMPLE_DATA["Inductors"]:
        cur.execute(
            "INSERT INTO Inductors VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", row
        )

    for row in SAMPLE_DATA["Diodes"]:
        cur.execute(
            "INSERT INTO Diodes VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", row
        )

    for row in SAMPLE_DATA["ICs"]:
        cur.execute(
            "INSERT INTO ICs VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", row
        )

    for row in SAMPLE_DATA["Connectors"]:
        cur.execute(
            "INSERT INTO Connectors VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", row
        )

    conn.commit()
    conn.close()
    print(f"Created {DB_PATH}")
    print(f"  Resistors:  {len(SAMPLE_DATA['Resistors'])} parts")
    print(f"  Capacitors: {len(SAMPLE_DATA['Capacitors'])} parts")
    print(f"  Inductors:  {len(SAMPLE_DATA['Inductors'])} parts")
    print(f"  Diodes:     {len(SAMPLE_DATA['Diodes'])} parts")
    print(f"  ICs:        {len(SAMPLE_DATA['ICs'])} parts")
    print(f"  Connectors: {len(SAMPLE_DATA['Connectors'])} parts")


if __name__ == "__main__":
    main()
