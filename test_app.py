"""
Test script to validate the AgroVisionNet application structure
"""

import os
import sys

def test_file_structure():
    """Test if all required files exist"""
    print("Testing file structure...")
    
    required_files = [
        'app.py',
        'train_model.py',
        'predict.py',
        'requirements.txt',
        'README.md',
        '.gitignore',
        'templates/index.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✓ All required files present")
        return True

def test_requirements():
    """Test if requirements.txt is valid"""
    print("\nTesting requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.readlines()
        
        required_packages = ['flask', 'tensorflow', 'keras', 'numpy', 'pillow', 'werkzeug']
        found_packages = []
        
        for req in requirements:
            req = req.strip().lower()
            if req and not req.startswith('#'):
                package_name = req.split('==')[0].split('>=')[0].split('<=')[0]
                found_packages.append(package_name)
        
        missing_packages = [pkg for pkg in required_packages if pkg not in found_packages]
        
        if missing_packages:
            print(f"❌ Missing packages in requirements.txt: {missing_packages}")
            return False
        else:
            print(f"✓ All required packages listed: {', '.join(required_packages)}")
            return True
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        return False

def test_app_structure():
    """Test app.py structure"""
    print("\nTesting app.py structure...")
    
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        required_elements = [
            ('Flask app', 'app = Flask(__name__)'),
            ('DISEASE_CLASSES', 'DISEASE_CLASSES = ['),
            ('index route', '@app.route(\'/\')'),
            ('predict route', '@app.route(\'/predict\''),
            ('health route', '@app.route(\'/health\''),
            ('preprocess_image', 'def preprocess_image('),
            ('predict_disease', 'def predict_disease(')
        ]
        
        missing_elements = []
        for name, pattern in required_elements:
            if pattern not in content:
                missing_elements.append(name)
        
        if missing_elements:
            print(f"❌ Missing elements in app.py: {missing_elements}")
            return False
        else:
            print("✓ All required elements present in app.py")
            return True
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def test_html_interface():
    """Test HTML interface"""
    print("\nTesting HTML interface...")
    
    try:
        with open('templates/index.html', 'r') as f:
            content = f.read()
        
        required_elements = [
            'AgroVisionNet',
            'Upload Plant Image',
            'Analyze Plant',
            'fetch(\'/predict\'',
            'FormData',
            'result-section'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing elements in index.html: {missing_elements}")
            return False
        else:
            print("✓ All required elements present in HTML interface")
            return True
    except Exception as e:
        print(f"❌ Error reading index.html: {e}")
        return False

def test_training_script():
    """Test training script structure"""
    print("\nTesting train_model.py structure...")
    
    try:
        with open('train_model.py', 'r') as f:
            content = f.read()
        
        required_elements = [
            'create_model',
            'train_model',
            'MobileNetV2',
            'ImageDataGenerator',
            'model.save'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing elements in train_model.py: {missing_elements}")
            return False
        else:
            print("✓ All required elements present in train_model.py")
            return True
    except Exception as e:
        print(f"❌ Error reading train_model.py: {e}")
        return False

def test_predict_script():
    """Test prediction script structure"""
    print("\nTesting predict.py structure...")
    
    try:
        with open('predict.py', 'r') as f:
            content = f.read()
        
        required_elements = [
            'load_model',
            'preprocess_image',
            'def predict(',
            'DISEASE_CLASSES',
            'sys.argv'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Missing elements in predict.py: {missing_elements}")
            return False
        else:
            print("✓ All required elements present in predict.py")
            return True
    except Exception as e:
        print(f"❌ Error reading predict.py: {e}")
        return False

def test_readme():
    """Test README documentation"""
    print("\nTesting README.md documentation...")
    
    try:
        with open('README.md', 'r') as f:
            content = f.read()
        
        required_sections = [
            'Installation',
            'Usage',
            'API Endpoints',
            'Model Details',
            'Technologies Used',
            'Project Structure'
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ Missing sections in README.md: {missing_sections}")
            return False
        else:
            print("✓ All required sections present in README.md")
            return True
    except Exception as e:
        print(f"❌ Error reading README.md: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("AgroVisionNet Application Tests")
    print("="*60)
    
    tests = [
        test_file_structure,
        test_requirements,
        test_app_structure,
        test_html_interface,
        test_training_script,
        test_predict_script,
        test_readme
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Application structure is complete.")
        return 0
    else:
        print(f"\n❌ {total - passed} test(s) failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
