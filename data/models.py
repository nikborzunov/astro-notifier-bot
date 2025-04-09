# Models for storing asteroid, event, and photo data

class Asteroid:
    def __init__(self, name, closest_approach_date, distance):
        self.name = name
        self.closest_approach_date = closest_approach_date
        self.distance = distance

class Event:
    def __init__(self, name, date, description):
        self.name = name
        self.date = date
        self.description = description

class Photo:
    def __init__(self, title, url, date):
        self.title = title
        self.url = url
        self.date = date
