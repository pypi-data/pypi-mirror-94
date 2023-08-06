from setuptools import setup
setup(
  name = 'robocadSimPy',         # How you named your package folder (MyLib)
  packages = ['robocadSimPy'],   # Chose the same as "name"
  version = '0.0.4.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'python lib for robocadSim',   # Give a short description about your library
  author = 'Abdrakov Airat',                   # Type in your name
  author_email = 'robocadsim@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/CADindustries/robocadSim',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/CADindustries/robocadSim',    # I explain this later on
  keywords = ['simulator', 'robocadSim', 'robot'],   # Keywords that define your package best
  install_requires=['numpy'],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
