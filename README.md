# Park Buddies

**Note**  
Currently in the process of being refactored and overhauled to take advantage of new features on Flask.

## Description
<!-- 
Provide a short description explaining the what, why, and how of your project. Use the following questions as a guide:

- What was your motivation?
- Why did you build this project? (Note: the answer is not "Because it was a homework assignment.")
- What problem does it solve?
- What did you learn? -->

A web application to find National Parks to explore and find information about current operations. Started out as the Capstone project, but has since moved into a fun personal project.

![park-buddies](https://img.shields.io/website?down_color=red&down_message=offline&style=for-the-badge&up_color=green&up_message=online&url=https%3A%2F%2Fpark-buddies.kchungdev.com)
![park-buddies](https://img.shields.io/github/last-commit/kev-odin/park-buddies?style=for-the-badge)
![park-buddies](https://img.shields.io/github/languages/count/kev-odin/park-buddies?style=for-the-badge)
![park-buddies](https://img.shields.io/github/languages/top/kev-odin/park-buddies?style=for-the-badge)
![park-buddies](https://img.shields.io/github/repo-size/kev-odin/park-buddies?style=for-the-badge)
![park-buddies](https://img.shields.io/github/license/kev-odin/park-buddies?style=for-the-badge)
![park-buddies](https://img.shields.io/badge/made%20with-%E2%9D%A4%EF%B8%8F-grey?style=for-the-badge)

## Table of Contents (Optional)
<!-- If your README is long, add a table of contents to make it easy for users to find what they need.
 -->
- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [License](#license)

## Installation
<!-- What are the steps required to install your project? Provide a step-by-step description of how to get the development environment running. -->

### Docker Compose  
1. Copy this repository and run the command: `docker compose up`  
2. This will build the images necessary to run this project.  

<!-- **Docker**  
A ready to use Docker image should be hosted in the GitHub Packages Container Registry.  
* Simply pull the image from this repository with: `docker pull ghcr.io/kev-odin/park-buddies:latest`  
* Run the image with this command: `docker run park-buddies:latest`  
* Then open your web browser and enter `localhost:5000` in the address bar. -->

### Local Installation
1. Clone this repository: `git clone git@github.com:kev-odin/park-buddies.git`
2. Create a virtual environment: `python3 -m venv venv`
3. Start venv: `source venv/bin/activate`
4. Install project requirements: `pip install -r flask-web/requirements.txt`
5. Run: `python3 flask-web/app.py`
6. Open a web browser to this URL: `localhost:5000`

## Usage
<!-- 
Provide instructions and examples for use. Include screenshots as needed.

To add a screenshot, create an `assets/images` folder in your repository and upload your screenshot to it. Then, using the relative filepath, add it to your README using the following syntax:

    ```md
    ![alt text](assets/images/screenshot.png)
    ```
 -->
 ![park-home](assets/images/park-home.webp)

## Tech Stack
![Python](https://img.shields.io/badge/Python-grey?style=for-the-badge&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-grey?style=for-the-badge&logo=javascript&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-grey?style=for-the-badge&logo=docker&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-grey?style=for-the-badge&logo=flask&logoColor=white)
![bootstrap](https://img.shields.io/badge/bootstrap-grey?style=for-the-badge&logo=bootstrap&logoColor=white)
![github actions](https://img.shields.io/badge/github_actions-grey?style=for-the-badge&logo=githubactions&logoColor=white)
![DigitalOcean](https://img.shields.io/badge/DigitalOcean-grey?style=for-the-badge&logo=digitalocean&logoColor=white)

## How to Contribute
If you are intrested in contributing to this project, feel free to create an issue, fork the repository, and create a pull request. If new features are added, write relevant unit and integration tests to ensure code coverage.

## License
Park Buddies is licensed under the [MIT License](LICENSE.txt).
