# BandMates
Advanced Software Engineering FS24 Group Project

## Team PECY
Pia Rosebelle M. Dela Paz \
Efe Saman \
Cagla Ataoglu \
Yaren Durgun \
Marika Thors

## How to run Bandmates
### Backend
1. Navigate to directory 'bandmates'
2. Make sure the docker engine is running on your machine
3. Run the following command: \
  `docker-compose up --build`

### Frontend
1. Navigate to directory 'bandmates-app'
2. If vite is not installed, run: \
   `npm create vite@latest` \
   `npm install vite`
3. Run the following command: \
   `npm run dev`


### Unit tests
Prerequisite: Make sure to have moto v2.0.0 installed, newer versions are not guaranteed to work, as well as pytest and unittest.
1. Go to microservice with a test file in the command line.
2. Run `pytest -p no:warnings test_<name of service>_service.py`
Alternatively to run all tests at once:
1. Go to root of project
2. Run `pytest -p no:warnings`
