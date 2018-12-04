class Records:
    count = 0

    def __init__(self, Recordstitle, description, location, category):
        self.Recordstitle = Recordstitle
        self.description = description
        self.location = location
        self.category = category
        self.id = Records.count
        Records.count += 1


class Category:
    def __init__(self, redflag ,intervention, status):
        self.redflag = redflag
        self.intervention = intervention
        self.status = status