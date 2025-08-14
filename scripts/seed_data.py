import random
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from directory.models import Skill, Offer, Request
from matches.models import Match
from ledger.models import Transaction
from reviews.models import Review


FIRST_NAMES = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Riley", "Jamie", "Morgan", "Drew", "Avery",
               "Quinn", "Harper", "Rowan", "Cameron", "Emerson", "Kai", "Hayden", "Jules", "Parker", "Skyler"]

LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

REALISTIC_USERNAMES = [
    "alex_smith", "sam_johnson", "jordan_williams", "taylor_brown", "casey_jones",
    "riley_garcia", "jamie_miller", "morgan_davis", "drew_rodriguez", "avery_martinez",
    "quinn_hernandez", "harper_lopez", "rowan_gonzalez", "cameron_wilson", "emerson_anderson",
    "kai_thomas", "hayden_taylor", "jules_moore", "parker_jackson", "skyler_martin"
]

LOCATIONS = ["NYC", "SF", "Austin", "Seattle", "Chicago", "Remote", "London", "Berlin"]
SKILL_NAMES = [
    "Web Design", "Python", "Gardening", "Guitar", "Cooking", "Math Tutoring", "House Painting", "Yoga",
    "Copywriting", "Photography", "Sewing", "3D Printing", "Bike Repair", "Public Speaking", "Data Entry",
    "Spanish", "French", "JavaScript", "Carpentry", "Illustration", "Video Editing", "Baking", "Dog Training",
    "Singing", "Barista Skills", "Sourdough"
]


def create_users(num=20):
    User = get_user_model()
    users = []
    for i in range(num):
        first_name = FIRST_NAMES[i] if i < len(FIRST_NAMES) else random.choice(FIRST_NAMES)
        last_name = LAST_NAMES[i] if i < len(LAST_NAMES) else random.choice(LAST_NAMES)
        username = REALISTIC_USERNAMES[i] if i < len(REALISTIC_USERNAMES) else f"{first_name.lower()}_{last_name.lower()}"
        email = f"{username}@example.com"
        user, _ = User.objects.get_or_create(username=username, defaults={
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'location': random.choice(LOCATIONS),
            'bio': f"Hi, I'm {first_name} {last_name} and I love helping others learn new skills!",
        })
        user.set_password('demodemo')
        user.save()
        users.append(user)
    return users


def create_skills():
    skills = []
    for name in SKILL_NAMES:
        skill, _ = Skill.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
        skills.append(skill)
    return skills


def create_offers_requests(users, skills):
    offers, requests = [], []
    for _ in range(60):
        user = random.choice(users)
        skill = random.choice(skills)
        offers.append(Offer.objects.create(
            user=user,
            skill=skill,
            title=f"{skill.name} help",
            description=f"I can help with {skill.name.lower()}.",
            hour_value=random.choice([0.5, 1.0, 1.5, 2.0]),
            availability=random.choice(["Weeknights", "Weekends", "Flexible"]),
            location=random.choice(LOCATIONS),
            is_active=True,
        ))
    for _ in range(40):
        user = random.choice(users)
        skill = random.choice(skills)
        requests.append(Request.objects.create(
            user=user,
            skill=skill,
            title=f"Need {skill.name}",
            description=f"Looking for help with {skill.name.lower()}.",
            hours_needed=random.choice([0.5, 1.0, 2.0, 3.0]),
            when=random.choice(["Evenings", "Weekends", "Next week"]),
            location=random.choice(LOCATIONS),
            is_active=True,
        ))
    return offers, requests


def create_matches_transactions_reviews(users, offers, requests):
    accepted, completed = [], []
    for _ in range(10):
        offer = random.choice(offers)
        req = random.choice(requests)
        requester = req.user
        provider = offer.user
        m = Match.objects.create(offer=offer, request=req, requester=requester, provider=provider, agreed_hours=Decimal('1.0'))
        m.status = Match.STATUS_ACCEPTED
        m.save(update_fields=['status'])
        accepted.append(m)
    for _ in range(8):
        offer = random.choice(offers)
        req = random.choice(requests)
        requester = req.user
        provider = offer.user
        m = Match.objects.create(offer=offer, request=req, requester=requester, provider=provider, agreed_hours=Decimal('1.0'))
        Transaction.objects.create(from_user=requester, to_user=provider, hours=Decimal('1.0'), match=m)
        m.status = Match.STATUS_DONE
        m.save(update_fields=['status'])
        # Add reviews from both sides
        Review.objects.create(match=m, rater=requester, ratee=provider, rating=random.randint(3, 5), comment="Great job!")
        Review.objects.create(match=m, rater=provider, ratee=requester, rating=random.randint(3, 5), comment="Pleasure to work with.")
        completed.append(m)
    return accepted, completed


def run():
    print("Seeding demo data...")
    users = create_users()
    skills = create_skills()
    offers, requests = create_offers_requests(users, skills)
    accepted, completed = create_matches_transactions_reviews(users, offers, requests)
    print(f"Seeded demo data: {len(users)} users, {len(skills)} skills, {len(offers)} offers, {len(requests)} requests, {len(accepted)} accepted matches, {len(completed)} completed matches.")
    print("Demo login: alex_smith@example.com / demodemo (after seeding).")


