"""About: purpose, audience, computer-vision vision, limitations and disclaimer."""

from __future__ import annotations

import customtkinter as ctk

from .. import theme as T
from ..config import APP_NAME, VERSION_LABEL
from ..icons import logo_image
from .base import ResponsiveRow, ScrollPage

TARGET_USERS = (
    "Bell's palsy", "Facial nerve injury", "Facial nerve reconstruction or reanimation",
    "Acoustic neuroma surgery", "Other conditions affecting facial nerve function",
)

CV_FUTURE = (
    ("Standardised capture", "Guided expressions, framing and lighting checks could make "
                             "home recordings more comparable from session to session."),
    ("Objective movement tracking", "Facial landmarks can quantify how far specific points move "
                                    "during an expression, on each side of the face."),
    ("Longitudinal overview", "Organised trends across weeks and months could help patients and "
                              "clinicians review progress together between appointments."),
    ("Clinician-ready summaries", "Structured exports could complement established clinical "
                                  "grading systems — after proper validation."),
)

LIMITATIONS = (
    "Measurements are experimental and have not been compared against clinical grading scales "
    "or validated in any study.",
    "Results change with lighting, camera position, distance, head angle, facial hair, glasses "
    "and camera quality.",
    "Head rotation (turning left/right) cannot be fully corrected from a single 2-D camera.",
    "The landmark model was not designed for or tested on facial paralysis; its accuracy on "
    "asymmetric faces is unknown.",
    "Synkinesis, muscle tone and other clinically important features are not measured.",
    "The software has not undergone a formal security review or quality-management process.",
)

NOT_STATEMENTS = (
    "Is not a medical device.",
    "Has not been clinically validated.",
    "Does not diagnose any condition.",
    "Does not recommend treatments.",
    "Does not replace healthcare professionals.",
    "Uses experimental computer-vision calculations, where available.",
)


