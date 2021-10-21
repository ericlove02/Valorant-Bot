
# Valorant-Bot
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<div id="top"></div>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project  
I play a fair amount of VALORANT in my free time, so I decided to combine two of my hobbies and challenged myself to create a bot that could complete the practice session of VALORANT without human input. VALORANT and Riot Games in general has a very storng anti-cheat system, so the task was not as easy as other games, which could use injection bots or easily manipulate game inputs.   
For this project, the bot needed to be GUI based, with minimal interaction with the game. This meant usint PyTorch and OpenCV to do all of the detection. While the game is open, the program runs in the background, taking around 20 screenshots second and using a pretrained PyTorch model to search for bots in the field of view. When a bot is detected, the program uses a the height of the selected bot to target the head, as shooting the head is a one-shot kill in VALORANT. At this point, the detection portion of the bot is complete, and it us up to the inputs to finish the job.    
With the coordinates of the head selected, the bot passes the information to an Arduino through serial communitcation, and the Arduino acts as a mouse to the computer, so as not to be detected and block by the anti-cheat. The bot continues detecting and click one heads until all the bots are killed and the round is complete.    
For the bot to complete all of these actions at the same time, this program uses multithreading, with bot detection, screencapture, movement, and shooting each on their own threads.
    
#### Disclaimer: This bot was not created as a guide for people who want to cheat in VALORANT. This was created as a fun project and should not be used to ruin the game. I plan on implemnting a fail-safe that will stop the bot from functioning in online games.

### Built With
* [PyTorch](https://pytorch.org/)
* [OpenCV](https://opencv.org/)
* Multithreading
* [PyAutoGui](https://pyautogui.readthedocs.io/en/latest/#)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

```sh
   py install pip
   ```
### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/ericlove02/Valorant-Bot.git
   ```
2. Install required packages
   ```sh
   pip install -r requirements.txt
   ```
3. Run `main.py`
   ```sh
   py main.py
   ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

https://user-images.githubusercontent.com/53005525/138217033-50f1d75c-08e2-4c0b-ae6b-887c768ab35a.mp4

https://user-images.githubusercontent.com/53005525/138217040-2e148102-ddbc-401d-9f45-b225a198affa.mp4

Screen recording the output significantly dropped the frame rate.
<!-- CONTACT -->
## Contact

Eric Love - [LinkedIn](https://www.linkedin.com/in/ericlove02) - [eric.love02@yahoo.com](mailto:eric.love02@yahoo.com)

Project Link: [https://github.com/ericlove02/Valorant-Bot](https://github.com/ericlove02/Valorant-Bot)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[forks-shield]: https://img.shields.io/github/forks/ericlove02/Valorant-Bot.svg?style=for-the-badge
[forks-url]: https://github.com/ericlove02/Valorant-Bot/network/members
[stars-shield]: https://img.shields.io/github/stars/ericlove02/Valorant-Bot.svg?style=for-the-badge
[stars-url]: https://github.com/ericlove02/Valorant-Bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/ericlove02/Valorant-Bot.svg?style=for-the-badge
[issues-url]: https://github.com/ericlove02/Valorant-Bot/issues
