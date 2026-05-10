from fastapi.templating import Jinja2Templates

# Общий объект шаблонов для всей Web-части приложения
# Храним отдельно, чтобы не создавать Jinja2Templates заново в каждом файле с роутерами
templates = Jinja2Templates(directory="app/templates")