class AboutPage(ScrollPage):
    key = "about"

    def __init__(self, master, app):
        super().__init__(master, app)
        hero = ctk.CTkFrame(self.body, fg_color=T.NAVY, corner_radius=20)
        hero.grid(row=0, column=0, sticky="ew")
        hero.grid_columnconfigure(1, weight=1)
        img = ctk.CTkImage(light_image=logo_image(256), dark_image=logo_image(256), size=(96, 96))
        ctk.CTkLabel(hero, text="", image=img).grid(row=0, column=0, rowspan=3, padx=(34, 24),
                                                    pady=30)
        ctk.CTkLabel(hero, text=APP_NAME, font=T.font(28, "bold"), text_color=T.WHITE,
                     anchor="w").grid(row=0, column=1, sticky="sw", pady=(30, 0))
        ctk.CTkLabel(hero, text=VERSION_LABEL, font=T.font(13, "bold"), text_color=T.TEAL,
                     anchor="w").grid(row=1, column=1, sticky="w")
        purpose = ctk.CTkLabel(
            hero, text="A local, privacy-conscious prototype that helps people recovering from "
                       "facial nerve conditions complete standardised check-ins, organise "
                       "symptom information, record facial movement and review their history "
                       "over time — information that patients and clinicians can look at "
                       "together.", font=T.font(14), text_color="#C9D5E8", anchor="w",
            justify="left", wraplength=720)
        purpose.grid(row=2, column=1, sticky="nw", pady=(8, 30), padx=(0, 34))
        T.bind_wraplength(purpose, hero, margin=200, minimum=320)

        row = ResponsiveRow(self.body, breakpoints=((1000, 2), (0, 1)), gap=20)
        row.grid(row=1, column=0, sticky="ew", pady=(22, 0))

        users = T.Card(row)
        users.grid_columnconfigure(0, weight=1)
        T.card_title(users, "Who it is for", "People tracking recovery of facial movement after:",
                     "profile").grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        for i, u in enumerate(TARGET_USERS, start=1):
            f = ctk.CTkFrame(users, fg_color=T.SURFACE_ALT, corner_radius=10)
            f.grid(row=i, column=0, sticky="ew", padx=22, pady=3)
            ctk.CTkLabel(f, text="", image=T.icon("check", T.TEAL, 14)).pack(side="left",
                                                                            padx=(12, 8), pady=8)
            ctk.CTkLabel(f, text=u, font=T.font(13), text_color=T.TEXT).pack(side="left")
        ctk.CTkFrame(users, fg_color="transparent", width=1, height=16).grid(row=20, column=0)
        row.add(users)

        not_card = T.Card(row, border_color="#FDE68A")
        not_card.grid_columnconfigure(0, weight=1)
        T.card_title(not_card, "Important disclaimer", "This application:", "warning",
                     T.BLUE).grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        for i, s in enumerate(NOT_STATEMENTS, start=1):
            f = ctk.CTkFrame(not_card, fg_color=T.AMBER_SOFT, corner_radius=10)
            f.grid(row=i, column=0, sticky="ew", padx=22, pady=3)
            ctk.CTkLabel(f, text=s, font=T.font(13, "bold"), text_color=T.AMBER,
                         anchor="w").pack(side="left", padx=14, pady=8)
        ctk.CTkLabel(not_card, text="Always follow the advice of your healthcare team. Seek "
                     "medical care promptly for new weakness, eye pain or redness, or any "
                     "symptom that worries you.", font=T.font(12), text_color=T.GRAY,
                     anchor="w", justify="left", wraplength=420).grid(
            row=20, column=0, sticky="w", padx=22, pady=(10, 20))
        row.add(not_card)

        cv = T.Card(self.body)
        cv.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        cv.grid_columnconfigure(0, weight=1)
        T.card_title(cv, "How computer vision could support recovery tracking",
                     "The long-term vision — none of this is a validated capability today.",
                     "face", T.TEAL).grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 12))
        grid = ResponsiveRow(cv, breakpoints=((900, 4), (560, 2), (0, 1)), gap=14)
        grid.grid(row=1, column=0, sticky="ew", padx=22)
        for title, text in CV_FUTURE:
            f = ctk.CTkFrame(grid, fg_color=T.SURFACE_ALT, corner_radius=12)
            f.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(f, text=title, font=T.font(13, "bold"), text_color=T.HEADING,
                         anchor="w").grid(row=0, column=0, sticky="w", padx=14, pady=(12, 2))
            lbl = ctk.CTkLabel(f, text=text, font=T.font(12), text_color=T.GRAY, anchor="w",
                               justify="left", wraplength=200)
            lbl.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 14))
            T.bind_wraplength(lbl, f, margin=30, minimum=160)
            grid.add(f)
        how = ctk.CTkLabel(
            cv, text="In this prototype, the MediaPipe Face Landmarker locates 478 points on the "
                     "face in each camera frame, entirely on this computer. During each guided "
                     "expression the app measures distances between selected points — for "
                     "example how far each mouth corner moves toward the eye during a smile — "
                     "and expresses them relative to the distance between the eyes. These are "
                     "demonstrations of what landmark geometry can capture, not clinical "
                     "measurements.", font=T.font(12), text_color=T.TEXT, anchor="w",
            justify="left", wraplength=900)
        how.grid(row=2, column=0, sticky="w", padx=22, pady=(16, 20))
        T.bind_wraplength(how, cv, margin=50, minimum=300)

        lim = T.Card(self.body)
        lim.grid(row=3, column=0, sticky="ew", pady=(20, 0))
        lim.grid_columnconfigure(0, weight=1)
        T.card_title(lim, "Current prototype limitations", None, "about").grid(
            row=0, column=0, sticky="ew", padx=22, pady=(20, 10))
        for i, text in enumerate(LIMITATIONS, start=1):
            lbl = ctk.CTkLabel(lim, text=f"•  {text}", font=T.font(12), text_color=T.TEXT,
                               anchor="w", justify="left", wraplength=900)
            lbl.grid(row=i, column=0, sticky="w", padx=26, pady=2)
            T.bind_wraplength(lbl, lim, margin=60, minimum=300)
        ctk.CTkLabel(lim, text="Face landmark model: MediaPipe Face Landmarker (Google, Apache "
                     "License 2.0). Interface built with CustomTkinter, OpenCV and Matplotlib.",
                     font=T.font(11), text_color=T.GRAY_LIGHT, anchor="w", justify="left",
                     wraplength=900).grid(row=20, column=0, sticky="w", padx=22, pady=(12, 20))
