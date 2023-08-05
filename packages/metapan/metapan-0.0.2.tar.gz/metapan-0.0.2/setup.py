from setuptools import setup, find_packages 
  
# with open('requirements.txt') as f: 
#     requirements = f.readlines() 
  
long_description = 'later' 
  
setup( 
        name ='metapan', 
        version ='0.0.2', 
        author ='Anupam Gautam', 
        author_email ='gautamanupam07@gmail.com', 
        url ='https://github.com/AnupamGautam/metapan.git', 
        description ='Start', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='GPL-3.0', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'metapan = metapan.metapan:main'
            ] 
        }, 
        classifiers =( 
            "Programming Language :: Python :: 3.8", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        keywords ='pangenome on metagenome', 
        zip_safe = True
) 
