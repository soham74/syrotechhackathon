import random
from decimal import Decimal
from datetime import datetime, timedelta
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

# Realistic offer titles and descriptions
OFFER_DATA = {
    "Web Design": {
        "titles": [
            "Modern Website Design & Development",
            "Responsive Web Design Help",
            "UI/UX Design Consultation",
            "WordPress Site Building",
            "Frontend Development Tutoring"
        ],
        "descriptions": [
            "Professional web designer with 5+ years experience. I can help you create modern, responsive websites using HTML, CSS, and JavaScript. Perfect for beginners or those looking to improve their skills.",
            "Looking to build your portfolio website? I specialize in clean, modern designs that convert. Can work with Figma, Adobe XD, or code from scratch.",
            "Need help with your website project? I offer one-on-one tutoring in web design principles, responsive design, and modern frameworks like React and Vue.js.",
            "WordPress expert here! I can help you set up, customize, and maintain your WordPress site. From themes to plugins, I've got you covered.",
            "Frontend developer offering personalized coding sessions. Learn HTML, CSS, JavaScript, and modern frameworks. Great for students and career changers."
        ]
    },
    "Python": {
        "titles": [
            "Python Programming Tutoring",
            "Data Science with Python",
            "Web Development with Django/Flask",
            "Python for Beginners",
            "Automation Scripts & Tools"
        ],
        "descriptions": [
            "Experienced Python developer offering personalized tutoring. Whether you're a complete beginner or want to learn advanced topics like data science, I can help you master Python programming.",
            "Data scientist with expertise in pandas, numpy, and scikit-learn. Learn how to analyze data, create visualizations, and build machine learning models with Python.",
            "Full-stack developer specializing in Django and Flask. I can teach you how to build web applications, APIs, and deploy them to production. Perfect for aspiring developers.",
            "Patient tutor for Python beginners! I'll help you understand programming fundamentals, work through exercises, and build your first projects. No prior experience needed.",
            "Automation specialist here! Learn how to write Python scripts to automate repetitive tasks, scrape websites, and integrate with APIs. Save hours of manual work."
        ]
    },
    "Gardening": {
        "titles": [
            "Organic Gardening Consultation",
            "Urban Garden Setup & Maintenance",
            "Plant Care & Troubleshooting",
            "Seasonal Gardening Tips",
            "Indoor Plant Care"
        ],
        "descriptions": [
            "Certified master gardener with 10+ years experience. I can help you plan, plant, and maintain a beautiful organic garden. From soil preparation to pest management.",
            "Urban gardening specialist! Learn how to grow food in small spaces, balconies, or community gardens. I'll help you maximize your harvest in limited space.",
            "Having trouble with your plants? I can diagnose issues, recommend solutions, and teach you proper care techniques. From watering schedules to fertilizer needs.",
            "Seasonal gardening expert offering year-round guidance. Learn what to plant when, how to prepare for each season, and maintain a productive garden all year.",
            "Indoor plant enthusiast here! I can help you choose the right plants for your space, teach proper care techniques, and troubleshoot common indoor gardening issues."
        ]
    },
    "Guitar": {
        "titles": [
            "Acoustic Guitar Lessons",
            "Electric Guitar & Rock Techniques",
            "Fingerstyle Guitar Mastery",
            "Music Theory for Guitarists",
            "Songwriting & Arrangement"
        ],
        "descriptions": [
            "Professional guitarist offering personalized acoustic guitar lessons. Learn proper technique, chord progressions, and your favorite songs. All skill levels welcome!",
            "Rock guitarist with 15+ years experience. I can teach you electric guitar techniques, soloing, effects pedals, and how to play like your favorite rock stars.",
            "Fingerstyle specialist here! Learn beautiful fingerpicking patterns, classical techniques, and how to play complex arrangements. Perfect for intermediate players.",
            "Music theory made simple for guitarists! I'll teach you scales, chord construction, and how to understand the music you're playing. No boring textbooks!",
            "Singer-songwriter offering lessons in songwriting, arrangement, and performance. Learn how to write your own songs and develop your unique style."
        ]
    },
    "Cooking": {
        "titles": [
            "Home Cooking Fundamentals",
            "International Cuisine Classes",
            "Meal Prep & Planning",
            "Baking & Pastry Arts",
            "Healthy Cooking Techniques"
        ],
        "descriptions": [
            "Home chef with a passion for teaching! Learn essential cooking techniques, knife skills, and how to create delicious meals from scratch. Perfect for beginners.",
            "Traveled the world and learned to cook! I can teach you authentic dishes from Italy, Thailand, Mexico, and more. Spice up your cooking repertoire.",
            "Meal prep expert here! Learn how to plan, shop, and cook meals for the week. Save time, money, and eat healthier with efficient meal preparation.",
            "Pastry chef offering baking lessons! From bread to cakes, cookies to croissants. Learn the science of baking and create beautiful, delicious treats.",
            "Nutrition-focused cooking instructor. Learn how to cook healthy, flavorful meals that support your wellness goals. From plant-based to Mediterranean cuisine."
        ]
    },
    "Math Tutoring": {
        "titles": [
            "High School Math Support",
            "College Calculus & Statistics",
            "Math Test Prep & Strategies",
            "Math for Adults",
            "STEM Math Applications"
        ],
        "descriptions": [
            "Certified math teacher offering support for algebra, geometry, and trigonometry. I can help you understand concepts, solve problems, and build confidence in math.",
            "Math professor with PhD offering advanced math tutoring. Calculus, linear algebra, statistics, and more. Perfect for college students and professionals.",
            "Test prep specialist! I can help you prepare for SAT, ACT, GRE, or any math exam. Learn strategies, practice problems, and improve your scores.",
            "Math tutor for adults! Whether you're returning to school, changing careers, or just want to improve your math skills, I can help you succeed.",
            "Engineer offering practical math applications. Learn how math is used in science, technology, and everyday problem-solving. Make math relevant and interesting."
        ]
    },
    "House Painting": {
        "titles": [
            "Interior Painting Techniques",
            "Exterior House Painting",
            "Color Consultation & Design",
            "Paint Prep & Surface Repair",
            "Faux Finishing & Textures"
        ],
        "descriptions": [
            "Professional painter with 8+ years experience. I can teach you proper painting techniques, tool selection, and how to achieve professional results on your interior projects.",
            "Exterior painting specialist! Learn how to prepare surfaces, choose the right paint, and apply it correctly for lasting results. Weather-resistant finishes guaranteed.",
            "Color consultant and designer here! I can help you choose the perfect colors for your space, create color schemes, and understand how colors affect mood and perception.",
            "Surface preparation expert! Learn how to repair drywall, sand surfaces, and prepare walls for painting. The key to a professional finish is proper preparation.",
            "Faux finishing artist offering lessons in decorative painting techniques. Learn how to create marble, wood grain, and textured finishes that add character to your home."
        ]
    },
    "Yoga": {
        "titles": [
            "Vinyasa Flow Yoga",
            "Yin Yoga & Meditation",
            "Yoga for Beginners",
            "Therapeutic Yoga",
            "Yoga for Athletes"
        ],
        "descriptions": [
            "Certified yoga instructor specializing in vinyasa flow. Learn proper alignment, breathing techniques, and how to build strength and flexibility through dynamic movement.",
            "Yin yoga and meditation teacher here! Learn gentle, restorative poses and mindfulness techniques. Perfect for stress relief and deep relaxation.",
            "Patient instructor for yoga beginners! I'll guide you through basic poses, breathing exercises, and help you develop a safe, sustainable yoga practice.",
            "Therapeutic yoga specialist offering sessions for back pain, stress, and injury recovery. Learn poses and techniques to support your health and wellness.",
            "Athletic yoga instructor! Learn how yoga can improve your performance in other sports. Focus on flexibility, balance, and injury prevention for athletes."
        ]
    },
    "Copywriting": {
        "titles": [
            "Content Writing & SEO",
            "Sales Copy & Marketing",
            "Creative Writing Workshop",
            "Business Writing Skills",
            "Social Media Content"
        ],
        "descriptions": [
            "Professional copywriter with expertise in SEO and content marketing. I can teach you how to write engaging content that ranks well and converts readers into customers.",
            "Sales copy specialist! Learn how to write compelling headlines, persuasive copy, and marketing materials that drive results. From emails to landing pages.",
            "Creative writing workshop leader. Develop your voice, learn storytelling techniques, and get feedback on your writing. Perfect for aspiring authors and content creators.",
            "Business writing consultant. Learn how to write clear, professional emails, reports, and proposals. Improve your communication skills for the workplace.",
            "Social media expert offering content creation guidance. Learn how to write engaging posts, develop your brand voice, and grow your online presence."
        ]
    },
    "Photography": {
        "titles": [
            "Digital Photography Basics",
            "Portrait Photography",
            "Landscape & Nature Photography",
            "Photo Editing & Post-Processing",
            "Mobile Photography"
        ],
        "descriptions": [
            "Professional photographer teaching digital photography fundamentals. Learn camera settings, composition, lighting, and how to take better photos with any camera.",
            "Portrait photographer specializing in people photography. Learn how to pose subjects, use natural and artificial lighting, and create flattering portraits.",
            "Nature and landscape photographer here! Learn how to capture stunning outdoor scenes, work with natural light, and create dramatic landscape images.",
            "Photo editing expert! Learn Lightroom, Photoshop, and other editing tools. Transform your photos from good to great with professional editing techniques.",
            "Mobile photography specialist! Learn how to take amazing photos with your smartphone. From composition to editing apps, maximize your phone's camera potential."
        ]
    }
}

