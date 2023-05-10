import requests

class Streamer():
    def __init__(self):
        self.hashtags = ["#εκλογες_2023", "#εκλογες2023", "#ΣΥΡΙΖΑ", "#ΣΥΡΙΖΑ_ΠΣ ", "#Εκλογες_21__Μαιου",  "#Τσιπρας",
                         "#Εκλογες_21__Μαιου", "#ΠΑΣΟΚ", "#ΝΔ", "#ΚΚΕ", "#ΜέΡΑ25", "#MeRA25", "#Βελοπουλος"]
        self.users = ["@kmitsotakis", "@atsipras", "@syriza_gr", "@neademokratia", "@gt_kke", "@mera25_gr",
                      "@varoufakis_gr", "@velopky"]
        self.keywords = ["ΝΕΑ ΔΗΜΟΚΡΑΤΙΑ", "νέα δημοκρατία", "ΚΚΕ", "ΣΥΡΙΖΑ", "σύριζα", "ΠΑΣΟΚ", "πασόκ", "Μητσοτάκης",
                         "Τσίπρας", "Κουτσούμπας", "Βαρουφάκης", "ΜΕΡΑ25"]


if __name__ == "__main__":
    print()