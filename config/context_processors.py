from django.urls import resolve, reverse
from labs.models import Laboratory
from personnel.models import Employee


def breadcrumbs(request):
    url_name = resolve(request.path_info).url_name
    app_name = resolve(request.path_info).app_name
    
    print(f"URL_NAME: {url_name} APP_NAME: {app_name}")
    
    # Breadcrumbs ligic with applications division
    if app_name == 'home':
        breadcrumb_paths = {
            'home': [
                {'name': 'OperaLab', 'url': 'home:home'}, {'name': 'home'}
            ]
        }
    elif app_name == 'labs':
        lab_name = ''
        if url_name == 'detail_view':
            lab_name = Laboratory.objects.get(pk=request.resolver_match.kwargs['pk']).short_name
    
        breadcrumb_paths = {
            'home': [
                {'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Laboratory manager', 'url': 'labs:home'}, {'name': 'home'}
            ],
            'list': [
                {'name': 'OperaLab', 'url': 'home:home'},
                {'name': 'Laboratory manager', 'url': 'labs:home'}, {'name': 'List'}
            ],
            'add': [
                {'name': 'OperaLab', 'url': 'home:home'},
                {'name': 'Laboratory manager', 'url': 'labs:home'}, {'name': 'Create'}
            ],
            'detail_view': [
                {'name': 'OperaLab', 'url': 'home:home'},
                {'name': 'Laboratory manager', 'url': 'labs:home'},
                {'name': 'List', 'url': 'labs:list'},
                {'name': f"{lab_name}"}
            ]
        }
    elif app_name == 'personnel':
        emp_name = ''
        emp_path = ''
        if url_name in ['technician_view', 'lab_manager_view', 'director_view', 'group_manager_view']:
            emp_name = Employee.objects.get(pk=request.resolver_match.kwargs['pk'])
            emp_path = url_name
            
        breadcrumb_paths = {
            'home': [
                {'name': 'OperaLab', 'url': 'home:home'}, {'name': 'Personnel'}
            ],
            'list': [
                {'name': 'OperaLab', 'url': 'home:home'},
                {'name': 'Personnel', 'url': 'personnel:home'}, {'name': 'List'}
            ],
            emp_path: [
                {'name': 'OperaLab', 'url': 'home:home'},
                {'name': 'Personnel', 'url': 'personnel:home'},
                {'name': 'List', 'url': 'personnel:list'},
                {'name': f"{emp_name}"},
            ]
        }
    else:
        print("IN_ELSE")
        breadcrumb_paths = {}
    
    return {'breadcrumbs': breadcrumb_paths.get(url_name, [])}
