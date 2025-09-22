
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def run_tests():
    # Setup Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    django.setup()
    
 
    sys.path.insert(0, os.path.join(settings.BASE_DIR, 'apps'))
    
  
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    

    test_paths = [
        'core.tests',
        'customers.tests', 
        'products.tests',
        'orders.tests',
        'dashboard.tests',
    ]
    
    failures = test_runner.run_tests(test_paths)
    sys.exit(bool(failures))

if __name__ == '__main__':
    run_tests()