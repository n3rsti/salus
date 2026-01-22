# Salus - mental health and mindfulness platform


# Project Description

This project is the result of teamwork as part of the project assignment for the [Software Engineering](https://www.fer.unizg.hr/predmet/proinz) course at the Faculty of Electrical Engineering and Computing, University of Zagreb.

## Project Overview

Salus is a digital platform designed to support mental wellness through guided meditations, daily mindfulness challenges, and tools for mood and habit tracking. The app helps users monitor aspects like sleep quality, focus, and stress levels, and provides personalized recommendations to improve overall well-being based on their individual goals and tracked data.

## Motivation

The motivation behind this project comes from the increasing need for accessible and data-driven mental health support. Many people struggle to maintain mindfulness habits or track their emotional health consistently. Salus aims to make self-care simple, engaging, and help users build healthier routines.

## Problem We’re Solving

Existing mental health apps often focus on either guided content or tracking, but rarely integrate both with personalization. Our goal is to combine guided mindfulness practices with smart habit analytics and share it with people for free!

## What We’re Learning

Throughout this project, we’re learning to:

- Work effectively as a team—collaborating on design and development.

- Manage a complete project lifecycle—from planning and task distribution to implementation and testing.

- Explore new technologies and frameworks, such as:

  - Frontend: Nuxt / Vue

  - Backend: Fastapi / Python

  - Relational databases: PostgreSQL

## Deployment

For a demonstration of the application's functionality, a demo version is available at our [website](https://server.tail3ce7af.ts.net). This version allows users to explore key features and interact with the app in a limited scope.

### Accessing the Test Application
> - **Visit the Demo Link**: Navigate to the provided URL to access the live demo version of the application.
> - **Test Features**: You can explore the core functionalities, such as creating user, activities, programs split into days, each with separate activity list.
> - **Limited Scope?**: Please note that this demo version may have limited features or data for testing purposes.

For detailed instructions on installation and running the application in a local environment, please refer to the documentation in the [Wiki](https://github.com/n3rsti/salus/wiki).

## Installation
### Docker
`docker build -f api/Dockerfile -t 'salus-api' .`

`docker build -t 'salus-frontend' .`

`docker compose -f docker-compose.yaml up -d`

If you only need to run specific services:

`docker compose -f docker-compose.yaml up service1 service2 -d`

#### Environment variables
We are using `.env` file to store environment variables.
Please refer to `.env.example`.

If running in docker you should set:

`POSTGRES_HOST=postgres`

## Technologies

- Backend
  - FastAPI framework
  - Python

- Frontend
  - Nuxt framework
  - Vue
  - tailwindcss
    
- Database
  - PostgreSQL

## Team Members

Krzysztof Witucki\
Wiktor Górka\
Kacper Malak\
Theodoros Iliadis\
Filip Špiljar

# 📝 Licence
Važeča (1)
[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This repository contains open educational resources and is licensed under the Creative Commons license, which allows you to download, share, and use the work as long as you attribute the author, do not use it for commercial purposes, and share it under the same conditions Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License HR.

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: https://creativecommons.org/licenses/by-nc/4.0/deed.hr 
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

Orginal [![cc0-1.0][cc0-1.0-shield]][cc0-1.0]
>
>COPYING: All the content within this repository is dedicated to the public domain under the CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.
>
[![CC0-1.0][cc0-1.0-image]][cc0-1.0]

[cc0-1.0]: https://creativecommons.org/licenses/by/1.0/deed.en
[cc0-1.0-image]: https://licensebuttons.net/l/by/1.0/88x31.png
[cc0-1.0-shield]: https://img.shields.io/badge/License-CC0--1.0-lightgrey.svg
