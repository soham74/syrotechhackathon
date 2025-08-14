# SkillBank — Time-based Skill Swap Platform

> **Building a more connected, equitable world through skill sharing**

## **Social Impact & Problem Statement**

### The Challenge
In today's digital economy, access to education and skill development is often limited by financial barriers. Traditional learning platforms require significant monetary investment, creating inequality in skill acquisition. Additionally, many people have valuable skills to share but lack platforms to exchange them meaningfully.

### Our Solution
**SkillBank** is a revolutionary time-based skill exchange platform that eliminates financial barriers to learning. Instead of money, users trade skills using time credits (1 hour = 1 credit). This creates an equitable ecosystem where anyone can learn new skills regardless of their financial situation.

### Social Impact
- **Democratizing Education**: Makes skill development accessible to everyone
- **Community Building**: Fosters meaningful connections through skill sharing
- **Economic Empowerment**: Enables skill development without financial barriers
- **Sustainable Learning**: Promotes continuous learning and knowledge sharing
- **Social Mobility**: Helps people advance their careers through skill acquisition

## **Features**

### Core Functionality
- **Skill Exchange System**: Offer and request skills using time credits
- **Smart Matching**: Connect learners with teachers based on skills and availability
- **Reputation System**: Build trust through reviews and ratings
- **Digital Wallet**: Track time credits and transaction history
- **Community Features**: Browse, filter, and discover skills

### User Experience
- **Intuitive Interface**: Clean, modern design with vibrant gradients
- **Real-time Updates**: HTMX-powered dynamic content without page reloads
- **Mobile Responsive**: Works seamlessly across all devices
- **Accessibility**: Designed for users of all abilities

### Technical Excellence
- **Modern Stack**: Django 5.x, HTMX, Tailwind CSS
- **Performance**: Optimized database queries and caching
- **Security**: CSRF protection, secure authentication
- **Scalability**: Designed for growth and expansion

## **Technology Stack**

- **Backend**: Django 5.x (Python)
- **Frontend**: HTMX, Tailwind CSS, Django Templates
- **Database**: PostgreSQL (production), SQLite (development)
- **Deployment**: Vercel (serverless)
- **Authentication**: Django's built-in auth system
- **Static Files**: WhiteNoise with service worker

## **Setup Instructions**

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/soham74/syrotechhackathon.git
   cd skillbank
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file
   echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')" > .env
   echo "DEBUG=1" >> .env
   echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed demo data (recommended)**
   ```bash
   python manage.py shell -c "from scripts.seed_data import run; run()"
   ```

8. **Start development server**
   ```bash
   python manage.py runserver
   ```

9. **Visit the application**
   - Homepage: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - Demo login: `alex_smith@example.com` / `demodemo` (after seeding)

### Production Deployment (Vercel)

1. **Fork/clone the repository to your GitHub account**

2. **Set up Vercel project**
   - Connect your GitHub repository to Vercel
   - Set build command: `pip install -r requirements.txt`
   - Set output directory: `api`

