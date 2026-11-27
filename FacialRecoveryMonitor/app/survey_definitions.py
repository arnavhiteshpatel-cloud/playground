"""Symptom survey content.

Responses are stored with their text label *and* (for ordered answer scales) an
integer position so they can be charted. Positions are only an ordering of the
answer options — they are not clinical scores, and the app never sums them into
a severity rating.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OptionSet:
    key: str
    labels: tuple[str, ...]
    ordinal: bool = True                 # False → categories have no natural order
    excluded_from_chart: tuple[str, ...] = ()  # e.g. "Not applicable"

    def score(self, label: str):
        if not self.ordinal or label in self.excluded_from_chart or label not in self.labels:
            return None
        return self.labels.index(label)

    @property
    def chart_labels(self) -> tuple[str, ...]:
        return tuple(l for l in self.labels if l not in self.excluded_from_chart)


FREQUENCY = OptionSet("frequency", ("No", "Sometimes", "Often", "Always"))
IMPACT = OptionSet("impact", ("Not at all", "A little", "Moderately", "A lot"))
CHANGE = OptionSet("change", ("No change noticed", "More movement", "Less movement",
                              "Not sure"), ordinal=False)
ADHERENCE = OptionSet("adherence", ("No", "Partly", "Yes", "Not applicable"),
                      excluded_from_chart=("Not applicable",))


@dataclass(frozen=True)
class Question:
    key: str
    number: int
    category: str
    text: str
    options: OptionSet
    hint: str = ""


CATEGORIES = (
    ("Eye symptoms", "eye"),
    ("Oral and speech symptoms", "survey"),
    ("Facial movement", "face"),
    ("Daily activities", "calendar"),
    ("Recovery habits", "check"),
)

QUESTIONS: tuple[Question, ...] = (
    Question("eye_dryness", 1, "Eye symptoms", "Do you experience eye dryness?", FREQUENCY),
    Question("eye_tearing", 2, "Eye symptoms", "Have you experienced excessive tearing?",
             FREQUENCY),
    Question("eye_closing_difficulty", 3, "Eye symptoms",
             "Do you experience difficulty closing your eye?", FREQUENCY),
    Question("eye_discomfort", 4, "Eye symptoms",
             "Do you experience discomfort related to your eye?", FREQUENCY),
    Question("speaking_difficulty", 5, "Oral and speech symptoms",
             "Do you experience difficulty speaking?", FREQUENCY),
    Question("drinking_difficulty", 6, "Oral and speech symptoms",
             "Do you experience difficulty drinking liquids?", FREQUENCY),
    Question("food_collecting", 7, "Oral and speech symptoms",
             "Do you notice food collecting on one side of your mouth?", FREQUENCY),
    Question("involuntary_movements", 8, "Facial movement",
             "Have you noticed involuntary facial movements?", FREQUENCY,
             "For example, an eye closing when you smile or eat."),
    Question("muscle_stiffness", 9, "Facial movement",
             "Have you noticed stiffness or tightness in your facial muscles?", FREQUENCY),
    Question("movement_change", 10, "Facial movement",
             "Have you noticed changes in facial movement since your last check-in?", CHANGE,
             "Your own impression only — there is no right or wrong answer."),
    Question("impact_eating", 11, "Daily activities",
             "Have facial symptoms affected eating?", IMPACT),
    Question("impact_communication", 12, "Daily activities",
             "Have facial symptoms affected communication?", IMPACT),
    Question("impact_daily", 13, "Daily activities",
             "Have facial symptoms affected your daily activities?", IMPACT),
    Question("exercises_completed", 14, "Recovery habits",
             "Have you completed your recommended exercises?", ADHERENCE,
             "Choose “Not applicable” if no exercises have been recommended to you."),
    Question("eye_care_followed", 15, "Recovery habits",
             "Have you followed your recommended eye-care routine, if applicable?", ADHERENCE),
)

QUESTION_BY_KEY = {q.key: q for q in QUESTIONS}
