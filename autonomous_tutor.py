import sqlite3
import datetime

# --- 1. PEDAGOGICAL FEEDBACK DATA (LaTeX & English) ---
HINTS = {
    "K1": "Remember: $a^0 = 1$ (except when a=0) and $a^1 = a$. Use these to simplify your expression.",
    "K2": "Negative power means reciprocal! $a^{-n} = 1/a^n$. Flip the fraction to make the power positive.",
    "K3": "Product Rule: $a^m \\cdot a^n = a^{m+n}$. Just add the exponents if the bases are the same.",
    "K4": "Power of a Power: $(a^m)^n = a^{m \\cdot n}$. Multiply the inner power by the outer power.",
    "K5": "Quotient Rule: $a^m / a^n = a^{m-n}$. Subtract the bottom exponent from the top one.",
    "K6": "Same Exponent: $a^n \\cdot b^n = (a \\cdot b)^n$. Combine the bases under the common power.",
    "K7": "Same Exponent (Division): $a^n / b^n = (a/b)^n$. Divide the bases first, then apply the power."
}

# --- 2. THE ENGINE (Autonomous Logic & Student Analytics) ---
class TutorEngine:
    def __init__(self):
        self.difficulty = "Medium" # Starting point
        self.logs = []
        self.stats = {k: {"correct": 0, "total": 0} for k in HINTS.keys()}

    def process_result(self, is_correct, rule_code):
        self.stats[rule_code]["total"] += 1
        if is_correct:
            self.stats[rule_code]["correct"] += 1
            # Progressive difficulty: Medium -> Hard
            if self.difficulty == "Medium": self.difficulty = "Hard"
            return "✅ Excellent work! Keep it up."
        else:
            # Regressive difficulty: Medium/Hard -> Easy
            self.difficulty = "Easy"
            return f"❌ Let's try an easier one.\n💡 HINT: {HINTS[rule_code]}"

# --- 3. MAIN APPLICATION (Database & Flow) ---
class MathAssistantApp:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:') # Professional in-memory DB
        self.cursor = self.conn.cursor()
        self.engine = TutorEngine()
        self.initialize_system()

    def initialize_system(self):
        # Create Tables
        self.cursor.execute('CREATE TABLE questions (id INT, rule TEXT, text TEXT, ans TEXT, diff TEXT)')
        
        # --- THE 42 QUESTION DATASET (K1-K7) ---
        q_bank = [
            # K1: Zero/First Power
            (1,'K1','15^1 + 1^0','16','Easy'),(2,'K1','(-5)^0','1','Easy'),
            (3,'K1','x^1 = 25, x=?','25','Medium'),(4,'K1','10^0 + 10^1','11','Medium'),
            (5,'K1','Starts with 5^0 million, Year 1?','1','Hard'),(6,'K1','2^n = 1, n=?','0','Hard'),
            # K2: Negative Exponents
            (7,'K2','2^-3 as fraction','1/8','Easy'),(8,'K2','10^-1 as decimal','0.1','Easy'),
            (9,'K2','(1/2)^-2','4','Medium'),(10,'K2','3^-1 + 3^-1 + 3^-1','1','Medium'),
            (11,'K2','Bacteria half (2^-1) every hour. 16 start, 2h later?','4','Hard'),(12,'K2','1/x^5 as negative power','x^-5','Hard'),
            # K3: Product Rule
            (13,'K3','x^2 * x^3','x^5','Easy'),(14,'K3','2^2 * 2^1','8','Easy'),
            (15,'K3','5^n * 5^2 = 5^7, n=?','5','Medium'),(16,'K3','10^2 * 10^-4','10^-2','Medium'),
            (17,'K3','Area 2^4. Double width (2^1), new area?','2^5','Hard'),(18,'K3','x^a * x^b * x^c','x^{a+b+c}','Hard'),
            # K4: Power of Power
            (19,'K4','(x^3)^2','x^6','Easy'),(20,'K4','(2^2)^3','64','Easy'),
            (21,'K4','(3^n)^2 = 3^10, n=?','5','Medium'),(22,'K4','(x^-2)^3','x^-6','Medium'),
            (23,'K4','Volume (2^2)^3. Side s if V=s^3?','4','Hard'),(24,'K4','((x^2)^3)^2','x^12','Hard'),
            # K5: Quotient Rule
            (25,'K5','x^8 / x^3','x^5','Easy'),(26,'K5','10^5 / 10^3','100','Easy'),
            (27,'K5','7^10 / 7^n = 7^4, n=?','6','Medium'),(28,'K5','2^3 / 2^-2','2^5','Medium'),
            (29,'K5','Dist 10^6, Time 10^2, Speed?','10^4','Hard'),(30,'K5','x^m / x^{m-1}','x','Hard'),
            # K6: Power of Product
            (31,'K6','(2*3)^2','36','Easy'),(32,'K6','2^3 * 5^3 as power','10^3','Easy'),
            (33,'K6','(x*4)^2 = 64, x=?','2','Medium'),(34,'K6','(a^2 * b^3)^2','a^4 * b^6','Medium'),
            (35,'K6','Triple (3^n) growth. 2 of each type, total?','(2*3)^n','Hard'),(36,'K6','(2x^2 y^3)^3','8x^6 y^9','Hard'),
            # K7: Power of Quotient
            (37,'K7','(10/2)^2','25','Easy'),(38,'K7','12^3 / 4^3 as power','3^3','Easy'),
            (39,'K7','(1/3)^2','1/9','Medium'),(40,'K7','(x^2 / y^3)^2','x^4 / y^6','Medium'),
            (41,'K7','Pizza slices 4^3, box 2^3. Box count?','2^3','Hard'),(42,'K7','(x/2)^3 = 27, x=?','6','Hard')
        ]
        self.cursor.executemany('INSERT INTO questions VALUES (?,?,?,?,?)', q_bank)
        self.conn.commit()

    def generate_report(self):
        filename = f"Teacher_Report_{datetime.date.today()}.txt"
        with open(filename, "w") as f:
            f.write("--- AUTONOMOUS LEARNING REPORT ---\n")
            f.write(f"Date: {datetime.datetime.now()}\n\n")
            f.write("RULE SUMMARY:\n")
            for rule, data in self.engine.stats.items():
                accuracy = (data['correct']/data['total']*100) if data['total'] > 0 else 0
                f.write(f"{rule}: {accuracy:.1f}% accuracy ({data['correct']}/{data['total']})\n")
            f.write("\n--- END OF REPORT ---")
        print(f"\n[SYSTEM] Session finished. Report saved to: {filename}")

    def start_session(self):
        print("=== Autonomous Exponents Tutor (English) ===")
        print("Rules: K1 to K7 | Difficulty: Adaptive")
        print("Type 'exit' to quit.\n")
        
        rules_to_test = ["K1", "K2", "K3", "K4", "K5", "K6", "K7"]
        
        for rule in rules_to_test:
            # Fetch question based on autonomous difficulty
            self.cursor.execute("SELECT text, ans FROM questions WHERE rule=? AND diff=?", 
                                (rule, self.engine.difficulty))
            q = self.cursor.fetchone()
            
            if q:
                print(f"Rule {rule} | Difficulty: {self.engine.difficulty}")
                user_ans = input(f"Solve: {q[0]} = ")
                
                if user_ans.lower() == 'exit': break
                
                is_correct = (user_ans.replace(" ", "") == q[1])
                feedback = self.engine.process_result(is_correct, rule)
                print(feedback + "\n" + "-"*40)
        
        self.generate_report()

if __name__ == "__main__":
    app = MathAssistantApp()
    app.start_session()