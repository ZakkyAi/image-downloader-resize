def check_library(library_name):
    try:
        __import__(library_name)
        print(f"{library_name} is installed.")
    except ImportError:
        print(f"{library_name} is NOT installed.")

# List of required libraries
libraries = ['flask', 'PIL', 'bing_image_downloader']

for lib in libraries:
    check_library(lib)
