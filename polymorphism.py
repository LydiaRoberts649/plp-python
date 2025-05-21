class car:
    def moving():
        return "driving"
    
    class plane:
        def moving():
            return "Flying"

for objects in [car(), plane()]:
    print(object.moving())