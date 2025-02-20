from hawk_python_sdk import Hawk
from app.config import settings


hawk = Hawk(settings.HAWK_TOKEN)