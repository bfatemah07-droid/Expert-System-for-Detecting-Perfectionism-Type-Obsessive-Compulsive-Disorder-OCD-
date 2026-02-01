# ====================================================
# King Abdulaziz University - FCIT
# Department of Computer Science
# CPCS331 – Artificial Intelligence – Fall 2026
#
# Expert System for Detecting Perfectionism Type OCD
# Section: EAR | Submit Date: 1 Nov 2025
#
# Team:
# Fatimah Baothman (2307298)
# Rafal Abdullah Riri (2308220)
# Maryam Kabbani (2306217)
# Sidrah Alyamani (2311603)
# ====================================================

from experta import *

# ================= Facts =================
class Profile(Fact):    # gender, age_group, role
    pass

class Symptoms(Fact):   # any_symptoms, checking, intrusive, can_relax
    pass

class OCDScore(Fact):   # value
    pass


# ============== Knowledge Engine ==============
class PerfectionismOCDEngine(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.tier = None          # "high" | "medium" | "low" | None
        self.messages = []        # aggregate rule messages for final printing

    # R1: No symptoms
    @Rule(Symptoms(any_symptoms=False))
    def rule1_no_symptoms(self):
        self.messages.append(
            "This system is designed for individuals who might suffer from perfectionism-related obsessive behaviors."
        )

    # Demographic rules fire only when role="other" (avoid overlap with R6)
    # R2: Female + Young + symptoms
    @Rule(Profile(gender="female", age_group="young", role="other"), Symptoms(any_symptoms=True))
    def rule2_female_young(self):
        self.messages.append(
            "The person may go into a cycle of checking and rechecking, a fear of imperfection, and anxiety about making small mistakes. Relaxation techniques and self-compassion training may be in order."
        )

    # R3: Female + Adult + symptoms
    @Rule(Profile(gender="female", age_group="adult", role="other"), Symptoms(any_symptoms=True))
    def rule3_female_adult(self):
        self.messages.append(
            "The person may repeatedly need to redo an activity or make everything ‘just right.’ The system suggests setting realistic goals, and if the distress lasts, one should seek counseling."
        )

    # R4: Male + Young + symptoms
    @Rule(Profile(gender="male", age_group="young", role="other"), Symptoms(any_symptoms=True))
    def rule4_male_young(self):
        self.messages.append(
            "The user may show tendencies to overcontrol and avoid activities for fear of making mistakes. The system recommends gradual exposure to imperfection and mindfulness exercises."
        )

    # R5: Male + Adult + symptoms
    @Rule(Profile(gender="male", age_group="adult", role="other"), Symptoms(any_symptoms=True))
    def rule5_male_adult(self):
        self.messages.append(
            "The user may feel constant pressure of meeting high standards at work or study. The system suggests stress management techniques and professional psychological consultation if anxiety interferes with daily life."
        )

    # R6: Student/Employee + symptoms
    @Rule(Profile(role=L("student") | L("employee")), Symptoms(any_symptoms=True))
    def rule6_role_pressure(self):
        self.messages.append(
            "The user might develop an excessive level of concern about grades or the quality of work. It is recommended to balance performance goals with self-care and realistic expectations."
        )

    # Symptom-specific rules
    # R7: Checking present
    @Rule(Symptoms(checking=True))
    def rule7_checking(self):
        self.messages.append(
            "The user shows clear signs of compulsive checking due to fear of imperfection. Recommend CBT to reduce these patterns."
        )

    # R8: Intrusive thoughts present
    @Rule(Symptoms(intrusive=True))
    def rule8_intrusive(self):
        self.messages.append(
            "Obsessive thinking regarding flaws or mistakes by the user. The system would recommend journaling, practicing awareness, and seeking a mental health professional."
        )

    # R9: Unable to relax (can_relax=False)
    @Rule(Symptoms(can_relax=False))
    def rule9_unable_to_relax(self):
        self.messages.append(
            "The user probably suffers from high perfectionism anxiety. The system recommends relaxation training, planning breaks, and reducing overcontrol behaviors."
        )

    # Classification rules (mark only; printing happens in Result section)
    @Rule(OCDScore(value=P(lambda v: v >= 8)))
    def rule10_mark_high(self):
        # It would be best to get professional assessment and help from a psychologist.
        self.tier = "high"

    @Rule(OCDScore(value=P(lambda v: 4 <= v <= 7)))
    def rule11_mark_medium(self):
        # Mild signs of perfectionism OCD tendencies; self-help and mindfulness techniques may be considered.
        self.tier = "medium"

    # any_symptoms=True starts at score >= 3; this covers 1..3 (0..2 is R1)
    @Rule(Symptoms(any_symptoms=True), OCDScore(value=P(lambda v: 1 <= v <= 3)))
    def rule12_mark_low(self):
        # No significant OCD symptoms were detected.
        self.tier = "low"


# ============== Input Helpers ==============
def ask_choice(prompt, choices):
    while True:
        v = input(f"{prompt} {choices}: ").strip().lower()
        if v in [c.lower() for c in choices]:
            return v
        print("Invalid choice. Please try again.")

POSITIVE = {"often", "yes", "high", "o", "y", "h"}   # +1
NEGATIVE = {"rarely", "no", "r", "n"}                # +0

def ask_level(prompt):
    while True:
        v = input(f"{prompt} (often/yes/high OR rarely/no): ").strip().lower()
        if v in POSITIVE or v in NEGATIVE:
            return v
        print("Please answer using: often/yes/high OR rarely/no (or o/y/h/r/n).")


# ================= Main =================
def main():
    print("\n=== Perfectionism OCD Expert System (CPCS331) ===")
    print("Note: Educational self-check — not a medical diagnosis.\n")

    gender    = ask_choice("Gender?", ["male", "female"])
    age_group = ask_choice("Age group?", ["young", "adult"])
    role      = ask_choice("Your role?", ["student", "employee", "other"])

    q_texts = [
        ("checking",          "Do you repeatedly check/review to ensure things are 'perfect'?"),
        ("intrusive",         "Do intrusive thoughts about small errors or flaws bother you?"),
        ("avoid",             "Do you avoid tasks because you fear not doing them perfectly?"),
        ("impact",            "Does striving for perfection impact your study/work time?"),
        ("unable_relax",      "Are you unable to relax before things feel 'perfect'?"),
        ("redo",              "Do you re-do tasks to remove tiny imperfections?"),
        ("over_organize",     "Do you spend excessive time organizing details?"),
        ("delay_submit",      "Do you delay submitting work to keep polishing it?"),
        ("fear_judgment",     "Do you fear being judged for small mistakes?"),
        ("seek_reassurance",  "Do you seek reassurance repeatedly about quality?"),
        ("plan_distress",     "Do slight plan deviations cause you noticeable distress?"),
        ("complaints",        "Do friends/family complain about your perfectionism?")
    ]

    score = 0
    answers = {}
    for key, text in q_texts:
        ans = ask_level(text)
        answers[key] = ans
        if ans in POSITIVE:
            score += 1

    # Map answers → Symptoms used by rules
    can_relax = not (answers["unable_relax"] in POSITIVE)  # yes → cannot relax → can_relax=False
    checking  = (answers["checking"]  in POSITIVE)
    intrusive = (answers["intrusive"] in POSITIVE)

    # any_symptoms only if score >= 3 (per your rubric)
    has_symptoms = score >= 3

    # Run engine
    engine = PerfectionismOCDEngine()
    engine.reset()
    engine.declare(Profile(gender=gender, age_group=age_group, role=role))
    engine.declare(Symptoms(any_symptoms=has_symptoms,
                            checking=checking,
                            intrusive=intrusive,
                            can_relax=can_relax))
    engine.declare(OCDScore(value=score))
    engine.run()

    print("\n")  # spacing before the result

    # Final output shape (Result + all rule messages + score note)
    tier = engine.tier
    if tier is None:
        if score >= 8:
            tier = "high"
        elif 4 <= score <= 7:
            tier = "medium"
        else:
            tier = "low" if has_symptoms else None

    if tier == "high":
        print("Result: Strong signs of Perfectionism OCD detected.")
        print("You might feel anxious or compelled to make everything perfect.")
        print("It’s recommended to seek professional guidance if this affects your well-being.\n")
    elif tier == "medium":
        print("Result: Mild signs of perfectionism OCD tendencies.")
        print("Self-help, mindfulness, and balanced routines may improve well-being.\n")
    else:
        print("Result: No significant OCD symptoms were detected.\n")

    for msg in engine.messages:
        print(msg + "\n")

    print(f"Your Total OCD Score = {score} / 12")
    print("Note: This system provides awareness only, not a medical diagnosis.\n")


if __name__ == "__main__":
    main()
