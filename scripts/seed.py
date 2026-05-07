"""
Seed script for Jobs4Hire database.
Populates with realistic test data for companies, developers, jobs, and applications.
"""
import asyncio
import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.company import Company
from app.models.developer import Developer
from app.models.job import Job
from app.models.application import Application
from app.config import settings


# Sample data
COMPANIES = [
    ("TechFlow", "Berlin", "We build scalable cloud infrastructure for European startups", "techflow.io"),
    ("DataMinds", "Amsterdam", "AI-powered analytics for e-commerce", "dataminds.nl"),
    ("GreenCode", "Stockholm", "Sustainable tech solutions for climate change", "greencode.se"),
    ("FinanceX", "Paris", "Next-gen banking APIs and payment solutions", "financex.fr"),
    ("HealthHub", "Copenhagen", "Digital health platform connecting patients and doctors", "healthhub.dk"),
    ("CloudNine", "Dublin", "Multi-cloud orchestration and DevOps automation", "cloudnine.ie"),
    ("CodeCraft", "Barcelona", "Custom software development for enterprise", "codecraft.es"),
    ("ByteBuilders", "Zurich", "Blockchain infrastructure and Web3 tools", "bytebuilders.ch"),
    ("NexusLabs", "Vienna", "IoT and smart city solutions", "nexuslabs.at"),
    ("FlowState", "Lisbon", "Productivity and collaboration tools for remote teams", "flowstate.pt"),
]

SKILLS = {
    "backend": ["Python", "Go", "Rust", "Node.js", "Java", "C#", "Ruby", "Elixir", "PHP"],
    "frontend": ["React", "Vue.js", "Angular", "Svelte", "TypeScript", "JavaScript", "Next.js", "Tailwind"],
    "data": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch", "Kafka", "Snowflake"],
    "devops": ["Docker", "Kubernetes", "Terraform", "AWS", "GCP", "Azure", "CI/CD", "Ansible"],
    "mobile": ["React Native", "Swift", "Kotlin", "Flutter"],
    "other": ["GraphQL", "REST", "Microservices", "Machine Learning", "Blockchain"],
}

SENIORITIES = ["junior", "mid", "senior", "staff", "principal"]
LOCATIONS = ["Berlin", "Amsterdam", "London", "Paris", "Barcelona", "Stockholm", "Copenhagen", "Dublin", "Remote"]
JOB_TYPES = ["contract", "permanent", "both"]
REMOTE_POLICIES = ["remote", "hybrid", "onsite"]


def random_skills(category_weights=None):
    """Generate random skills dict with experience years."""
    if category_weights is None:
        category_weights = {"backend": 3, "frontend": 2, "data": 2, "devops": 2, "other": 1}
    
    skills = {}
    for category, weight in category_weights.items():
        num_skills = random.randint(1, min(weight, len(SKILLS[category])))
        selected = random.sample(SKILLS[category], num_skills)
        for skill in selected:
            skills[skill] = random.randint(1, 8)
    return skills


def generate_job_description(title, company_name, skills):
    """Generate a realistic job description."""
    return f"""We are looking for a talented {title} to join our team at {company_name}.

**Responsibilities:**
- Design and develop scalable software solutions
- Collaborate with cross-functional teams
- Participate in code reviews and architectural decisions
- Mentor junior team members

**Requirements:**
- {random.randint(2, 5)}+ years of professional experience
- Strong proficiency in {', '.join(list(skills)[:3])}
- Experience with agile methodologies
- Excellent communication skills

**What we offer:**
- Competitive salary and equity
- Flexible working hours and remote options
- Professional development budget
- Modern tech stack and tools
"""


