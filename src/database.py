#!/usr/bin/python3

import re
import os
from uuid import uuid4
from models.main import Base
from dotenv import load_dotenv
from models.career import Career
from models.roadmap import Roadmap
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError

load_dotenv()

career_paths = [
    "Frontend Engineer",
    "Backend Engineer",
    "Fullstack Developer",
    "Data Scientist",
    "DevOps Engineer",
    "UX Designer",
    "AI Engineer",
    "Technical Writer",
    "Product Manager",
    "Cyber Security",
    "Blockchain Developer",
    "Data Analyst",
    "Android Developer",
    "iOS Developer",
]

roadmaps = {
    career_paths[0]: {
        "link": "https://roadmap.sh/frontend",
        "video": "https://youtu.be/Tef1e9FiSR0?si=T5OI1xEdP0O0I-ZH",
        "guide": "https://guides.codewithmosh.com/frontend-developer-roadmap",
    },
    career_paths[1]: {
        "link": "https://roadmap.sh/backend",
        "video": "https://youtu.be/OeEHJgzqS1k?si=HBeuUsHnqwvwQza1",
        "guide": "https://guides.codewithmosh.com/backend-developer-roadmap",
    },
    career_paths[2]: {
        "link": "https://roadmap.sh/full-stack",
        "video": "https://youtu.be/GxmfcnU3feo?si=qwHZk1vN2RMicG62",
        "guide": "https://guides.codewithmosh.com/web-developer-roadmap",
    },
    career_paths[3]: {
        "link": "https://roadmap.sh/ai-data-scientist",
        "video": "https://youtu.be/9R3X0JoCLyU?si=jWFROS0wn04XuUMi",
        "guide": "https://guides.codewithmosh.com/data-science-roadmap",
    },
    career_paths[4]: {
        "link": "https://roadmap.sh/devops",
        "video": "https://youtu.be/6GQRb4fGvtk?si=RwDYgoCFpZzyw8CJ",
        "guide": "https://guides.codewithmosh.com/devops-roadmap",
    },
    career_paths[5]: {
        "link": "https://roadmap.sh/ux-design",
        "video": "https://youtu.be/HmKwiEmJIdM?si=ALh-JlXxf_sIkeSC",
    },
    career_paths[6]: {
        "link": "https://roadmap.sh/ai-engineer",
        "video": "https://youtu.be/7IgVGSaQPaw?si=CFb9kPNvmXu9VVdx",
        "guide": "https://guides.codewithmosh.com/machine-learning-engineer-roadmap",
    },
    career_paths[7]: {
        "link": "https://roadmap.sh/technical-writer",
        "video": "https://youtu.be/1w1QYR-n1js?si=q--a2oixTNsBXxmS",
    },
    career_paths[8]: {
        "link": "https://roadmap.sh/product-manager",
        "video": "https://youtu.be/kD2vTLNHkhk?si=0tGv5l3Ps8IrIQAe",
    },
    career_paths[9]: {
        "link": "https://roadmap.sh/cyber-security",
        "video": "https://youtu.be/D4fYyu305jg?si=1m_sFRYXrjF7gKYv",
    },
    career_paths[10]: {
        "link": "https://roadmap.sh/blockchain",
        "video": "https://youtu.be/zglv3lCchSo?si=Ecrya2N2boweEJjk",
    },
    career_paths[11]: {
        "link": "https://roadmap.sh/data-analyst",
        "video": "https://youtu.be/YRJbhFLLPyE?si=E_gA8-iHSDrXNQj_",
        "guide": "https://guides.codewithmosh.com/data-analyst-roadmap",
    },
    career_paths[12]: {
        "link": "https://roadmap.sh/android",
        "video": "https://youtu.be/yye7rSsiV6k?si=iT1sJ1ZTSqrE_3ej",
        "guide": "https://guides.codewithmosh.com/mobile-app-developer-roadmap",
    },
    career_paths[13]: {
        "link": "https://roadmap.sh/ios",
        "video": "https://youtu.be/yye7rSsiV6k?si=iT1sJ1ZTSqrE_3ej",
        "guide": "https://guides.codewithmosh.com/mobile-app-developer-roadmap",
    },
}

print("\nConnecting to remote database...")

engine = create_engine(
    f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

Base.metadata.create_all(engine)


class Database:
    def get_session(self):
        return Session(bind=engine)

    def populate_database(self):
        session = self.get_session()

        try:
            existing_career = (
                session.query(Career).filter_by(name=career_paths[0]).first()
            )

            if existing_career:
                return print("\nDatabase already populated...")
        except InvalidRequestError as error:
            print(f"this is an error - {error} but continue")

        print("\nPopulating database needed for Amakuru to work...")

        for career_name in career_paths:
            career = Career(id=uuid4(), name=career_name)

            roadmap_data = roadmaps.get(career_name)

            roadmap = Roadmap(
                id=uuid4(),
                link=roadmap_data["link"],
                video=roadmap_data["video"],
                guide=roadmap_data.get("guide"),
                career=career,
            )

            session.add(career)

            session.add(roadmap)

        # Commit the changes to the database
        session.commit()

        print("\nPopulated database successfully!")

    def get_careers(self, keyword: str):
        session = self.get_session()

        pattern = re.compile(re.escape(keyword), re.IGNORECASE).pattern

        print("\nSearching our Career Database...")

        return session.query(Career).filter(Career.name.op("~")(pattern)).all()