3. **Configure environment variables in Vercel**
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=0
   ALLOWED_HOSTS=your-domain.vercel.app
   DATABASE_URL=your-postgresql-connection-string
   ```

4. **Deploy**
   - Vercel will automatically deploy on git push
   - Run migrations: `python manage.py migrate`
   - Seed data: `python manage.py shell -c "from scripts.seed_data import run; run()"`

## **How It Works**

### For Skill Providers
1. **Create an Offer**: List your skills with hourly rates in time credits
2. **Set Availability**: Specify when you're available to teach
3. **Get Matched**: Receive requests from learners
4. **Earn Credits**: Build up your time credit balance
5. **Learn Skills**: Use your credits to learn from others

### For Skill Learners
1. **Browse Skills**: Discover available skills in your area
2. **Request Learning**: Propose matches with skill providers
3. **Spend Credits**: Use your time credits to learn
4. **Build Reputation**: Leave reviews and build your profile
5. **Share Skills**: Offer your own skills to earn credits

### The Credit System
- **1 Hour = 1 Credit**: Simple, transparent exchange rate
- **No Money Involved**: Pure time-based economy
- **Fair Exchange**: Everyone's time has equal value
- **Sustainable**: Encourages continuous learning and teaching

## **Key Features Explained**

### Smart Matching System
- **Skill-based Matching**: Connect users with relevant skills
- **Location Filtering**: Find local or remote opportunities
- **Availability Matching**: Align schedules for optimal learning
- **Reputation Consideration**: Build trust through reviews

### Digital Wallet
- **Credit Tracking**: Monitor your time credit balance
- **Transaction History**: View all skill exchanges
- **Balance Management**: Track incoming and outgoing credits
- **Financial Transparency**: Clear record of all exchanges

### Community Features
- **Skill Directory**: Browse available skills and requests
- **User Profiles**: View reputation and skill history
- **Review System**: Rate and review learning experiences
- **Search & Filter**: Find specific skills or providers

## **Live Demo**

**Visit the live application**: [https://syrotechhackathon.vercel.app/](https://syrotechhackathon.vercel.app/)

**Demo Credentials**:
- Email: `alex_smith@example.com`
- Password: `demodemo`

## **Impact Metrics**

### Potential Social Impact
- **Accessibility**: Eliminates financial barriers to skill development
- **Community**: Fosters meaningful connections through knowledge sharing
- **Equity**: Creates equal opportunities regardless of economic status
- **Sustainability**: Promotes continuous learning and skill development
- **Innovation**: Encourages diverse skill acquisition and knowledge transfer

### Target Users
- **Students**: Learn skills without financial burden
- **Professionals**: Expand skill sets for career advancement
- **Retirees**: Share valuable experience and stay engaged
- **Immigrants**: Learn local skills and build community connections
- **Entrepreneurs**: Access diverse skills for business development

## **Technical Architecture**

### Backend Structure
```
skillbank/
├── accounts/          # User authentication and profiles
├── directory/         # Skill offers and requests
├── matches/          # Matching and exchange system
├── ledger/           # Time credit wallet and transactions
├── reviews/          # Rating and review system
└── core/             # Django settings and configuration
```

### Frontend Components
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dynamic Content**: HTMX for seamless user interactions
- **Modern UI**: Gradient designs and smooth animations
- **Accessibility**: WCAG compliant design patterns

### Database Design
- **User Management**: Profiles, authentication, reputation
- **Skill System**: Categories, offers, requests
- **Matching Engine**: Proposals, acceptances, completions
- **Financial Tracking**: Credits, transactions, balances
- **Review System**: Ratings, feedback, reputation building

## **Future Roadmap**

### Phase 2 Features
- **Video Integration**: Real-time video learning sessions
- **Skill Verification**: Certification and validation system
- **Advanced Matching**: AI-powered skill recommendations
- **Mobile App**: Native iOS and Android applications
- **Community Events**: Skill sharing meetups and workshops

### Phase 3 Expansion
- **Corporate Partnerships**: B2B skill exchange programs
- **Educational Integration**: University and school partnerships
- **International Expansion**: Multi-language support
- **Advanced Analytics**: Learning progress tracking
- **API Development**: Third-party integrations

## **Contributing**

We welcome contributions to make SkillBank even better! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 Python style guidelines
- Write comprehensive tests for new features
- Update documentation for any changes
- Ensure accessibility standards are met

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Acknowledgments**

- **Django Community**: For the amazing web framework
- **Tailwind CSS**: For the beautiful design system
- **HTMX**: For seamless dynamic interactions
- **Vercel**: For reliable deployment platform
- **Syrotech Hackathon**: For the opportunity to build impactful solutions

## **Contact**

- **Project Link**: [https://github.com/soham74/syrotechhackathon](https://github.com/soham74/syrotechhackathon)
- **Live Demo**: [https://syrotechhackathon.vercel.app/](https://syrotechhackathon.vercel.app/)
- **Issues**: [GitHub Issues](https://github.com/soham74/syrotechhackathon/issues)

---

**Built with ❤️ for the Syrotech MVP Hackathon**

*Transforming technical skills into social impact, one skill exchange at a time.*

