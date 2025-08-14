import random
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from directory.models import Skill, Offer, Request

User = get_user_model()

# Realistic names for more diverse users
FIRST_NAMES = [
    'Alex', 'Jordan', 'Sam', 'Taylor', 'Casey', 'Morgan', 'Riley', 'Quinn',
    'Avery', 'Blake', 'Cameron', 'Drew', 'Emery', 'Finley', 'Gray', 'Hayden',
    'Jamie', 'Kendall', 'Logan', 'Mason', 'Noah', 'Parker', 'Reese', 'Sage',
    'Skyler', 'Tyler', 'Vaughn', 'Wren', 'Zion', 'Adrian', 'Brook', 'Cedar',
    'Dakota', 'Eden', 'Fern', 'Gale', 'Harper', 'Indigo', 'Jade', 'Kai',
    'Lane', 'Meadow', 'Nova', 'Ocean', 'Phoenix', 'River', 'Sky', 'Storm',
    'Willow', 'Zara', 'Atlas', 'Bear', 'Cedar', 'Dove', 'Eagle', 'Fox',
    'Hawk', 'Iris', 'Juniper', 'Lark', 'Maple', 'Nightingale', 'Oak', 'Pine',
    'Quail', 'Raven', 'Sparrow', 'Thrush', 'Violet', 'Wolf', 'Yarrow', 'Zen'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
    'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
    'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
    'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark',
    'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King',
    'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green',
    'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
    'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz',
    'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris',
    'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan',
    'Cooper', 'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos',
    'Kim', 'Cox', 'Ward', 'Richardson', 'Watson', 'Brooks', 'Chavez',
    'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes',
    'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long',
    'Ross', 'Foster', 'Jimenez', 'Powell', 'Jenkins', 'Perry', 'Russell',
    'Sullivan', 'Bell', 'Coleman', 'Butler', 'Henderson', 'Barnes', 'Gonzales'
]

# Realistic usernames based on names
def generate_username(first_name, last_name):
    patterns = [
        f"{first_name.lower()}_{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{random.randint(10, 99)}",
        f"{first_name.lower()}_{random.choice(['dev', 'design', 'tech', 'creative', 'pro'])}",
        f"{first_name.lower()}{random.choice(['2024', '23', '24', '2023'])}",
        f"{first_name.lower()}_{random.choice(['works', 'studio', 'lab', 'hub'])}"
    ]
    return random.choice(patterns)