# Realistic request titles and descriptions
REQUEST_DATA = {
    "Web Design": {
        "titles": [
            "Need help with my portfolio website",
            "Looking for website design guidance",
            "Help with WordPress customization",
            "Need tutoring in web development",
            "Want to learn responsive design"
        ],
        "descriptions": [
            "I'm a graphic designer looking to create a professional portfolio website. Need help with layout, responsive design, and making it stand out to potential clients.",
            "Starting a small business and need a website. Looking for guidance on design, hosting, and getting started with web development. Complete beginner here!",
            "Have a WordPress site but struggling with customization. Need help with themes, plugins, and making it look professional. Can work with your schedule.",
            "Computer science student wanting to improve my web development skills. Looking for a mentor to help me with HTML, CSS, and JavaScript projects.",
            "My website looks terrible on mobile devices. Need help learning responsive design principles and implementing them. Have basic HTML/CSS knowledge."
        ]
    },
    "Python": {
        "titles": [
            "Help with Python project",
            "Need data analysis assistance",
            "Learning Python for automation",
            "Struggling with Django framework",
            "Want to build a web scraper"
        ],
        "descriptions": [
            "Working on a Python project for my coding bootcamp. Need help debugging code and understanding best practices. Have some Python experience but stuck on certain concepts.",
            "Business analyst needing to learn Python for data analysis. Want to work with pandas and create visualizations. Looking for patient tutor who can explain concepts clearly.",
            "Tired of doing repetitive tasks at work. Want to learn Python automation to save time. Need help with scripts for file processing and data manipulation.",
            "Learning Django for a web development project. Understanding the basics but struggling with models, views, and deployment. Need guidance from experienced developer.",
            "Want to build a web scraper to collect data for my research project. Need help with requests, BeautifulSoup, and handling different website structures."
        ]
    },
    "Gardening": {
        "titles": [
            "Help with my vegetable garden",
            "Need advice on indoor plants",
            "Struggling with garden pests",
            "Want to start a balcony garden",
            "Need help with plant identification"
        ],
        "descriptions": [
            "First-time gardener trying to grow vegetables. Plants aren't growing well and I think I'm doing something wrong. Need help with soil, watering, and general care.",
            "Killing all my indoor plants! Need someone to teach me proper care techniques, watering schedules, and how to choose the right plants for my apartment.",
            "My garden is being destroyed by pests. Need help identifying the problem and finding organic solutions. Want to avoid chemical pesticides if possible.",
            "Live in an apartment with a small balcony. Want to grow herbs and vegetables but don't know where to start. Need help with container gardening and space optimization.",
            "Have several plants but don't know what they are or how to care for them. Need help with identification and creating proper care routines for each plant."
        ]
    }
}


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
    
    # Create offers with realistic data
    for _ in range(60):
        user = random.choice(users)
        skill = random.choice(skills)
        
        # Get realistic title and description
        skill_data = OFFER_DATA.get(skill.name, {
            "titles": [f"{skill.name} help"],
            "descriptions": [f"I can help with {skill.name.lower()}."]
        })
        
        title = random.choice(skill_data["titles"])
        description = random.choice(skill_data["descriptions"])
        
        # Add posting date (within last 30 days)
        days_ago = random.randint(0, 30)
        posted_date = datetime.now() - timedelta(days=days_ago)
        
        offer = Offer.objects.create(
            user=user,
            skill=skill,
            title=title,
            description=description,
            hour_value=random.choice([0.5, 1.0, 1.5, 2.0]),
            availability=random.choice(["Weeknights", "Weekends", "Flexible", "Mornings", "Afternoons"]),
            location=random.choice(LOCATIONS),
            is_active=True,
        )
        
        # Set created_at to realistic date
        offer.created_at = posted_date
        offer.save(update_fields=['created_at'])
        offers.append(offer)
    
    # Create requests with realistic data
    for _ in range(40):
        user = random.choice(users)
        skill = random.choice(skills)
        
        # Get realistic title and description
        skill_data = REQUEST_DATA.get(skill.name, {
            "titles": [f"Need {skill.name}"],
            "descriptions": [f"Looking for help with {skill.name.lower()}."]
        })
        
        title = random.choice(skill_data["titles"])
        description = random.choice(skill_data["descriptions"])
        
        # Add posting date (within last 30 days)
        days_ago = random.randint(0, 30)
        posted_date = datetime.now() - timedelta(days=days_ago)
        
        request = Request.objects.create(
            user=user,
            skill=skill,
            title=title,
            description=description,
            hours_needed=random.choice([0.5, 1.0, 2.0, 3.0, 4.0]),
            when=random.choice(["Evenings", "Weekends", "Next week", "This month", "Flexible"]),
            location=random.choice(LOCATIONS),
            is_active=True,
        )
        
        # Set created_at to realistic date
        request.created_at = posted_date
        request.save(update_fields=['created_at'])
        requests.append(request)
    
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


