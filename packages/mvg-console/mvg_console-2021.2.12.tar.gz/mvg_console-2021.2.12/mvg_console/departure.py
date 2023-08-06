from colr import color


class Departure:
    
    def __init__( self, json ):
        self.label = json["label"]
        self.destination = json["destination"]
        self.departure_time_minutes = json["departureTimeMinutes"]
        self.line_background_color = json["lineBackgroundColor"]
        self.product = json["product"]


    def get_label_colored(self):
        return color(self.label, fore="#fff", back=self.line_background_color)
    
    def __str__(self):
        label = self.get_label_colored()
        direction = self.destination
        departure_min = self.departure_time_minutes

        return label + "\t" + direction + "\t" + str(departure_min)