# Comprehensive skill-specific data
SKILL_DATA = {
    'JavaScript': {
        'titles': [
            'JavaScript Development & Modern ES6+',
            'Frontend JavaScript & React Fundamentals',
            'JavaScript Backend with Node.js',
            'JavaScript Debugging & Performance',
            'JavaScript Testing & Best Practices',
            'JavaScript for Beginners',
            'Advanced JavaScript Patterns',
            'JavaScript API Integration',
            'JavaScript Security & Best Practices',
            'JavaScript Build Tools & Webpack'
        ],
        'descriptions': [
            'Experienced JavaScript developer offering tutoring in modern ES6+, async programming, and real-world project development. I can help you build interactive web applications and understand JavaScript fundamentals.',
            'Frontend specialist with 5+ years building React applications. I can teach you component architecture, state management, and modern JavaScript patterns used in production apps.',
            'Full-stack JavaScript developer specializing in Node.js backend development. Learn server-side JavaScript, API design, database integration, and deployment strategies.',
            'JavaScript debugging expert who can help you troubleshoot complex issues, optimize performance, and understand browser developer tools. Perfect for intermediate developers.',
            'Quality-focused JavaScript developer teaching testing methodologies, TDD practices, and code quality standards. Learn Jest, Mocha, and testing best practices.',
            'Patient teacher offering beginner-friendly JavaScript lessons. We\'ll start with basics and gradually build up to building your first web applications.',
            'Advanced JavaScript concepts including closures, prototypes, design patterns, and functional programming. For developers ready to level up their skills.',
            'API integration specialist teaching how to work with REST APIs, GraphQL, and third-party services using JavaScript. Real-world examples included.',
            'Security-conscious developer teaching JavaScript security best practices, input validation, XSS prevention, and secure coding patterns.',
            'Build tool expert specializing in Webpack, Babel, and modern JavaScript tooling. Learn how to set up efficient development workflows.'
        ]
    },
    'Python': {
        'titles': [
            'Python Programming Fundamentals',
            'Data Science with Python',
            'Python Web Development (Django/Flask)',
            'Python Automation & Scripting',
            'Python for Machine Learning',
            'Python API Development',
            'Python Testing & Debugging',
            'Python Database Integration',
            'Python Security & Best Practices',
            'Python DevOps & Deployment'
        ],
        'descriptions': [
            'Experienced Python developer offering comprehensive programming lessons. From basic syntax to advanced concepts, I can help you build real-world applications.',
            'Data science professional teaching Python for analytics, pandas, numpy, and visualization libraries. Perfect for beginners transitioning to data science.',
            'Web development specialist with Django and Flask experience. Learn full-stack Python development, database design, and deployment strategies.',
            'Automation expert teaching Python scripting for productivity, web scraping, file processing, and system administration tasks.',
            'ML engineer offering Python lessons focused on scikit-learn, TensorFlow, and practical machine learning applications. Real project examples included.',
            'API development specialist teaching RESTful API design, FastAPI, and microservices architecture using Python. Industry best practices covered.',
            'Testing expert offering lessons in pytest, unittest, and debugging techniques. Learn how to write maintainable, testable Python code.',
            'Database specialist teaching SQLAlchemy, PostgreSQL integration, and data modeling with Python. Real-world database design patterns.',
            'Security-focused developer teaching Python security best practices, input validation, and secure coding patterns for production applications.',
            'DevOps engineer specializing in Python deployment, Docker, CI/CD pipelines, and cloud infrastructure. Learn production-ready deployment strategies.'
        ]
    },
    'Barista Skills': {
        'titles': [
            'Professional Barista Training',
            'Coffee Brewing & Latte Art',
            'Espresso Machine Mastery',
            'Coffee Bean Selection & Roasting',
            'Cafe Management & Customer Service',
            'Specialty Coffee Preparation',
            'Milk Steaming & Texturing',
            'Coffee Equipment Maintenance',
            'Coffee Tasting & Cupping',
            'Home Barista Setup & Skills'
        ],
        'descriptions': [
            'Certified barista with 8 years of experience in specialty coffee shops. I can teach you everything from basic brewing to advanced latte art techniques.',
            'Latte art specialist offering hands-on training in milk steaming, texturing, and creating beautiful designs. Perfect for aspiring baristas.',
            'Espresso machine expert teaching proper extraction, grind adjustment, and machine maintenance. Learn the fundamentals of great espresso.',
            'Coffee roaster and bean expert teaching coffee origins, roasting profiles, and how to select the perfect beans for different brewing methods.',
            'Cafe manager with experience in customer service, workflow optimization, and team management. Learn both technical skills and business operations.',
            'Specialty coffee preparation expert teaching pour-over, French press, AeroPress, and other brewing methods. Discover your perfect cup.',
            'Milk steaming specialist focusing on proper technique, temperature control, and creating silky microfoam for perfect lattes and cappuccinos.',
            'Equipment maintenance expert teaching proper cleaning, calibration, and troubleshooting for espresso machines and grinders.',
            'Coffee cupping specialist teaching how to evaluate coffee quality, identify flavor profiles, and develop your palate for coffee tasting.',
            'Home barista setup consultant helping you choose equipment, set up your coffee station, and develop skills for home brewing excellence.'
        ]
    },
    'Copywriting': {
        'titles': [
            'Professional Copywriting & Content Creation',
            'Marketing Copy & Conversion Optimization',
            'Brand Voice & Messaging Strategy',
            'SEO Content Writing',
            'Social Media Copywriting',
            'Email Marketing Copy',
            'Website Copy & UX Writing',
            'Creative Writing & Storytelling',
            'Technical Writing & Documentation',
            'Copywriting for Small Businesses'
        ],
        'descriptions': [
            'Professional copywriter with 10+ years creating compelling content for brands. I can teach you persuasive writing techniques and content strategy.',
            'Conversion optimization specialist teaching how to write copy that drives action. Learn psychological triggers, A/B testing, and ROI-focused writing.',
            'Brand strategist helping you develop unique voice, messaging frameworks, and consistent brand communication across all channels.',
            'SEO content expert teaching keyword research, on-page optimization, and writing content that ranks while engaging readers.',
            'Social media specialist offering training in platform-specific copywriting, engagement strategies, and viral content creation.',
            'Email marketing expert teaching persuasive email sequences, subject line optimization, and conversion-focused email copywriting.',
            'UX writer helping you create clear, user-friendly website copy that guides visitors and improves conversion rates.',
            'Creative writer specializing in storytelling, brand narratives, and emotional connection through words. Perfect for brand building.',
            'Technical writer teaching how to create clear documentation, user guides, and complex information in accessible language.',
            'Small business copywriting specialist helping entrepreneurs create effective marketing materials, website copy, and brand messaging.'
        ]
    },
    'French': {
        'titles': [
            'French Conversation & Fluency',
            'French Grammar & Writing',
            'Business French & Professional Communication',
            'French Literature & Culture',
            'French Pronunciation & Accent Reduction',
            'French for Travel & Daily Life',
            'French Exam Preparation (DELF/TCF)',
            'French Translation & Interpretation',
            'French for Children & Beginners',
            'French Immersion & Cultural Exchange'
        ],
        'descriptions': [
            'Native French speaker offering conversational practice and fluency development. Focus on real-world communication and cultural context.',
            'Experienced French teacher specializing in grammar, writing, and academic French. Perfect for students preparing for exams or academic work.',
            'Business French specialist teaching professional communication, business vocabulary, and cultural etiquette for French-speaking workplaces.',
            'French literature and culture expert offering lessons in French literature, history, and cultural understanding. Enrich your French learning.',
            'Pronunciation specialist helping you master French sounds, reduce accent, and speak with confidence. Individualized accent coaching.',
            'Travel-focused French lessons covering essential vocabulary, phrases, and cultural tips for visiting French-speaking countries.',
            'Exam preparation expert for DELF, TCF, and other French proficiency tests. Structured lessons with practice materials and strategies.',
            'Professional translator offering lessons in French translation techniques, interpretation skills, and cross-cultural communication.',
            'Patient teacher specializing in French for children and absolute beginners. Fun, interactive lessons with games and activities.',
            'Cultural immersion specialist offering French lessons combined with cultural exchange, cooking, music, and authentic French experiences.'
        ]
    },
    'Public Speaking': {
        'titles': [
            'Public Speaking & Presentation Skills',
            'Confidence Building & Stage Presence',
            'Speech Writing & Storytelling',
            'Business Presentations & Pitching',
            'TED Talk Preparation & Delivery',
            'Voice Projection & Vocal Techniques',
            'Audience Engagement & Interaction',
            'Speech Anxiety & Fear Management',
            'Toastmasters & Speaking Clubs',
            'Executive Communication & Leadership'
        ],
        'descriptions': [
            'Professional public speaking coach with 15 years of experience. I can help you overcome stage fright and deliver compelling presentations.',
            'Confidence-building specialist focusing on body language, stage presence, and mental preparation for public speaking success.',
            'Speech writer and storytelling expert teaching how to craft memorable speeches, structure presentations, and connect with audiences.',
            'Business communication specialist helping professionals deliver effective presentations, pitches, and executive communications.',
            'TED Talk coach specializing in idea development, speech crafting, and delivery techniques for impactful presentations.',
            'Voice coach teaching projection, articulation, pacing, and vocal variety for powerful, engaging speaking.',
            'Audience engagement expert teaching how to read crowds, handle questions, and create interactive, memorable presentations.',
            'Anxiety management specialist helping speakers overcome fear, build confidence, and develop mental resilience for public speaking.',
            'Toastmasters mentor guiding you through structured speaking programs and helping you join speaking communities.',
            'Executive communication coach specializing in leadership presentations, boardroom speaking, and high-stakes communication.'
        ]
    },
    'Gardening': {
        'titles': [
            'Organic Gardening & Sustainable Practices',
            'Urban Gardening & Container Growing',
            'Vegetable Gardening & Food Production',
            'Garden Design & Landscape Planning',
            'Plant Care & Maintenance',
            'Seasonal Gardening & Crop Planning',
            'Indoor Plants & Houseplant Care',
            'Garden Pest Management & Natural Solutions',
            'Composting & Soil Health',
            'Garden Photography & Documentation'
        ],
        'descriptions': [
            'Organic gardening expert with 20 years of experience growing food sustainably. Learn natural pest control, soil building, and eco-friendly practices.',
            'Urban gardening specialist teaching container gardening, vertical growing, and maximizing small spaces for abundant harvests.',
            'Vegetable gardening expert helping you grow your own food year-round. From seed starting to harvest, learn complete food production.',
            'Landscape designer offering garden planning, design principles, and creating beautiful, functional outdoor spaces.',
            'Plant care specialist teaching proper watering, fertilizing, pruning, and maintenance for healthy, thriving gardens.',
            'Seasonal gardening expert helping you plan year-round growing, succession planting, and extending your growing season.',
            'Houseplant expert teaching indoor gardening, plant selection, and creating healthy indoor environments for plants.',
            'Integrated pest management specialist teaching natural pest control, beneficial insects, and organic solutions for garden problems.',
            'Soil health expert teaching composting, soil building, and creating rich, fertile soil for optimal plant growth.',
            'Garden photographer helping you document your garden journey, create beautiful plant photos, and share your gardening story.'
        ]
    },
    'Video Editing': {
        'titles': [
            'Video Editing with Adobe Premiere Pro',
            'DaVinci Resolve & Color Grading',
            'YouTube Content Creation & Editing',
            'Social Media Video Production',
            'Documentary & Storytelling Editing',
            'Motion Graphics & After Effects',
            'Video Editing for Beginners',
            'Corporate Video Production',
            'Wedding & Event Video Editing',
            'Video Editing Workflow & Optimization'
        ],
        'descriptions': [
            'Professional video editor with 12 years of experience in Adobe Premiere Pro. Learn editing fundamentals, advanced techniques, and workflow optimization.',
            'DaVinci Resolve specialist teaching professional color grading, editing, and post-production workflows used in film and television.',
            'YouTube content creator helping you edit engaging videos, optimize for platform algorithms, and build your channel through quality editing.',
            'Social media video expert teaching platform-specific editing, vertical video production, and creating viral content for Instagram, TikTok, and more.',
            'Documentary editor specializing in storytelling, narrative structure, and creating compelling non-fiction content that engages audiences.',
            'Motion graphics artist teaching After Effects, animation, and visual effects to enhance your video projects with professional graphics.',
            'Beginner-friendly video editing instructor starting with fundamentals and gradually building to advanced techniques. No prior experience needed.',
            'Corporate video specialist teaching business video production, brand consistency, and creating professional content for companies.',
            'Wedding and event videographer offering editing techniques for capturing and creating beautiful memories from special occasions.',
            'Workflow optimization expert teaching efficient editing processes, project organization, and time-saving techniques for professional editors.'
        ]
    },
    'Data Entry': {
        'titles': [
            'Data Entry & Administrative Support',
            'Excel Spreadsheet Management',
            'Database Entry & Management',
            'Document Processing & Organization',
            'Data Quality & Accuracy Training',
            'Remote Data Entry Work',
            'Data Entry Software & Tools',
            'Administrative Assistant Skills',
            'Data Entry for Small Businesses',
            'Data Entry Speed & Efficiency'
        ],
        'descriptions': [
            'Experienced data entry specialist offering training in accurate, efficient data processing and administrative support skills.',
            'Excel expert teaching spreadsheet management, data organization, and advanced Excel functions for professional data handling.',
            'Database specialist teaching proper data entry techniques, database management, and maintaining data integrity across systems.',
            'Document processing expert helping you organize, categorize, and efficiently process large volumes of documents and information.',
            'Data quality specialist teaching accuracy techniques, error prevention, and maintaining high standards in data entry work.',
            'Remote work expert helping you set up efficient home office systems and find legitimate data entry opportunities online.',
            'Software specialist teaching various data entry tools, automation techniques, and productivity software for efficient work.',
            'Administrative assistant training covering data entry, office management, and professional support skills for business environments.',
            'Small business specialist helping entrepreneurs set up efficient data management systems and processes for their operations.',
            'Speed and efficiency coach teaching techniques to increase data entry speed while maintaining accuracy and quality standards.'
        ]
    }
}

