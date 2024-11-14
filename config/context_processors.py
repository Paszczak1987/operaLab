from django.urls import resolve


def breadcrumbs(request):
    url_name = resolve(request.path_info).url_name
    app_name = resolve(request.path_info).app_name  # Pobierz nazwę aplikacji
    
    print(f"URL_NAME: {url_name} APP_NAME: {app_name}")
    
    breadcrumb_paths = {}
    # Logika breadcrumbs z podziałem na aplikacje
    if app_name == 'home':
        breadcrumb_paths = {
            'home': [{'name': 'OperaLab', 'url': 'home:home'}, {'name': 'About'}]
        }
    elif app_name == 'labs':
        print("IN_LABS")
        breadcrumb_paths = {
            'home': [{'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Laboratory manager', 'url': 'labs:home'}, {'name': 'About'}],
            'list': [{'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Laboratory manager', 'url': 'labs:home'}, {'name': 'List'}],
            'add': [{'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Laboratory manager', 'url': 'labs:home'}, {'name': 'Create'}],
            
        }
    elif app_name == 'personnel':
        print("IN_PERSONNEL")
        breadcrumb_paths = {
            'home': [{'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Personnel'}],
            'list': [{'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Personnel', 'url': 'personnel:home'}, {'name': 'List'}],
        }
    else:
        print("IN_ELSE")
        breadcrumb_paths = {}

    return {'breadcrumbs': breadcrumb_paths.get(url_name, [])}
