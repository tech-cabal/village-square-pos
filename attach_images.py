import os
import shutil
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'village_square.settings')
django.setup()

from inventory.models import FoodItem
from django.core.files import File

images = {
    "Jollof Rice": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\jollof_rice_1782260807932.png",
    "Fried Rice": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\fried_rice_1782260816586.png",
    "Pounded Yam": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\pounded_yam_1782260827221.png",
    "Egusi Soup": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\egusi_soup_1782260836561.png",
    "Amala": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\amala_1782260847619.png",
    "Eba": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\eba_1782260856130.png",
    "Ofada Rice": r"C:\Users\HomePC\.gemini\antigravity\brain\2ad4b7e9-e943-4752-8f85-293266bdee20\ofada_rice_1782260865684.png",
}

for name, path in images.items():
    if os.path.exists(path):
        try:
            food = FoodItem.objects.get(name=name)
            with open(path, 'rb') as f:
                filename = os.path.basename(path)
                food.image.save(filename, File(f), save=True)
            print(f"Added image for {name}")
        except FoodItem.DoesNotExist:
            print(f"Food item {name} not found")
    else:
        print(f"Image not found at {path}")

print("Done attaching images.")