# Realistic posting times spread across different days
def generate_realistic_times():
    now = timezone.now()
    times = []
    
    # Generate times over the last 30 days - create more than we need
    for i in range(100):  # Generate 100 times for 50+ offers/requests
        # Random day within last 30 days (avoid today to ensure past times)
        days_ago = random.randint(1, 30)
        # Random hour of the day (more activity during business hours)
        hour = random.choices(
            range(24),
            weights=[1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 5, 4, 4, 3, 3, 4, 4, 5, 5, 4, 3, 2, 2, 1]
        )[0]
        # Random minute
        minute = random.randint(0, 59)
        
        posting_time = now - timedelta(days=days_ago, hours=hour, minutes=minute)
        times.append(posting_time)
    
    return times

def create_users():
    users = []
    for i in range(25):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = generate_username(first_name, last_name)
        email = f"{username}@example.com"
        
        # Create user with realistic profile
        user = User.objects.create_user(
            username=username,
            email=email,
            password='demodemo',
            first_name=first_name,
            last_name=last_name
        )
        
        # Add profile info if the model supports it
        if hasattr(user, 'profile'):
            user.profile.bio = f"Passionate about sharing knowledge and helping others learn. Based in {random.choice(['San Francisco', 'New York', 'London', 'Berlin', 'Toronto', 'Sydney', 'Remote'])}."
            user.profile.save()
        
        users.append(user)
        print(f"Created user: {first_name} {last_name} ({username})")
    
    return users