async def seed_database():
    """Main seed function."""
    engine = create_async_engine(settings.database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        print("🌱 Seeding database...")

        # 1. Create companies
        print("\n📊 Creating companies...")
        companies = []
        for name, location, description, website in COMPANIES:
            employee_count = random.choice([10, 25, 50, 100, 250, 500])
            if employee_count <= 10:
                size = "1-10"
            elif employee_count <= 50:
                size = "11-50"
            elif employee_count <= 200:
                size = "51-200"
            elif employee_count <= 1000:
                size = "201-1000"
            else:
                size = "1000+"
            
            company = Company(
                name=name,
                slug=name.lower().replace(" ", "-"),
                location=location,
                description=description,
                website_url=f"https://{website}",
                logo_url=f"https://logo.clearbit.com/{website}",
                size=size,
                verified=random.choice([True, False]),
                response_rate=random.randint(70, 100) if random.random() > 0.3 else None,
            )
            companies.append(company)
            session.add(company)
        
        await session.commit()
        print(f"✅ Created {len(companies)} companies")

        # 2. Create developers
        print("\n👨‍💻 Creating developers...")
        first_names = ["Alex", "Sam", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Jamie", "Avery", "Quinn",
                       "Elena", "Marco", "Sofia", "Lucas", "Nina", "Oscar", "Emma", "Felix", "Mia", "Noah",
                       "Lena", "Max", "Anna", "Leo", "Zoe", "Hugo", "Lily", "Theo", "Eva", "Ben"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Martinez", "Rodriguez",
                      "Müller", "Schmidt", "Andersson", "Hansen", "van der Berg", "de Vries", "O'Connor"]
        
        developers = []
        for i in range(30):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            seniority = random.choice(SENIORITIES)
            
            # Skill distribution based on seniority
            if seniority in ["junior"]:
                skills = random_skills({"backend": 2, "frontend": 1, "data": 1})
                years_exp = random.randint(0, 2)
                rate_multiplier = 1.0
            elif seniority == "mid":
                skills = random_skills({"backend": 3, "frontend": 2, "data": 2, "devops": 1})
                years_exp = random.randint(2, 5)
                rate_multiplier = 1.5
            elif seniority == "senior":
                skills = random_skills({"backend": 3, "frontend": 2, "data": 2, "devops": 2, "other": 1})
                years_exp = random.randint(5, 10)
                rate_multiplier = 2.0
            else:  # staff, principal
                skills = random_skills({"backend": 4, "frontend": 3, "data": 3, "devops": 3, "other": 2})
                years_exp = random.randint(10, 15)
                rate_multiplier = 2.5

            developer = Developer(
                email=f"{first_name.lower()}.{last_name.lower()}{i}@example.com",
                full_name=full_name,
                location=random.choice(LOCATIONS),
                bio=f"Passionate {seniority} developer with {years_exp} years of experience building modern web applications.",
                availability=random.choice(["open_contract", "open_fulltime", "both"]),
                hourly_rate_min=int(50 * rate_multiplier),
                hourly_rate_max=int(100 * rate_multiplier),
                daily_rate_min=int(400 * rate_multiplier),
                daily_rate_max=int(800 * rate_multiplier),
                salary_min=int(50000 * rate_multiplier),
                salary_max=int(90000 * rate_multiplier),
                remote_preference=random.choice(REMOTE_POLICIES),
                skills=skills,
                total_years_experience=years_exp,
                seniority=seniority,
                github_username=f"{first_name.lower()}{last_name.lower()}{i}",
                email_verified=random.choice([True, False]),
                languages_spoken=random.sample(["English", "German", "French", "Spanish", "Dutch"], random.randint(2, 4)),
            )
            developers.append(developer)
            session.add(developer)
        
        await session.commit()
        print(f"✅ Created {len(developers)} developers")

        # 3. Create jobs
        print("\n💼 Creating jobs...")
        job_titles = [
            "Senior Backend Engineer",
            "Frontend Developer",
            "Full Stack Engineer",
            "DevOps Engineer",
            "Data Engineer",
            "Machine Learning Engineer",
            "React Developer",
            "Python Developer",
            "Go Developer",
            "Cloud Architect",
            "Platform Engineer",
            "Mobile Developer",
            "Technical Lead",
            "Staff Engineer",
            "Solutions Architect",
            "Database Administrator",
            "Site Reliability Engineer",
            "Security Engineer",
            "Blockchain Developer",
            "AI/ML Researcher",
        ]
        
        jobs = []
        for i in range(20):
            company = random.choice(companies)
            title = random.choice(job_titles)
            job_type = random.choice(JOB_TYPES)
            remote_policy = random.choice(REMOTE_POLICIES)
            seniority = random.choice(SENIORITIES)
            
            # Generate relevant skills
            required_skills = random.sample(
                SKILLS["backend"] + SKILLS["frontend"] + SKILLS["devops"],
                random.randint(3, 6)
            )
            nice_to_have = random.sample(
                list(set(SKILLS["backend"] + SKILLS["frontend"] + SKILLS["other"]) - set(required_skills)),
                random.randint(2, 4)
            )
            
            # Salary ranges based on seniority
            if seniority == "junior":
                salary_min, salary_max = 40000, 60000
                hourly_min, hourly_max = 30, 50
            elif seniority == "mid":
                salary_min, salary_max = 55000, 80000
                hourly_min, hourly_max = 50, 80
            elif seniority == "senior":
                salary_min, salary_max = 75000, 110000
                hourly_min, hourly_max = 80, 120
            else:
                salary_min, salary_max = 100000, 150000
                hourly_min, hourly_max = 100, 150

            job = Job(
                company_id=company.id,
                title=title,
                slug=f"{title.lower().replace(' ', '-')}-{company.slug}-{i}",
                description=generate_job_description(title, company.name, required_skills),
                short_description=f"Join {company.name} as a {title}",
                job_type=job_type,
                remote_policy=remote_policy,
                location=company.location if remote_policy != "remote" else None,
                salary_min=salary_min,
                salary_max=salary_max,
                hourly_rate_min=hourly_min if job_type in ["contract", "both"] else None,
                hourly_rate_max=hourly_max if job_type in ["contract", "both"] else None,
                required_skills=required_skills,
                nice_to_have_skills=nice_to_have,
                seniority=seniority,
                experience_years_min=random.randint(1, 5),
                status="active",
                featured=random.choice([True, False, False, False]),  # 25% featured
                expires_at=datetime.utcnow() + timedelta(days=random.randint(30, 90)),
            )
            jobs.append(job)
            session.add(job)
        
        await session.commit()
        print(f"✅ Created {len(jobs)} jobs")

        # 4. Create applications
        print("\n📝 Creating applications...")
        applications = []
        for _ in range(5):
            developer = random.choice(developers)
            job = random.choice(jobs)
            
            # Avoid duplicates
            if any(app.developer_id == developer.id and app.job_id == job.id for app in applications):
                continue
            
            application = Application(
                job_id=job.id,
                developer_id=developer.id,
                cover_letter=f"I am very interested in the {job.title} position at your company. With my {developer.total_years_experience} years of experience and skills in {', '.join(list(developer.skills.keys())[:3])}, I believe I would be a great fit for this role.",
                status=random.choice(["pending", "reviewed", "shortlisted", "rejected"]),
            )
            applications.append(application)
            session.add(application)
            
            # Update job application count
            job.application_count += 1
        
        await session.commit()
        print(f"✅ Created {len(applications)} applications")

        print("\n🎉 Database seeding complete!")
        print(f"\n📊 Summary:")
        print(f"   - Companies: {len(companies)}")
        print(f"   - Developers: {len(developers)}")
        print(f"   - Jobs: {len(jobs)}")
        print(f"   - Applications: {len(applications)}")


if __name__ == "__main__":
    asyncio.run(seed_database())
