from pathlib import Path
import shutil

base_dir=Path("./File_Organiser_Bot")



for item in base_dir.iterdir():
  if item.is_file() and not item.name=='file_organiser_bot.py':
    destination=Path(base_dir,f"{item.suffix[1:]}_files")
    destination.mkdir(exist_ok=True)
    shutil.move(item,destination)
    