def create_offers_requests(users, skills):
    # Generate realistic posting times
    posting_times = generate_realistic_times()
    random.shuffle(posting_times)
    
    offers_created = 0
    requests_created = 0
    
    for skill in skills:
        skill_name = skill.name
        if skill_name in SKILL_DATA:
            skill_data = SKILL_DATA[skill_name]
            
            # Create 3-5 offers per skill
            num_offers = random.randint(3, 5)
            for i in range(num_offers):
                user = random.choice(users)
                title = random.choice(skill_data['titles'])
                description = random.choice(skill_data['descriptions'])
                posting_time = posting_times.pop() if posting_times else (timezone.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23), minutes=random.randint(1, 59)))
                
                # Realistic hour values based on skill complexity
                hour_value = random.choice([0.5, 1.0, 1.5, 2.0, 2.5, 3.0])
                
                # Realistic availability options
                availability = random.choice([
                    'Weekdays', 'Weekends', 'Evenings', 'Flexible', 
                    'Mornings', 'Afternoons', 'By appointment', 'Remote only'
                ])
                
                # Realistic locations
                location = random.choice([
                    'San Francisco', 'New York', 'London', 'Berlin', 
                    'Toronto', 'Sydney', 'Remote', 'Chicago', 'Austin',
                    'Seattle', 'Boston', 'Los Angeles', 'Vancouver'
                ])
                
                offer = Offer.objects.create(
                    user=user,
                    skill=skill,
                    title=title,
                    description=description,
                    hour_value=hour_value,
                    availability=availability,
                    location=location,
                    is_active=random.choice([True, True, True, False]),  # 75% active
                    created_at=posting_time
                )
                offers_created += 1
                
                # Create 1-2 requests per skill
                if random.choice([True, False]):
                    request_user = random.choice(users)
                    request_title = f"Looking to learn {skill_name}"
                    request_description = f"I'm interested in learning {skill_name.lower()} and would love to connect with someone who can teach me the fundamentals."
                    request_posting_time = posting_times.pop() if posting_times else (timezone.now() - timedelta(days=random.randint(1, 30), hours=random.randint(1, 23), minutes=random.randint(1, 59)))
                    
                    request = Request.objects.create(
                        user=request_user,
                        skill=skill,
                        title=request_title,
                        description=request_description,
                        hours_needed=random.choice([0.5, 1.0, 1.5, 2.0]),
                        when=random.choice(['Weekends', 'Evenings', 'Flexible', 'Weekdays']),
                        location=random.choice(['San Francisco', 'New York', 'London', 'Berlin', 'Remote']),
                        is_active=random.choice([True, True, False]),  # 67% active
                        created_at=request_posting_time
                    )
                    requests_created += 1
    
    print(f"Created {offers_created} offers and {requests_created} requests")
    return offers_created, requests_created

def run():
    print("Starting SkillBank data seeding...")
    
    # Clear existing data
    Offer.objects.all().delete()
    Request.objects.all().delete()
    User.objects.filter(email__endswith='@example.com').delete()
    
    # Create skills if they don't exist
    skill_names = ['JavaScript', 'Python', 'Barista Skills', 'Copywriting', 'French', 'Public Speaking', 'Gardening', 'Video Editing', 'Data Entry']
    skills = []
    
    for skill_name in skill_names:
        skill, created = Skill.objects.get_or_create(
            name=skill_name,
            defaults={'description': f'Learn {skill_name} from experienced community members'}
        )
        skills.append(skill)
        if created:
            print(f"Created skill: {skill_name}")
    
    # Create users
    users = create_users()
    
    # Create offers and requests
    offers_created, requests_created = create_offers_requests(users, skills)
    
    print(f"\nSeeding complete!")
    print(f"Created {len(users)} users")
    print(f"Created {offers_created} offers")
    print(f"Created {requests_created} requests")
    print(f"Demo login: alex_smith@example.com / demodemo")


