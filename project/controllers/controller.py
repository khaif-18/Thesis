class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_view(self):
        return self.view.show(self.model)